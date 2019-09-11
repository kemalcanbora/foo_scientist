# Foo Scientist

Apache Spark follows a master/slave architecture with two main daemons
  - Master Daemon — (Master/Driver Process)
  - Worker Daemon –(Slave Process)

Cluster Manager
![alt text](https://miro.medium.com/max/534/1*o80WzWJShjCV1RSfWzCiQA.png)

Sometimes architecture can be hard to build for this there are solutions such as cloudera etc. I wanted to do it my way.
All you have to do is edit the json file yourself it's name is **architecture.json** and run mimar.py

<h2>Note:</h2> Don't change type in json file and if you add another slave in json file just add new number end of the name like 
hadoop_slave_2, hadoop_slave_3 .. 

<h2>JSON File</h2>
<pre>
[{
  "type":"hadoop-master",
  "password":"123456",
  "IP": "10.11.2.183",
  "username": "root",
  "name": "hadoop_master_mimar"
},
{
  "type":"hadoop-slave",
  "password":"123456",
  "IP": "10.11.2.228",
  "username": "root",
  "name": "hadoop_slave_1"
}]
</pre>
