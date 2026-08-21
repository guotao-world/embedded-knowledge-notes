# linux备份emmc镜像

**dd工具：**

**Data Duplicator (数据复制器)**

**先卸载分区：**

umount /run/media/mmcblk1p1
umount /run/media/mmcblk1p2

**再生成镜像：**

dd if=/dev/mmcblk1 of=/home/root/mmc_image.img status=progress

**先卸载分区：**

umount /run/media/mmcblk1p1
umount /run/media/mmcblk1p2

再**恢复镜像：**

dd if=/home/root/mmc_image.img of=/dev/mmcblk1 status=progress