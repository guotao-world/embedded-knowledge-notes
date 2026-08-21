# linux音频驱动编译调试流程 alsa编译调试

**查看声卡：**

cat /proc/asound/cards
aplay -l

**查看参数：**

aplay --dump-hw-params -D hw:0,0
arecord --dump-hw-params -D hw:0,0

在源代码中搜索关键字：

grep -rn "dai-tdm-slot" sound/soc/

**播放一个 8k wav：**

aplay MIX1.wav
aplay -D hw:0,0 MIX1.wav

**播放裸 PCM：**

aplay -D hw:0,0 -r 8000 -f S16_LE -c 2 -t raw test.pcm

**录音测试：**

arecord -D hw:0,0 -r 8000 -f S16_LE -c 2 -d 5 test.wav

**各参数：**

-   -D hw:0,0：card0 device0
-   -r 8000：8kHz
-   -f S16_LE：16bit little endian
-   -c 2：双声道
-   -t raw：裸 PCM

**查看设备树：**

ls /proc/device-tree
cat /proc/device-tree/model

**查看声卡：**

cat /proc/asound/cards

**查看设备树的更新时间：**

ls -l /run/media/mmcblk0p1/

**alsa简单声卡支持（编译内核选项**

make menuconfig
Device Drivers
-> Sound card support
-> Advanced Linux Sound Architecture -> ALSA for SoC audio support -> ASoC Simple sound card support

**验证声卡(simple-card)：**uname -acat /proc/asound/cardscat /proc/device-tree/sound/compatiblecat /proc/device-tree/sound/simple-audio-card,namels /proc/device-tree/sound/dmesg | grep -i sounddmesg | grep -i asocdmesg | grep "my-codec"dmesg | grep "asoc"
dmesg | grep " asoc-simple-card"

**MD5校验：Ubuntu：**md5sum ../../../arch/arm/boot/zImagessh root@192.168.55.71 md5sum /run/media/mmcblk1p1/zImage**开发板:**md5sum /run/media/mmcblk1p1/zImage

**在编译了的内核中查找某个字符串：**strings ../../../arch/arm/boot/zImage | grep "probe"grep -a "my dummy codec probe" ../../../arch/arm/boot/zImage

**编译内核中的sound声卡：**export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- export ARCH=armcd workspace_imx6ull/kernel/sound/soc/generic/make -C ../../../ -j16cd ../../../arch/arm/boot/**编译codec驱动：**export CROSS_COMPILE=/usr/local/arm/gcc-linaro-4.9.4-2017.01-x86_64_arm-linux-gnueabihf/bin/arm-linux-gnueabihf- export ARCH=armcd workspace_imx6ull/kernel/sound/soc/codecs/make -C ../../../ -j16cd ../../../arch/arm/boot/**拷贝内核到emmc**scp ../../../arch/arm/boot/zImage root@192.168.55.71:/run/media/mmcblk1p1/