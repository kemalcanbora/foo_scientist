cd /usr/local/spark/conf
cp spark-env.sh.template spark-env.sh
echo '''export SPARK_MASTER_HOST=<Path_of_JAVA_installation>''' >> spark-env.sh
echo '''export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/''' >> spark-env.sh
sudo nano slaves
cd /opt/spark
./sbin/start-all.sh