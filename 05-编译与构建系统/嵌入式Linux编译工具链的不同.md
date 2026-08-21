# 嵌入式Linux编译工具链的不同

**示例：**

**应用：**

aarch64-linux-gnu-gcc

需要一些依赖库，例如libc、libpthread、libm、Qt、ALSA、OpenCV。

注意：交叉编译器通常使用构建根文件系统的编译器，有的编译器会自动添加 sysroot，添加sysroot的作用是为了使用开发板里面的根文件系统的 ARM64 库

**内核：**

aarch64-none-linux-gnu-gcc

"none"表示：不依赖具体操作系统环境。

**Q:为什么kernel不用应用那个gcc？**

**A:实际上可以用。**也可能成功。Linux kernel并不严格要求必须none。但是Rockchip选择aarch64-none-linux-gnu。

**原因是：**

1.  **更纯净**Kernel不需要glibc。

2.  **和bootloader统一**U-Boot也使用类似工具链。

3.  3.

4.  **避免应用库干扰**

5.  用户空间工具链里面可能

6.  