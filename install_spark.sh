apt update
apt -y install openssh-server
apt -y apt-get install sshpass
add-apt-repository ppa:webupd8team/java
apt -y update
apt -y install oracle-java8-installer oracle-java8-set-default
apt-get -y install openssh-server openssh-client
apt-get -y install scala
curl -O http://apache.mirror.anlx.net/spark/spark-2.3.4/spark-2.3.4-bin-hadoop2.6.tgz
tar xvf spark-2.3.4-bin-hadoop2.6.tgz
echo 123456 | sudo -S mv spark-2.3.4-bin-hadoop2.6/ /opt/spark
echo -e "\n" >> ~/.bashrc
echo '''export SPARK_HOME=/opt/spark''' >> ~/.bashrc
echo '''export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin''' >> ~/.bashrc
source ~/.bashrc