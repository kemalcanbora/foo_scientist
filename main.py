import json
import subprocess
import os


def read_json():
    with open('architecture.json') as json_file:
        data = json.load(json_file)
        data = json.dumps(data)
        data = json.loads(data)

    return data


def generate_hosts():
    data = read_json()
    for item in data:
        machine_host = item["IP"] + " " + item["name"]
        subprocess.call("echo {} | sudo -S -- sh -c 'echo {}>> /etc/hosts'".format(item["password"], machine_host),
                        shell=True)

        if item["type"] == "hadoop-slave":
            for slave in data:
                machine_hosts_for_slave = slave["IP"] + " " + slave["name"]

                query_for_slaver = '''sshpass -p {} ssh {}@{} "echo {} | sudo -S -- sh -c 'echo {} >> /etc/hosts'" '''.format(
                    item["password"],
                    item["username"],
                    item["IP"],
                    item["password"],
                    machine_hosts_for_slave)

                subprocess.call(query_for_slaver, shell=True)


def id_rsa_copy_to_slaves():
        data = read_json()
        subprocess.call('ssh-keygen -b 4096 -f ~/.ssh/id_rsa -N ""', shell=True)
        subprocess.call('cat ~/.ssh/id_rsa.pub | sudo tee -a ~/.ssh/authorized_keys', shell=True)
        for machine in data:
            if machine["type"] == "hadoop-slave":
                subprocess.call("sshpass -p {} ssh-copy-id -i ~/.ssh/id_rsa.pub {}@{}".format(machine["password"],
                                                                                                  machine["username"],
                                                                                                  machine["IP"]),
                                shell=True)

                subprocess.call('sshpass -p {} ssh {}@{} echo {} | sudo -S -- sh -c "systemctl restart sshd"'.format(machine["password"],
                                                                                                                     machine["username"],
                                                                                                                     machine["IP"],
                                                                                                                     machine["password"]), shell=True)


def spark_sh_install():
    path = os.getcwd()
    data = read_json()
    java_path = "/usr/lib/jvm/java-11-openjdk-amd64"

    for machine in data:
        if machine["type"] == "hadoop-master":
            # subprocess.call("echo {} | sudo -S curl -O http://apache.mirror.anlx.net/spark/spark-2.3.4/spark-2.3.4-bin-hadoop2.6.tgz".format(machine["password"]),shell=True)
            subprocess.call("chmod +x install_spark.sh", shell=True)

            subprocess.call("echo {} | sudo -S {}/install_spark.sh".format(machine["password"],path), shell=True)

            subprocess.call('echo {} | sudo -S cp -i /opt/spark/conf/spark-env.sh.template /opt/spark/conf/spark-env.sh'.format(machine["password"]), shell=True)
            subprocess.call("echo {} | sudo -S -- sh -c 'echo export SPARK_MASTER_HOST={} >> /opt/spark/conf/spark-env.sh'".format(machine["password"], machine["IP"]), shell=True)
            subprocess.call("echo {} | sudo -S -- sh -c 'echo export SPARK_MASTER_IP={} >> /opt/spark/conf/spark-env.sh'".format(machine["password"], machine["IP"]), shell=True)
            subprocess.call("echo {} | sudo -S -- sh -c 'echo export JAVA_HOME={} >> /opt/spark/conf/spark-env.sh'".format(machine["password"], java_path), shell=True)
            subprocess.call("echo {} | sudo -S -- sh -c 'echo export SPARK_LOCAL_HOSTNAME=localhost >> /opt/spark/conf/spark-env.sh'".format(machine["password"], java_path), shell=True)


            generate_slave_file()

        if machine["type"] == "hadoop-slave":
            scp_spark_file = "sshpass -p {} scp -r {}/spark-2.3.4-bin-hadoop2.6.tgz {}@{}:'/home/{}'".format(
                machine["password"],
                path,
                machine["username"],
                machine["IP"],
                machine["username"])

            subprocess.call(scp_spark_file, shell=True)

            scp_slaves_query = "sshpass -p {} scp -r {}/install_spark.sh {}@{}:'/home/{}'".format(machine["password"],
                                                                                                  path,
                                                                                                  machine["username"],
                                                                                                  machine["IP"],
                                                                                                  machine["username"])
            subprocess.call(scp_slaves_query, shell=True)

            subprocess.call('sshpass -p {} ssh {}@{} "$HOME/install_spark.sh"'.format(machine["password"],
                                                                                  machine["username"],
                                                                                  machine["IP"]), shell=True)

            slavesfile = "sshpass -p {} scp -r /opt/spark/conf/slaves {}@{}:'/opt/spark/conf/'".format(
                machine["password"],
                machine["username"],
                machine["IP"])
            subprocess.call(slavesfile, shell=True)

def generate_slave_file():
    data = read_json()
    for machine in data:
        subprocess.call("echo {} | sudo -S -- sh -c 'echo {}>> /opt/spark/conf/slaves'".format(machine["password"],
                                                                                               machine["name"]),shell=True)

if __name__ == '__main__':
    generate_hosts()
    id_rsa_copy_to_slaves()
    spark_sh_install()
