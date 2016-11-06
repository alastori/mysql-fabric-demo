#!/bin/bash

#Initial Fabric setup - creating fabric schema
mysqlfabric manage setup
mysql -hlocalhost -P3306 -ufabric -psecret -e"SHOW DATABASES; USE fabric; SHOW TABLES;"

#Starting Fabric Daemon
mysqlfabric manage start --daemonize
cat /var/log/fabric.log

#List HA groups (is empty)
mysqlfabric group lookup_groups

#Creating the HA group
mysqlfabric group create my_group

#List HA groups (have a new my_group)
mysqlfabric group lookup_groups

#List servers and status (is empty)
mysqlfabric group lookup_servers my_group
mysqlfabric group health my_group

#Adding servers to the group
mysqlfabric group add my_group localhost:3307
mysqlfabric group add my_group localhost:3308
mysqlfabric group add my_group localhost:3309

#List servers and status (have added servers)
mysqlfabric group lookup_servers my_group
mysqlfabric group health my_group

#Promoting one of the servers as PRIMARY (master)
mysqlfabric group promote my_group #--slave_id=<uuid>

#List servers and status
mysqlfabric group lookup_servers my_group
mysqlfabric group health my_group

#Activate the automatic failover
mysqlfabric group activate my_group
cat /var/log/fabric.log
