# Linux 总线驱动模型设备创建顺序

## 一、设备创建顺序（以 I2C 为例）

```
1. DTS 解析 → device_node（只是描述）
2. I2C controller driver 注册 → i2c_adapter 出现
3. i2c-core 扫描 device_node
4. 创建 i2c_client（真正设备）
5. match driver → probe
```

---

## 二、谁把 reg 填到 client->addr？

在内核里是 I2C 核心代码（不是你写的驱动），核心函数路径大致是：

```
of_i2c_register_devices()
    ↓
of_i2c_get_board_info()
    ↓
info.addr = reg
    ↓
i2c_new_device()
    ↓
client->addr = info.addr
```

### 遍历子节点宏

```c
#define for_each_available_child_of_node(parent, child) \
    for (child = of_get_next_available_child(parent, NULL); \
         child; \
         child = of_get_next_available_child(parent, child))
```

---

## 三、bus 总线核心职能

| 角色 | 核心职能 |
|------|---------|
| **bus** | 1. match（判断 device 和 driver 是否匹配）<br>2. 提供统一管理机制（pm / uevent / sysfs） |
| **driver** | 1. probe（初始化设备）<br>2. remove（释放资源） |
| **driver core** | 在 match 成功后调用 probe/remove |

> bus 的职责是定义"匹配规则"，probe 永远属于 driver，由 driver core 在 match 成功后统一调用。

> 不是所有 bus 都"只做 match/probe/remove"，而是所有 bus 都至少做这三件事，但很多 bus 还做更多（尤其 PCI / USB）。

---

## 四、spi_sync / spi_async 这类函数

不是放在 bus 结构体里的，也不是"只在头文件中"。它们是 SPI core 提供的"对外 API"，实现写在 `spi.c` 中。

---

## 五、设备模型 vs 设备树

| 概念 | 本质 | 特点 |
|------|------|------|
| **设备模型（Driver Model）** | Linux 内核运行时模型（核心机制） | 逻辑关系模型，bus 平级注册 |
| **设备树（Device Tree）** | 硬件描述数据（静态描述） | 硬件连接关系（拓扑） |

- bus 在 Linux device model 中是平级概念：platform / i2c / spi / usb / pci（并列 bus）
- `bus_register()` 只是在 Linux 内核里"注册一种总线类型"，不依赖任何硬件控制器
- bus = 软件抽象层（规则 + 组织方式）
- 总线下的设备是由相应的控制器驱动从设备树解析出来并创建的

### 设备树模型

```
device model（设备模型）
─────────────────────────────────────
bus（总线框架） platform / i2c / spi / usb / pci
─────────────────────────────────────
device（设备）  driver（驱动）
```

### 设备模型

```
Linux 设备模型
────────────────────────────────
bus framework 层
┌────┬────┬────┬─────────┐
│    │    │    │         │
platform i2c spi usb   pci
│    │    │    │
└──── device / driver binding ────┘
```

---

## 六、部分总线的区别

I2C 这种总线，本质上是"无自描述能力"的总线，所以必须依赖外部描述（DT/ACPI）。
