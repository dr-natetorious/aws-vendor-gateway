#!/bin/bash

yum -y update
yum -y install httpd mod_ssl
service httpd start
/sbin/chkconfig httpd on
echo "<html><h1>hello from `hostname`</h1></html>" > /var/www/html/index.html
