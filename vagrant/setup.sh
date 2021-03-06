#!/bin/bash
# Author : Mounir ZAGHAB
# Date : 31/07/2016 

export VAGRANT_HTTP_PROXY=${http_proxy}
export VAGRANT_YUM_HTTP_PROXY=${http_proxy}
export VAGRANT_HTTPS_PROXY=${http_proxy}
export VAGRANT_FTP_PROXY=${http_proxy}
export VAGRANT_NO_PROXY=${no_proxy},/var/run/docker.sock

echo "launch virtual cluster"

vagrant up --parallel

echo "Install init"
ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant --tags init  

echo "Install ambari server /agent"

ansible-playbook -i ../ansible/inventories/vagrant-cluster.hosts ../ansible/playbooks/site.yml -u vagrant --tags ambari  

echo "Ambari UI  is accessible on : http://192.168.162.101:8080/" 
