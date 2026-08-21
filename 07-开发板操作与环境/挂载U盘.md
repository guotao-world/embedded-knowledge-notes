# 挂载U盘

**挂载：**

lsblk
mkdir /mnt/usb
mount /dev/sda1 /mnt/usb

**拷贝：**

cp somefile.txt /mnt/usb/

**弹出：**

umount /mnt/usb # 或 umount /dev/sda1
sync # 同步缓存