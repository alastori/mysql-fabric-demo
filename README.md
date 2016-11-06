MySQL Fabric 1.5 Demo
=====================

A demonstration of MySQL Fabric 1.5 capabilities using vagrant+virtualbox.

## Synopsis
These are files to create a environment for demonstrantion of [MySQL Fabric 1.5](http://dev.mysql.com/doc/mysql-utilities/1.5/en/fabric.html) using [Vagrant](https://www.vagrantup.com/) and [Virtualbox](https://www.virtualbox.org/) on CentOS 7.

## Architecute
There will be one single VM with 4 MySQL instances accessible through ports 3306 to 3309.

## Pre-reqs
You need to have altready installed:
- [Vagrant](https://www.vagrantup.com/downloads.html) 
- [Virtualbox](https://www.virtualbox.org/wiki/Downloads)

The rest of the software will be automatically downloaded and installed.

## How to use

- Inside the directory, run ```vagrant up```. 
  - It will download CentOS 7, MySQL Server, MySQL Fabric. This will take several minutes to finish.
  - Also this repository will be downloaded inside the VM folder ```/vagrant```. 
- Access the VM with ```vagrant ssh```.
- Issue the commands from ```/vagrant/fabric-demo-create.sh```.
- Follow the demo steps in ```/vagrant/fabric-demo-t?.sh```.
  
## Rollback

If you need, you can remove the datadir with:
```
mysqld_multi --password=Root#123 stop
rm -Rf /data/mysql*
```