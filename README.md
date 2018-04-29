# ansible-hdp
# Author : Mounir ZAGHAB
# Date : 31/07/2016 
=== Build Vagrant Environment 

Author : Mounir ZAGHAB

Init cluster VM : 

----
https://docs.hortonworks.com/

install ambari:
https://docs.hortonworks.com/HDPDocuments/Ambari-2.6.1.5/bk_ambari-installation/content/ch_Getting_Ready.html

## AZURE
test connectivity           : 

`ansible -i ansible/inventories/azure_rm.py  -m ping all`

Install init                : 

`ansible-playbook -i ansible/inventories/azure_rm.py ansible/playbooks/site.yml  --tags init`

Install ambari server and agent: 

`ansible-playbook -i ansible/inventories/azure_rm.py ansible/playbooks/site.yml --tags ambari`

Ambari UI   : http://192.168.162.101:8080/ 

## VAGRANT
launch :
cd vagrant; ./setup.sh

test connectivity           : ansible -i ../ansible/inventories/vagrant-cluster.hosts  -m ping all -u vagrant

Install init                : ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant --tags init  

Install ambari server /agent: ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant --tags ambari  

Ambari UI   : http://192.168.162.101:8080/ 
    
ssh connect : vagrant ssh vag-hdp001

Blueprint cluster creation : 
----
https://cwiki.apache.org/confluence/display/AMBARI/Blueprints
- Register Blueprint with Ambari :
	curl --user admin:admin -i -X POST -H X-Requested-By:ambari -d @mycluster.json http://192.168.162.101:8080/api/v1/blueprints/myblueprint
- Create Cluster :
	curl --user admin:admin -i -X POST -H X-Requested-By:ambari -d @myhostmapping.json http://192.168.162.101:8080/api/v1/clusters/mycluster

Usefull blueprint curls : 
- Export blueprint from existing cluster :
	curl --user admin:admin -i -X GET http://192.168.162.101:8080/api/v1/clusters/:clusterName?format=blueprint
- list of blueprint : 
	curl --user admin:admin -i -X GET http://192.168.162.101:8080/api/v1/blueprints
- Register Blueprint with Ambari :
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
- Delete Cluster : 
    curl --user admin:admin -i -X DELETE -H X-Requested-By:ambari http://192.168.162.101:8080/api/v1/clusters/mycluster

----

Rest API cluster creation TODO: 
https://cwiki.apache.org/confluence/display/AMBARI/Add+a+host+and+deploy+components+using+APIs


----
https://cwiki.apache.org/confluence/display/AMBARI/Create+a+new+Cluster
Install hdp  		: ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant --tags hdp 

Launch all			: ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant

Install cluster		: ansible-playbook -i vagrant-cluster.hosts ../playbooks/site.yml --tags cdh-install -u vagrant -e cdh_new_install='True'

do all in one shot :  ansible-playbook via : ansible-playbook -i vagrant-cluster.hosts ../playbooks/site.yml -u vagrant -e cdh_new_install='True'

----
