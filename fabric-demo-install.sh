#!/bin/bash

#Modify these variables as you wish
DIR_TO_INSTALL=/usr
#PACKAGES_DIR=/home/vagrant/packages
MYSQL_BASEDIR=$DIR_TO_INSTALL
MYSQL_DATADIR=/data
MYSQL_ADMIN_USER=root
MYSQL_ADMIN_PWD="Root#123"

#Stop running MySQL instance at port 3306
mysqladmin -u$MYSQL_ADMIN_USER -p$MYSQL_ADMIN_PWD -P3306 shutdown
sleep 6
ps -ef | grep mysqld

#Next lines set up my.cnf with enough servers for Fabric
echo "[client]" > /etc/my.cnf
echo "protocol=tcp" >> /etc/my.cnf
echo "" >> /etc/my.cnf
echo "[mysqld_multi]" >> /etc/my.cnf
echo "mysqld = $MYSQL_BASEDIR/sbin/mysqld" >> /etc/my.cnf
echo "mysqladmin = $MYSQL_BASEDIR/bin/mysqladmin" >> /etc/my.cnf
echo "user = $MYSQL_ADMIN_USER" >> /etc/my.cnf
echo "password = $MYSQL_ADMIN_PWD" >> /etc/my.cnf
echo "" >> /etc/my.cnf
for x in {0..3}; do
    port=$((3306 + $x))
    mkdir -p $MYSQL_DATADIR/mysql$x
    chown -R mysql:mysql $MYSQL_DATADIR
    cd $MYSQL_BASEDIR
    mysqld --initialize-insecure --user=mysql --datadir=$MYSQL_DATADIR/mysql$x 
    echo "[mysqld$x]" >> /etc/my.cnf
    echo "user = mysql" >> /etc/my.cnf
    echo "socket = /data/mysql$x/mysqld.sock" >> /etc/my.cnf
    echo "port = $port" >> /etc/my.cnf
    echo "basedir = $MYSQL_BASEDIR" >> /etc/my.cnf
    echo "datadir = /data/mysql$x/" >> /etc/my.cnf
    echo "pid-file = /data/mysql$x/mysql$x.pid" >> /etc/my.cnf
    echo "general_log" >> /etc/my.cnf
    echo "log-bin" >> /etc/my.cnf
    echo "gtid_mode=ON" >> /etc/my.cnf
    echo "enforce-gtid-consistency" >> /etc/my.cnf
    echo "log-slave-updates" >> /etc/my.cnf
    echo "relay-log-recovery" >> /etc/my.cnf
    echo "binlog_format=mixed" >> /etc/my.cnf
    echo "server-id=$x" >> /etc/my.cnf
    echo " " >> /etc/my.cnf
    echo "alias mysql$x='mysql -u$MYSQL_ADMIN_USER -p$MYSQL_ADMIN_PWD -P$port'" >> /root/.bashrc
done
source /root/.bashrc

#Starting MySQL Server  
echo "Starting MySQL instances..."
cp /vagrant/mysqld_multi $MYSQL_BASEDIR/bin
chmod +x $MYSQL_BASEDIR/bin/mysqld_multi
cd $MYSQL_BASEDIR
mysqld_multi --no-log --password=$MYSQL_ADMIN_PWD report
mysqld_multi start
sleep 6
mysqld_multi --no-log --password=$MYSQL_ADMIN_PWD report

#Changing MySQL root user password 
for x in {0..3}; do
    port=$((3306 + $x))
    mysqladmin -u$MYSQL_ADMIN_USER -P$port password "$MYSQL_ADMIN_PWD"
    mysql -u$MYSQL_ADMIN_USER -p$MYSQL_ADMIN_PWD -P$port -e"SELECT @@hostname,@@port,@@version,USER();"
done
mysqld_multi --no-log --password=$MYSQL_ADMIN_PWD report

#Setting users for fabric and for the application + resetting master just in case
for x in {0..3}; do
    port=$((3306 + $x))
    mysql -u$MYSQL_ADMIN_USER -p$MYSQL_ADMIN_PWD -P$port -e"CREATE USER IF NOT EXISTS 'fabric'@'%' IDENTIFIED BY 'secret'; GRANT ALL ON *.* TO 'fabric'@'%';"
    mysql -u$MYSQL_ADMIN_USER -p$MYSQL_ADMIN_PWD -P$port -e"CREATE USER IF NOT EXISTS 'fabric'@'localhost' IDENTIFIED BY 'secret'; GRANT ALL ON *.* TO 'fabric'@'localhost';"
    mysql -u$MYSQL_ADMIN_USER -p$MYSQL_ADMIN_PWD -P$port -e"CREATE USER IF NOT EXISTS 'web'@'%' IDENTIFIED BY 'web'; GRANT ALL ON *.* TO 'web'@'%';"
    mysql -u$MYSQL_ADMIN_USER -p$MYSQL_ADMIN_PWD -P$port -e"CREATE USER IF NOT EXISTS 'web'@'localhost' IDENTIFIED BY 'web'; GRANT ALL ON *.* TO 'web'@'localhost';"
    mysql -u$MYSQL_ADMIN_USER -p$MYSQL_ADMIN_PWD -P$port -e"RESET MASTER;"
done

#Install MySQL Utilities and MySQL Connector/Python
echo "Installing MySQL Utilities..."
yum -y install mysql-{utilities-1.5.6,connector-python}
mysqlserverinfo --version
echo "MySQL Utilities installed via YUM."

#Creating the fabric mail configuration file
mv /etc/mysql/fabric.cfg /etc/mysql/fabric-default.cfg
cp /vagrant/fabric.cfg /etc/mysql/fabric.cfg

#Listing UUIDs
mysqld_multi --no-log --password=$MYSQL_ADMIN_PWD report
for x in {0..3}; do
    port=$((3306 + $x))
    mysql -B -N -u$MYSQL_ADMIN_USER -p$MYSQL_ADMIN_PWD -P$port -e"SELECT @@datadir, @@port, @@server_uuid;"
done