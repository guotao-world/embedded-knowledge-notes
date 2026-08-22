# 设备树解析流程

## 一、注意事项

- `/sys` 和 `/proc` 都只是"展示"，真正被驱动使用的是内核已经展开好的 `device_node` 树
- `mx_pinctrl_parse_groups()` 它解析的是 `struct device_node`（内核内存中的设备树结构）
- `/sys/firmware/devicetree` 和 `/proc/device-tree` 只是 device tree 的调试/兼容"视图层"，不是核心机制，可以在内核配置中关闭，但不能理解为可随意删除的运行时组件
- `unflatten_device_tree()` 完全不依赖任何驱动（包括 SoC 适配驱动）。它做的事情是：纯数据结构构建，不涉及硬件语义。本质就是把 DTB（二进制设备树）解析成内核的 `device_node` 树结构

---

## 二、解析流程

```
Bootloader (U-Boot)
        ↓
DTB 传入内核
        ↓
start_kernel()
        ↓
unflatten_device_tree()
    （位置：drivers/of/fdt.c）
        ↓
内核得到 device_node（核心节点）
        ↓
根据 device_node 创建用户接口映射（可选）：
    /sys/firmware/devicetree
    /proc/device-tree（兼容）
        ↓
driver probe（依赖 device_node）
        ↓
imx_pinctrl_parse_groups()
        ↓
pinctrl 生效（写寄存器）
```

---

## 三、关键阶段说明

| 阶段 | 函数 | 作用 |
|------|------|------|
| DTB 传入 | Bootloader 完成 | 将 DTB 地址通过寄存器或约定方式传给内核 |
| 解析 DTB | `unflatten_device_tree()` | 纯数据结构解析，DTB → device_node 树 |
| 视图层创建 | 可选 | 创建 `/sys/firmware/devicetree` 等调试接口 |
| 驱动使用 | `probe()` 中 | 驱动通过 `of_*` API 读取 device_node 中的属性 |
| 硬件配置 | 各子系统 | 如 pinctrl 解析后写寄存器配置引脚复用 |
