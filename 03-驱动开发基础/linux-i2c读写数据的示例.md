# Linux I2C 读写数据的示例

## 一、示例一（标准方式：I2C_RDWR）

使用 `ioctl(fd, I2C_RDWR, &msgset)` 一次完成"写寄存器地址 + 读数据"的组合操作。

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>

int main()
{
    int fd;
    fd = open("/dev/i2c-1", O_RDWR);
    if (fd < 0) {
        perror("open");
        return -1;
    }

    unsigned char reg = 0x10;
    unsigned char data;
    struct i2c_msg msgs[2];
    struct i2c_rdwr_ioctl_data msgset;

    // 第1条消息：写寄存器地址
    msgs[0].addr = 0x50;
    msgs[0].flags = 0;
    msgs[0].len = 1;
    msgs[0].buf = &reg;

    // 第2条消息：读数据
    msgs[1].addr = 0x50;
    msgs[1].flags = I2C_M_RD;
    msgs[1].len = 1;
    msgs[1].buf = &data;

    msgset.msgs = msgs;
    msgset.nmsgs = 2;

    if (ioctl(fd, I2C_RDWR, &msgset) < 0) {
        perror("ioctl I2C_RDWR");
        return -1;
    }

    printf("data = 0x%02x\n", data);
    close(fd);
    return 0;
}
```

---

## 二、示例二（普通方式：write + read）

先通过 `I2C_SLAVE` 设置从机地址，再用 `write` / `read` 单独操作。

### 写数据

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>

int main()
{
    int fd;
    fd = open("/dev/i2c-1", O_RDWR);
    if (fd < 0) {
        perror("open");
        return -1;
    }

    // 设置从机地址
    if (ioctl(fd, I2C_SLAVE, 0x50) < 0) {
        perror("ioctl");
        return -1;
    }

    unsigned char buf[2];
    buf[0] = 0x10;   // 寄存器地址
    buf[1] = 0x55;   // 数据

    if (write(fd, buf, 2) != 2) {
        perror("write");
        return -1;
    }

    close(fd);
    return 0;
}
```

### 读数据

```c
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>

int main()
{
    int fd;
    fd = open("/dev/i2c-1", O_RDWR);
    if (fd < 0) {
        perror("open");
        return -1;
    }

    if (ioctl(fd, I2C_SLAVE, 0x50) < 0) {
        perror("ioctl");
        return -1;
    }

    unsigned char reg = 0x10;
    unsigned char data;

    // 先写寄存器地址
    if (write(fd, &reg, 1) != 1) {
        perror("write reg");
        return -1;
    }

    // 再读数据
    if (read(fd, &data, 1) != 1) {
        perror("read");
        return -1;
    }

    printf("data = 0x%02x\n", data);
    close(fd);
    return 0;
}
```

---

## 三、两种方式对比

| 方式 | 优点 | 缺点 |
|------|------|------|
| `I2C_RDWR` | 一次 ioctl 完成组合事务，原子性好 | 代码稍复杂 |
| `write` + `read` | 代码简单直观 | 两次调用之间可能被其他设备打断 |
