# linux开发板查看系统信息

**查看CPU信息：**

cat /proc/cpuinfo

**查看内存信息：**

cat /proc/meminfo
free -h

**查看磁盘信息：**

df -h
lsblk

**查看内核版本：**

uname -a

**查看系统版本：**

cat /etc/os-release
cat /etc/issue

**查看运行时间和负载：**

uptime

**查看进程：**

top
ps aux

**查看中断：**

cat /proc/interrupts