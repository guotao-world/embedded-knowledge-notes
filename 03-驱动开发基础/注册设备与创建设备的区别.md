# 注册设备与创建设备的区别

## 一、设备号（dev_t）

在 Linux 字符设备体系中，设备节点（`/dev/xxx`）最终一定对应一个 `dev_t`（主设备号 + 次设备号）。

**VFS 识别字符设备的唯一索引就是 dev_t，没有 dev_t，就没有路由入口。**

> 很多"被别的驱动调用的驱动"本来就不应该有设备节点，也不需要设备号（dev_t）。

### 关键判断标准（非常重要）

Linux 里驱动是否需要 dev_t（设备号），本质只看一件事：

> **是否需要"用户空间访问入口"**

### 个人理解

- 理论上系统设计不使用 dev_t 也可以，但是使用 dev_t 可以解耦得更完全且更准确。
- 只构建设备号以及创建设备节点，不注册设备 `cdev_add` 与不构建类，不考虑驱动运行，加载模块时会报错吗？**模块"加载阶段"一般不会报错。** 内核通常不会因为你少写 `cdev_add()` 或 `class_create()` 就拒绝加载模块。

---

## 二、cdev_add()：注册"字符设备能力"

```c
cdev_init(&icm20608dev.cdev, &icm20608_ops);
cdev_add(&icm20608dev.cdev, icm20608dev.devid, ICM20608_CNT);
```

它做的事情是：**把"驱动能力"注册进内核字符设备子系统。**

核心作用：

- 告诉内核："这个 major:minor 对应的设备，有这些 file_operations"
- 建立映射关系：

```
设备号（dev_t） ──→ file_operations（open/read/write/ioctl）
```

---

## 三、device_create()：创建设备"节点 + 设备模型对象"

> 创建 `/dev/` 设备节点不是必须创建类，但是创建类以后可以通过设备模型自动创建节点，更方便。

```c
device_create(icm20608dev.class, NULL, icm20608dev.devid, NULL, ICM20608_NAME);
```

它做的事情是：**向 Linux 设备模型 + sysfs + udev 提供信息。**

具体做三件关键事：

### 1. 创建 sysfs 设备对象

路径类似：

```
/sys/class/icm20608/icm20608
```

### 2. 通知 udev（用户态守护进程）

```
kernel → netlink → udev
```

udev 监听后自动执行：**创建 /dev 设备节点**

### 3. 最终生成

```
/dev/icm20608
```

---

## 四、对比总结

| 操作 | 作用层级 | 核心作用 |
|------|---------|---------|
| `register_chrdev_region()` | 设备号 | 申请/保留 dev_t 范围 |
| `cdev_init()` + `cdev_add()` | 内核字符设备子系统 | 绑定 dev_t 与 file_operations |
| `class_create()` | 设备模型 | 创建设备类（sysfs 容器） |
| `device_create()` | 设备模型 + udev | 创建设备对象，触发 udev 生成 `/dev/xxx` |
