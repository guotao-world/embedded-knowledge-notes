# 编译imx6ull linux应用app

**环境安装：**

1.  **下载**：去[Linaro官网]{.underline}下载适合64位系统的版本，比如gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabihf.tar.xz。

2.  **解压**（假设放到/usr/local/arm）：

sudo mkdir -p /usr/local/arm
sudo tar -xvf gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabihf.tar.xz -C /usr/local/arm/

**3. 配置并验证环境变量**

为了让编译器随时可用，将bin目录加入环境变量。

export PATH=$PATH:/usr/local/arm/gcc-linaro-7.5.0-2019.12-x86_64_arm-linux-gnueabihf/bin

**永久加入环境变量（为了省事可以加入/etc/profile）：**

**~/.bashrc**（用户级，你检查过了，没有添加）

**~/.profile**或**~/.bash_profile**（用户级登录脚本）

**/etc/profile**和**/etc/environment**（系统级全局配置）

**AI建议：不要动~/.profile**（因为它是系统级敏感配置，容易影响桌面环境）。**直接在~/.bashrc末尾添加**（最稳妥，只影响终端）：

![](../images/image11.png)

**4.生效并验证：**

arm-linux-gnueabihf-gcc -v

**5.若使用makefile则需：**

export ARCH=arm
export CROSS_COMPILE=arm-linux-gnueabihf-
export PATH=$PATH:/your/toolchain/bin

**编译app标准指令：**

${CC} -o testApp testApp.c -Ixxx -Lyyy -lzzz

xxx 表示头文件的路径，yyy表示库文件的路径，zzz表示链接库。

**编译示例：**

arm-linux-gnueabihf-gcc hello.c -o hello
arm-linux-gnueabihf-gcc -std=gnu99 --sysroot=/opt/fsl-imx-x11/4.1.15-2.1.0/sysroots/cortexa7hf-neon-poky-linux-gnueabi -o playAndRecoed playAndRecoed.c -lpthread -lasound

**使用ssh拷贝到开发板：**

scp helloworld root@192.168.55.71:/home/root/
scp audioApp root@192.168.55.71:/home/root/
scp playAndRecoed root@192.168.55.71:/home/root/

**在开发板上执行：**

chmod +x audioApp
./audioApp

**使用file命令查看文件属性，确认它确实是ARM架构的：**

file helloworld