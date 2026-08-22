# Linux 开发板挂载共享文件夹

## 一、挂载 NFS 共享

```bash
mount -t nfs 服务器IP:/共享路径 /mnt/nfs -o nolock
```

## 二、挂载 SMB 共享

```bash
mount -t cifs //服务器IP/共享名 /mnt/smb -o username=用户,password=密码
```

---

## 三、示例

```bash
mkdir /mnt/nfs
mount -t nfs 192.168.1.100:/home/user/share /mnt/nfs -o nolock
```

---

## 四、卸载

```bash
umount /mnt/nfs
```

---

## 五、常用参数

| 参数 | 作用 |
|------|------|
| `-t nfs` | NFS 网络文件系统 |
| `-t cifs` | CIFS/SMB 共享 |
| `-o nolock` | NFS 禁用文件锁（嵌入式常用） |
| `-o username=,password=` | CIFS 认证信息 |
