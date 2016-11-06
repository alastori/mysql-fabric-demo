#!/bin/bash

#Download repo using git client
yum -y install git
mkdir -p /vagrant
cd /vagrant
git clone https://github.com/alastori/mysql-fabric-demo.git
mv /vagrant/mysql-fabric-demo/* /vagrant
rm -Rf /vagrant/mysql-fabric-demo