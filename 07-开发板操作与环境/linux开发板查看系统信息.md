# Linux 开发板查看系统信息

## 一、查看 CPU 信息

```bash
cat /proc/cpuinfo
```

## 二、查看内存信息

```bash
cat /proc/meminfo
free -h
```

## 三、查看磁盘信息

```bash
df -h
lsblk
```

## 四、查看内核版本

```bash
uname -a
```

## 五、查看系统版本

```bash
cat /etc/os-release
cat /etc/issue
```

## 六、查看运行时间和负载

```bash
uptime
```

## 七、查看进程

```bash
top
ps aux
```

## 八、查看中断

```bash
cat /proc/interrupts
```

---

## 九、常用命令速查

| 命令 | 作用 |
|------|------|
| `cat /proc/cpuinfo` | CPU 型号、核心数、频率 |
| `free -h` | 内存使用情况 |
| `df -h` | 磁盘使用情况 |
| `uname -a` | 内核版本、架构 |
| `uptime` | 运行时间、负载 |
| `cat /proc/interrupts` | 中断统计 |
