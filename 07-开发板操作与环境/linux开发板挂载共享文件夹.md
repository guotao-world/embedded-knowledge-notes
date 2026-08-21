# linux开发板挂载共享文件夹

**挂载NFS共享：**

mount -t nfs 服务器IP:/共享路径 /mnt/nfs -o nolock

**挂载SMB共享：**

mount -t cifs //服务器IP/共享名 /mnt/smb -o username=用户,password=密码

**示例：**

mkdir /mnt/nfs
mount -t nfs 192.168.1.100:/home/user/share /mnt/nfs -o nolock

**卸载：**

umount /mnt/nfs