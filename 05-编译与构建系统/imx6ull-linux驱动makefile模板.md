# imx6ull Linux 驱动 Makefile 模板

```makefile
# 内核源码路径
KERNELDIR := /home/zhangxin/workspace_imx6ull/kernel

# 当前模块源码路径
CURRENT_PATH := $(shell pwd)

# 交叉编译器前缀（根据你实际工具链修改）
CROSS_COMPILE := arm-linux-gnueabihf-
ARCH := arm

# 模块列表
obj-m := led.o

# 默认目标
all: build

# 编译模块
build: kernel_modules

kernel_modules:
	$(MAKE) -C $(KERNELDIR) M=$(CURRENT_PATH) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) modules

# 清理模块
clean:
	$(MAKE) -C $(KERNELDIR) M=$(CURRENT_PATH) ARCH=$(ARCH) CROSS_COMPILE=$(CROSS_COMPILE) clean
```

---

## 关键字段说明

| 变量 | 作用 |
|------|------|
| `KERNELDIR` | 内核源码路径，必须是已编译过的内核源码树 |
| `CURRENT_PATH` | 当前模块源码所在路径 |
| `CROSS_COMPILE` | 交叉编译器前缀 |
| `ARCH` | 目标架构（arm / arm64 等） |
| `obj-m` | 要编译成模块的目标文件 |
| `M=` | 指定外部模块源码目录 |
| `modules` | 内核 make 目标，编译外部模块 |
