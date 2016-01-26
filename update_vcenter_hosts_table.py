#!/usr/bin/python
#####################
#Author : Aniket Gole
#Email : roshan3133@gmail.com
#####################

from pysphere import *
import MySQLdb
import re
from contextlib import closing
import logging
import time

#todays Date
today = time.strftime("%d-%m-%Y")
logfile= str('vcenter_host_' + today +'.log')
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
# prepare a cursor object using cursor() method
#cursor = db.cursor
logger.info("======== Script started =========")
with closing(db.cursor()) as cur:
  sql1 = 'select host_ip from %s' % (table_name)
  cur.execute(sql1)
  esxi_hosts = cur.fetchall() 
  esxi_hosts_list = [i[0] for i in esxi_hosts]
server = VIServer()
server.connect(vcenter_server_ip, vcenter_server_user, vcenter_server_pass)
hosts = server.get_hosts()
logger.info("Total Host in %s table before update : %s" % len(table_name, esxi_hosts_list))
logger.info("Total number Host in %s before update : %s" % len(table_name, hosts.values()))

for k,v in hosts.items():
      #if v == ip:
      #vm_d['status'] = "in_vc"
      esxi_host_ip = v
      #print "host_ip in vcenter == ",esxi_host_ip
      if v not in esxi_hosts_list:
        print "host_ip in vcenter == ", esxi_host_ip
        sql = "INSERT INTO %s (host_ip) VALUES ('"'%s'"')" % (table_name, esxi_host_ip)
        print "sql query == ", sql
        with closing(db.cursor()) as cur:
	  cur.execute(sql)
          print "db updated"
	  db.commit()
# disconnect from server

# Reporting after db t_vcenter table update
with closing(db.cursor()) as cur:
  sql1 = ('select host_ip from %s' % (table_name))
  cur.execute(sql1)
  esxi_hosts = cur.fetchall() 
  esxi_hosts_list = [i[0] for i in esxi_hosts]
logger.info("Total Host in %s table after update : %s" % len(table_name, esxi_hosts_list))
logger.info("Total number of Host in vcenter after update : %s" % len(table_name, hosts.values()))
logger.info("======== Script Ended =========")

db.close()
