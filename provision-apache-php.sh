#!/bin/bash

yum -y install httpd
systemctl start httpd.service
curl http://localhost
systemctl enable httpd.service
#echo ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
yum -y install php php-mysqlnd
systemctl restart httpd.service
#echo "<?php phpinfo(); ?>" > /var/www/html/info.php
#chmod 644 /var/www/html/info.php
curl http://localhost/info.php
#cat /var/log/httpd/error_log
#echo "<?php 
#\$mysqlnd = function_exists('mysqli_fetch_all');
#if (\$mysqlnd) {
#    echo 'mysqlnd enabled!\n';
#} else {
#    echo 'mysqlnd NOT enabled.\n';
#}" > /var/www/html/mysqlnd.php
#chmod 644 /var/www/html/mysqlnd.php
curl http://localhost/mysqlnd.php
#rm /var/www/html/info.php
yum -y install php-devel php-pear
pecl channel-update pecl.php.net
pecl install mysqlnd_ms
mv /etc/php.ini /etc/php-default.ini
#cp /vagrant/php.ini /etc/php.ini
#chmod 644 /etc/php.ini
cp /vagrant/mysqlnd_ms.ini /etc/php.d/mysqlnd_ms.ini
chmod 644 /etc/php.d/mysqlnd_ms.ini
systemctl restart httpd.service
#cp /vagrant/fabric-test.php /var/www/html/fabric-test.php
#chmod 644 /var/www/html/fabric-test.php
cat /var/log/httpd/error_log
#tail -f /var/log/httpd/error_log
