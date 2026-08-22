# 设备树的概念

## 一、核心概念

**设备树属于硬件描述机制，而非设备描述机制。而硬件包括设备，因此硬件描述的概念更广。**

设备树是一种硬件拓扑与资源描述机制，它描述的是 SoC/板级硬件结构；Linux 设备模型中的 device 只是设备树描述对象中的一部分。

设备树的范围比设备模型更广，因为它不仅描述设备，还描述 CPU、内存、时钟、复位、电源域、总线等硬件资源。

---

## 二、层次关系

```
Hardware Description (Device Tree)
        │
┌───────┼───────────────────┐
│       │                   │
Device Model  Resource Framework  Other Framework
│       │                   │
│       │                   │
platform/i2c/spi  clk/regulator  CPU/memory
        │
        │
      driver
        │
        │
     subsystem
        │
        │
   ALSA/GPIO/NET
```

---

## 三、设备树 vs 设备模型

| 概念 | 描述范围 | 典型内容 |
|------|---------|---------|
| **设备树（Device Tree）** | 硬件拓扑与资源 | CPU、内存、时钟、复位、电源域、总线、外设 |
| **设备模型（Device Model）** | 内核运行时的设备/驱动组织 | device、driver、bus、class |

设备树是"静态的硬件描述"，设备模型是"动态的内核运行时结构"。驱动在 probe 时从设备树读取硬件信息，然后创建设备模型对象。
