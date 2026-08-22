# Linux 源码顶层结构

```
linux/
├── arch/           # 架构相关（ARM / x86 / RISC-V）
├── drivers/        # 所有设备驱动（核心）
├── include/        # 头文件
├── kernel/         # 内核核心调度（进程/调度）
├── mm/             # 内存管理
├── fs/             # 文件系统
├── net/            # 网络协议栈
├── ipc/            # 进程间通信
├── lib/            # 通用库
├── init/           # 内核启动入口
├── scripts/        # 构建系统
├── Documentation/  # 文档
├── sound/          # 音频子系统（ALSA/ASoC）
├── crypto/         # 加密算法
├── security/       # 安全模块
├── block/          # 块设备层
└── firmware/       # 固件
```

---

## 关键目录说明

| 目录 | 作用 |
|------|------|
| `arch/arm` | ARM 32 位架构相关代码（启动、异常向量、平台代码） |
| `arch/arm64` | ARM 64 位架构相关代码 |
| `drivers/` | 所有设备驱动（gpio、i2c、spi、sound 等） |
| `include/linux` | 内核通用头文件 |
| `kernel/` | 调度、进程管理、定时器等核心 |
| `mm/` | 内存管理（页表、slab、vmalloc 等） |
| `init/main.c` | `start_kernel()` 内核启动入口 |
| `scripts/` | kbuild 构建脚本、设备树编译器 dtc 等 |
