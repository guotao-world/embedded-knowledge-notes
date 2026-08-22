# Linux 开发板 SCP 传输文件

## 一、从本地拷贝到开发板

```bash
scp 本地文件 root@开发板IP:/目标路径
```

## 二、从开发板拷贝到本地

```bash
scp root@开发板IP:/源文件 本地路径
```

---

## 三、示例

```bash
scp zImage root@192.168.55.71:/run/media/mmcblk1p1/
scp root@192.168.55.71:/home/root/log.txt ./
```

---

## 四、传输整个目录

```bash
scp -r 本地目录 root@开发板IP:/目标路径
```

---

## 五、常用参数

| 参数 | 作用 |
|------|------|
| `-r` | 递归复制目录 |
| `-P` | 指定端口（大写 P） |
| `-p` | 保留文件修改时间和权限 |
