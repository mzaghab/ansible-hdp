#!/bin/bash
cd /tmp
git clone https://github.com/apache/incubator-ambari.git
cd incubator-ambari/ambari-client/
mvn clean install rpm:rpm
mv target/rpm/ambari-client/RPMS/x86_64/ambari-client*.rpm ambari-client.rpm
rpm -ivh ambari-client.rpm
rm -r -f /tmp/incubator-ambari