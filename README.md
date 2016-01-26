# vcenter_inventory
Get the information from Vcenter servers and update mysql tables with 
vcenter_host_ip, vm_name, vm_ipv4, vm_ipv6, vm_ips, vm_os

### make database table with below coloumn
vcenter_host_ip, vm_name, vm_os, vm_ipv4, vm_ipv6, vm_ips

### Description:
This will update MySQL table with all esxi host_ip, vm_name, vm_ipv4, vm_ipv6, vm_os etc...

###Requirment:
Need python >= 2.7

###Usage:
```
update vcenter vm table for all esxi host_ip, vm_name, vm_ipv4, vm_ipv6, vm_os etc...
python vcenter_inventory.py

update vcenter hosts table for vcenter or esxi_host_ip only.
python update_vcenter_hosts_table.py
```
###Logs:
After execution it will genrate logs in 
/var/log/vcenter_inventory_dd-mm-yy.logs 
/var/log/vcenter_host__dd-mm-yy.logs 
