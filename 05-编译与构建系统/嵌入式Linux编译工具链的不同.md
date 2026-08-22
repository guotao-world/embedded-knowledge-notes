# 嵌入式 Linux 编译工具链的不同

## 一、应用层工具链

```
aarch64-linux-gnu-gcc
```

需要一些依赖库，例如：`libc`、`libpthread`、`libm`、`Qt`、`ALSA`、`OpenCV`。

> 注意：交叉编译器通常使用构建根文件系统的编译器，有的编译器会自动添加 sysroot。添加 sysroot 的作用是为了使用开发板里面的根文件系统的 ARM64 库。

---

## 二、内核工具链

```
aarch64-none-linux-gnu-gcc
```

`"none"` 表示：不依赖具体操作系统环境。

---

## 三、为什么 kernel 不用应用那个 gcc？

**实际上可以用，也可能成功。** Linux kernel 并不严格要求必须 none。但是 Rockchip 选择 `aarch64-none-linux-gnu`。

原因：

1. **更纯净**：Kernel 不需要 glibc
2. **和 bootloader 统一**：U-Boot 也使用类似工具链
3. **避免应用库干扰**：用户空间工具链里面可能带有应用层库的默认配置

---

## 四、对比总结

| 工具链 | 目标 | 依赖 | 典型用途 |
|--------|------|------|---------|
| `aarch64-linux-gnu-gcc` | 用户空间应用 | glibc 等系统库 | 应用程序、Qt、ALSA 应用 |
| `aarch64-none-linux-gnu-gcc` | 裸机/内核 | 无操作系统依赖 | 内核、U-Boot、裸机程序 |
