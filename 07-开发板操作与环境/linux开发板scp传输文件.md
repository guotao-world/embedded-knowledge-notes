# linux开发板scp传输文件

**从本地拷贝到开发板：**

scp 本地文件 root@开发板IP:/目标路径

**从开发板拷贝到本地：**

scp root@开发板IP:/源文件 本地路径

**示例：**

scp zImage root@192.168.55.71:/run/media/mmcblk1p1/
scp root@192.168.55.71:/home/root/log.txt ./

**传输整个目录：**

scp -r 本地目录 root@开发板IP:/目标路径