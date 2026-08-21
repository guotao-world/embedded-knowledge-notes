# imx6ull linux驱动makefile模板

```makefile
# 内核源码路径
KERNELDIR := /home/zhangxin/workspace_imx6ull/kernel
# 当前模块源码路径
CURRENT_PATH :=$(shell pwd)
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
$(MAKE)-C$(KERNELDIR)M=$(CURRENT_PATH)ARCH=$(ARCH)CROSS_COMPILE=$(CROSS_COMPILE)modules
# 清理模块
clean:
$(MAKE)-C$(KERNELDIR)M=$(CURRENT_PATH)ARCH=$(ARCH)CROSS_COMPILE=$(CROSS_COMPILE)clean
```