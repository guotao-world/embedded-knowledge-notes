# imx6ull芯片内核编译

**在内核中增加打印：**


**编译内核中的sound声卡：**

export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
cd workspace_imx6ull/kernel/sound/soc/generic/
make -C ../../../ -j16

**编译好的内核位置：**

cd ../../../arch/arm/boot/

**编译内核中的codec驱动：**

export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf-
export ARCH=arm
cd workspace_imx6ull/kernel/sound/soc/codecs/
make -C ../../../ -j16
cd ../../../arch/arm/boot/

**拷贝内核到emmc**

scp ../../../arch/arm/boot/zImage root@192.168.55.71:/run/media/mmcblk1p1/

**搜索文件中的字符串：**

grep -rn "你要找的字符" ./
grep -rn "bitclock-master" ../../