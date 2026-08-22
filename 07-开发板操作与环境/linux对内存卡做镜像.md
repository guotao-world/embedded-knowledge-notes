# Linux 对内存卡做镜像

## 一、查看设备

```bash
lsblk
```

## 二、卸载分区

```bash
umount /dev/sdb1
umount /dev/sdb2
```

---

## 三、整卡备份

### 带压缩

```bash
sudo dd if=/dev/sdb bs=4M | gzip > sdcard.img.gz
```

### 带压缩且显示进度

```bash
sudo dd if=/dev/sdd bs=4M | pv -s 128G | gzip > sdcard.img.gz
```

### 不带压缩

```bash
sudo dd if=/dev/sdd of=sdcard_backup.img bs=4M status=progress
```

---

## 四、参数含义

| 参数 | 含义 |
|------|------|
| `if` | 输入设备（你的 SD 卡） |
| `of` | 输出镜像文件 |
| `bs=4M` | 块大小，提高速度 |
| `status=progress` | 显示进度 |

---

## 五、校验

> 如果采用压缩的方式就不能用 md5sum 校验了。

```bash
md5sum sdcard_backup.img
```

---

## 六、恢复镜像

### 带解压

```bash
gunzip -c sdcard.img.gz | sudo dd of=/dev/sdb bs=4M status=progress conv=fsync
```

### 不带解压

```bash
dd if=sdcard_backup.img of=/dev/sdb bs=4M status=progress
```
