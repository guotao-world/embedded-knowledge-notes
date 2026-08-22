# Linux 开发板设置静态 IP

## 一、临时设置（重启失效）

```bash
ifconfig eth0 192.168.1.100 netmask 255.255.255.0
route add default gw 192.168.1.1
```

---

## 二、永久设置（修改配置文件）

```bash
vi /etc/network/interfaces
```

### 配置内容

```
auto eth0
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8
```

---

## 三、重启网络

```bash
/etc/init.d/networking restart
```

或

```bash
systemctl restart networking
```

---

## 四、参数说明

| 字段 | 作用 |
|------|------|
| `auto eth0` | 开机自动启用 eth0 |
| `iface eth0 inet static` | 使用静态 IP |
| `address` | IP 地址 |
| `netmask` | 子网掩码 |
| `gateway` | 默认网关 |
| `dns-nameservers` | DNS 服务器 |
