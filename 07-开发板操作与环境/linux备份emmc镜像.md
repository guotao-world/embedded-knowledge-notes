# Linux 备份 eMMC 镜像

## 一、dd 工具

**Data Duplicator（数据复制器）**

---

## 二、备份镜像

### 先卸载分区

```bash
umount /run/media/mmcblk1p1
umount /run/media/mmcblk1p2
```

### 再生成镜像

```bash
dd if=/dev/mmcblk1 of=/home/root/mmc_image.img status=progress
```

---

## 三、恢复镜像

### 先卸载分区

```bash
umount /run/media/mmcblk1p1
umount /run/media/mmcblk1p2
```

### 再恢复镜像

```bash
dd if=/home/root/mmc_image.img of=/dev/mmcblk1 status=progress
```

---

## 四、参数说明

| 参数 | 含义 |
|------|------|
| `if` | 输入设备（源） |
| `of` | 输出文件/设备（目标） |
| `status=progress` | 显示进度 |
