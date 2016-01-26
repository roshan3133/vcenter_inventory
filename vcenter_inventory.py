#!/usr/bin/python
#####################
#Author : Aniket Gole
#Email : roshan3133@gmail.com
#####################
from pysphere import *
import time
import MySQLdb
import re
from contextlib import closing
import logging

#todays Date
today = time.strftime("%d-%m-%Y")
logfile= str('vcenter_inventory_' + today +'.log')
#Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('/var/log/'+logfile)
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# Open database connection
mysqlhost = ""
mysqluser = ""
mysqlpass = ""
mysqldb = ""
table_name = ""
# Vcenter server details
vcenter_server_ip = ""
vcenter_server_user = ""
vcenter_server_pass = ""

db = MySQLdb.connect(mysqlhost, mysqluser, mysqlpass, mysqldb)
#table_name = 't_vcenter'

# prepare a cursor object using cursor() method
# Reporting after db t_vcenter table update
with closing(db.cursor()) as cur:
  #sql1 = 'CREATE TABLE IF NOT EXISTS %s (host_ip varchar(30), vm_name varchar(60), vm_os varchar(100), vm_ipv4 varchar(20), vm_ipv6 varchar(100), vm_ips varchar(250))' % (table_name)
  sql2 = ('select distinct host_ip from %s' % (table_name))
  sql3 = ('select vm_name from %s' % (table_name))
  #cur.execute(sql1)
  cur.execute(sql2)
  esxi_hosts = cur.fetchall() 
  esxi_hosts_list = [i[0] for i in esxi_hosts]
  cur.execute(sql3)
  host_vm = cur.fetchall()
  host_vm_list = [i[0] for i in host_vm]
logger.info("======== Script started =========")
logger.info("Total Host in %s table before update : %s" % len(table_name, esxi_hosts_list))
logger.info("Total VM in %s table before update : %s" % len(table_name, host_vm_list))

#Global Variables
#date = time.asctimetime.localtime(time.time()) 
server = VIServer()
server.connect(vcenter_server_ip, vcenter_server_user, vcenter_server_pass)
ipv4pat = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
ipv6pat = re.compile("^(2405:).*")
hosts = server.get_hosts()
logger.info("Total Host in Vcenter : %s" % len(hosts.values()))
error_ip = ['10.70.8.201']

    #host = [k for k,v in hosts.items() if v==ip][0]
for k,v in hosts.items():
    if v not in error_ip:
      #if v not in esxi_hosts_list:
        esxi_host_ip = v
        logger.info("host_ip in vcenter == %s" % esxi_host_ip)
        p = VIProperty(server, k)
        vms = p.vm
        for vm in vms:
          if vm.name:
          #if vm.name not in host_vm_list:
            vm_obj = server.get_vm_by_name(vm.name)
            net = vm_obj.get_property('net', from_cache=False)
            os = vm_obj.get_property('guest_full_name', from_cache=False)
            vm_name = vm.name
            logger.info("vm_name -- %s" % vm_name)
            vm_os = os
            logger.info("vm_os -- %s" % vm_os)
            ips = []
            ipv4 ="NULL"
            ipv6 = "NULL"
            if net:
              logger.info("Total IPs %s" % net)
              c_net = len(net)
              for cn in xrange(c_net):
                vm_ip = net[cn].get('ip_addresses')
                logger.info("ip --- %s" % vm_ip)
                lip = len(vm_ip)
                logger.info("length -- %s" % lip)
                if lip != 0:
                  logger.info("ip list is > 0")
                  for ipv in xrange(lip):
                    #logger.info("vsip",vm_ip[ipv]) 
                    if ipv4pat.match(vm_ip[ipv]):
                      #logger.info("got the ipv4")
		      if ipv4 == 'NULL':
                        ipv4 = vm_ip[ipv]
                        logger.info("Got ipv4 : %s" % ipv4)
                      else:
                        #logger.info("got the ips")
                        ips.append(vm_ip[ipv])
                    elif ipv6pat.match(vm_ip[ipv]):
                      #logger.info("got the ipv6")
                      if ipv6 == 'NULL':   
                        ipv6 = vm_ip[ipv]
                        logger.info("Got ipv6 : %s" % ipv6)
                      else:
                        #logger.info("got the ips")
                        ips.append(vm_ip[ipv])
                    else:
                      #logger.info("got the ips")
                      ips.append(vm_ip[ipv])
            ipt = ','.join(ips)
            logger.info("Got ips : %s" % ips)
            if vm.name in host_vm_list and esxi_host_ip in esxi_hosts_list: 
              sql = ("UPDATE %s SET vm_os='"'%s'"', vm_ipv4='"'%s'"', vm_ipv6='"'%s'"', vm_ips='"'%s'"' where host_ip='"'%s'"' and vm_name='"'%s'"'" % (table_name, vm_os, ipv4, ipv6, ipt, esxi_host_ip, vm_name))
              logger.info("sql query == %s" % sql)
              #exit(0)
              with closing(db.cursor()) as cur:
	        cur.execute(sql)
                logger.info("Values updated in database")
	        db.commit()
            else:
              sql = ("INSERT INTO %s (host_ip, vm_name, vm_os, vm_ipv4, vm_ipv6, vm_ips) VALUES ('"'%s'"', '"'%s'"', '"'%s'"', '"'%s'"', '"'%s'"', '"'%s'"')" % (table_name, esxi_host_ip, vm_name, vm_os, ipv4, ipv6, ipt)) 
              logger.info("sql query == %s" % sql)
              #exit(0)
              with closing(db.cursor()) as cur:
	        cur.execute(sql)
                logger.info("Values inserted in database")
	        db.commit()
	  else:
            logger.info("This host does not have vm in vcenter : ",esxi_host_ip)

# Reporting after db t_vcenter table update
with closing(db.cursor()) as cur:
  #sql1 = 'CREATE TABLE IF NOT EXISTS %s (host_ip varchar(30), vm_name varchar(60), vm_os varchar(100), vm_ipv4 varchar(20), vm_ipv6 varchar(100), vm_ips varchar(250))' % (table_name)
  sql2 = ('select distinct host_ip from %s' % (table_name))
  sql3 = ('select vm_name from %s' % (table_name))
  #cur.execute(sql1)
  cur.execute(sql2)
  esxi_hosts = cur.fetchall() 
  esxi_hosts_list = [i[0] for i in esxi_hosts]
  cur.execute(sql3)
  host_vm = cur.fetchall()
  host_vm_list = [i[0] for i in host_vm]
logger.info("Total Host in %s after update : %s" % len(table_name, esxi_hosts_list))
logger.info("Total VM in t_%s table after update : %s" % len(table_name, host_vm_list))
logger.info("======== Script Ended =========")

#Closing mysql connection              
db.close()
