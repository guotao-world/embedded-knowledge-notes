# linux开发板设置静态IP

**临时设置（重启失效）：**

ifconfig eth0 192.168.1.100 netmask 255.255.255.0
route add default gw 192.168.1.1

**永久设置（修改配置文件）：**

vi /etc/network/interfaces

**配置内容：**

auto eth0
iface eth0 inet static
address 192.168.1.100
netmask 255.255.255.0
gateway 192.168.1.1
dns-nameservers 8.8.8.8

**重启网络：**

/etc/init.d/networking restart

或

systemctl restart networking