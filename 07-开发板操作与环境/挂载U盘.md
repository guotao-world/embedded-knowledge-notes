# 挂载 U 盘

## 一、挂载

```bash
lsblk
mkdir /mnt/usb
mount /dev/sda1 /mnt/usb
```

## 二、拷贝

```bash
cp somefile.txt /mnt/usb/
```

## 三、弹出

```bash
umount /mnt/usb    # 或 umount /dev/sda1
sync               # 同步缓存
```

---

## 四、说明

| 命令 | 作用 |
|------|------|
| `lsblk` | 查看块设备，确认 U 盘设备名 |
| `mkdir /mnt/usb` | 创建挂载点 |
| `mount /dev/sda1 /mnt/usb` | 挂载 U 盘第一个分区 |
| `umount /mnt/usb` | 卸载 U 盘 |
| `sync` | 同步缓存到磁盘，确保数据写入完成 |

> 注意：卸载前务必执行 `sync`，否则可能导致数据丢失。
