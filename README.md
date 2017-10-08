# ansible-hdp
# Author : Mounir ZAGHAB
# Date : 31/07/2016 
=== Build Vagrant Environment 

Author : Mounir ZAGHAB

Init cluster VM : 

----
install hdp cluster : http://docs.hortonworks.com/HDPDocuments/Ambari-2.5.0.3/bk_ambari-installation/content/ch_Getting_Ready.html

launch :
cd vagrant; ./setup.sh

test connectivity           : ansible -i ../ansible/inventories/vagrant-cluster.hosts  -m ping all -u vagrant

Install init                : ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant --tags init  

Install ambari server /agent: ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant --tags ambari  

Ambari UI : http://192.168.162.101:8080/ 

vagrant ssh vag001
----
Blueprint cluster creation : 
----
https://cwiki.apache.org/confluence/display/AMBARI/Blueprints

- list of blueprint : 
	curl --user admin:admin -i -X GET http://192.168.162.101:8080/api/v1/blueprints
- Register Blueprint with Ambari
	curl --user admin:admin -i -X POST -H X-Requested-By:ambari -d @mycluster.json http://192.168.162.101:8080/api/v1/blueprints/myblueprint
- Delete registered Blueprint :
	curl --user admin:admin -i -X DELETE -H X-Requested-By:ambari http://192.168.162.101:8080/api/v1/blueprints/myblueprint
- Setup Stack Repositories (Optional)
	curl --user admin:admin -i -X PUT -H X-Requested-By:ambari -d '{"Repositories":{"base_url":"http://192.168.56.114/hortonworks/HDP/2.6/centos6/","verify_base_url":"true"}}' http://192.168.162.101:8080/api/v1/stacks/HDP/versions/2.6/operating_systems/redhat6/repositories/HDP-2.6
	curl --user admin:admin -i -X PUT -H X-Requested-By:ambari -d '{"Repositories":{"base_url":"http://192.168.56.114/hortonworks/HDP-UTILS-1.1.0.21/centos6/","verify_base_url":"true"}}' http://192.168.162.101:8080/api/v1/stacks/HDP/versions/2.6/operating_systems/redhat6/repositories/HDP-UTILS-1.1.0.21
- Create Cluster
	curl --user admin:admin -i -X POST -H X-Requested-By:ambari -d @myhostmapping.json http://192.168.162.101:8080/api/v1/clusters/mycluster
- List Cluster :
	curl --user admin:admin -i -X GET http://192.168.162.101:8080/api/v1/clusters/
----

Rest API cluster creation TODO: 

----
https://cwiki.apache.org/confluence/display/AMBARI/Create+a+new+Cluster
Install hdp  		: ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant --tags hdp 

Launch all			: ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant

Install cluster		: ansible-playbook -i vagrant-cluster.hosts ../playbooks/site.yml --tags cdh-install -u vagrant -e cdh_new_install='True'

do all in one shot :  ansible-playbook via : ansible-playbook -i vagrant-cluster.hosts ../playbooks/site.yml -u vagrant -e cdh_new_install='True'
----
