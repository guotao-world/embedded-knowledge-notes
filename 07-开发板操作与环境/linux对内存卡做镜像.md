# linux对内存卡做镜像

**查看设备：**

lsblk

**卸载分区：**

umount /dev/sdb1
umount /dev/sdb2

**开始整卡备份带压缩：**

sudo dd if=/dev/sdb bs=4M | gzip > sdcard.img.gz

**开始整卡备份带压缩且显示进度：**

sudo dd if=/dev/sdd bs=4M | pv -s 128G | gzip > sdcard.img.gz

**开始整卡备份不带压缩：**

sudo dd if=/dev/sdd of=sdcard_backup.img bs=4M status=progress

**参数含义**

if 输入设备（你的 SD 卡）
of 输出镜像文件
bs=4M 提高速度
status=progress 显示进度

**校验（如果采用的压缩的方式就不能校验了）：**

md5sum sdcard_backup.img

**恢复镜像带解压：**

gunzip -c sdcard.img.gz | sudo dd of=/dev/sdb bs=4M status=progress conv=fsync

**恢复镜像不带解压：**

dd if=sdcard_backup.img of=/dev/sdb bs=4M status=progress