import json
import subprocess
import os

host_list = []


def read_json():
    with open('architecture.json') as json_file:
        data = json.load(json_file)
        data = json.dumps(data)
        data = json.loads(data)

    return data


def copy_hosts_file_to_all_machines(copy_done=None):
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


        if copy_done == True:
            query_for_slaver = '''sshpass -p {} ssh {}@{} "echo {} | sudo -S -- sh -c 'echo {} >> /opt/spark/conf/slaves'" '''.format(
                item["password"],
                item["username"],
                item["IP"],
                item["password"],
                item["name"])

            subprocess.call(query_for_slaver, shell=True)


def id_rsa_copy_to_slaves():
    data = read_json()
    subprocess.call('ssh-keygen -t rsa -P ""', shell=True)
    subprocess.call('cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys', shell=True)
    for machine in data:
        if machine["type"] == "hadoop-slave":
            subprocess.call("sshpass -p {} ssh-copy-id -i $HOME/.ssh/id_rsa.pub {}@{}".format(machine["password"],
                                                                                              machine["username"],
                                                                                              machine["name"]),
                            shell=True)
            subprocess.call("chmod 0600 $HOME/.ssh/authorized_keys", shell=True)


def install_spark_all_machines():
    data = read_json()
    print("Chmod done! and install_spark shell is running!")
    for machine in data:
        if machine["type"] == "hadoop-master":
            subprocess.call("chmod +x install_spark.sh", shell=True)
            subprocess.call("echo {} | sudo -S ./install_spark.sh".format(machine["password"]), shell=True)


        elif machine["type"] == "hadoop-slave":
            path = os.getcwd()
            scp_query = "scp -r {}/install_spark.sh {}@{}:'/home/{}'".format(path,
                                                                             machine["username"],
                                                                             machine["IP"],
                                                                             machine["username"])

            subprocess.call(scp_query, shell=True)
            subprocess.call('sshpass -p {} ssh {}@{} "chmod +x install_spark.sh"'.format(machine["password"],
                                                                                         machine["username"],
                                                                                         machine["IP"]), shell=True)

            subprocess.call('sshpass -p {} ssh {}@{} echo ' + machine[
                "password"] + ' | sudo -S -- sh -c "./install_spark.sh"'.format(machine["password"],
                                                                                machine["username"],
                                                                                machine["IP"]), shell=True)


if __name__ == '__main__':
     id_rsa_copy_to_slaves()
     copy_hosts_file_to_all_machines()
     install_spark_all_machines()
     copy_hosts_file_to_all_machines(copy_done=True)
