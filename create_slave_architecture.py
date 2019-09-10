import subprocess
hosts_path = "/etc/hosts"
sudo_pass = 123456
machine_user = "root" # need to change or default make all of them to "root"

master_ip = input("What is Master IP? ")
slave_count = input("How many slaves are there? ")

master_of_puppets = [{"master":master_ip}]
for slave in range(int(slave_count)):
    IP = input("What is hadoop-slave_{} IP? ".format(slave))
    master_of_puppets.append({"hadoop-slave_{}".format(slave):IP})


machine_names = []
for machine in master_of_puppets:
    machine_names.append(machine.keys())

## ilk sudo olmak gerek
subprocess.call("echo  '\n' >> {}".format(hosts_path), shell=True)
for i in master_of_puppets:
    ips = list(i.values())[0]+" "+list(i.keys())[0]
    subprocess.call("echo '{}' >> {}".format(ips,hosts_path), shell=True)

exit()

#https://www.edureka.co/blog/setting-up-a-multi-node-cluster-in-hadoop-2-x/
subprocess.call('ssh-keygen -t rsa -P ""', shell=True)
subprocess.call('cat $HOME/.ssh/id_rsa.pub >> $HOME/.ssh/authorized_keys ', shell=True)
for machine_name in machine_names:
    subprocess.call("ssh-copy-id -i $HOME/.ssh/id_rsa.pub {}@{}".format(machine_user,machine_name), shell=True)
    subprocess.call("chmod 0600 $HOME/.ssh/authorized_keys", shell=True)


subprocess.call("chmod +x install_spark.sh", shell=True)
print("Chmod done! and install_spark shell is running!")
subprocess.call("echo {} | sudo -S ./install_spark.sh".format(sudo_pass), shell=True)





