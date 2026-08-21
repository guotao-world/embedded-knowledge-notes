# static关键字与const关键字

-   const 表示只读输入
-   static 表示仅当前文件使用（如果确实如此）

这两个警告都是合理的，不是为了"代码好看"，而是为了提高接口的安全性和可维护性。

在 Linux 内核、DSP 算法库、ALSA 驱动里，经验上有个规则：

能加 const 就加 const

能加 static 就加 static

**static关键字**

![](../images/image7.png)

**const关键字：**

shortcheck_frameData_changed(constshort*data,shortlen)

意思是：

我承诺不会修改调用者的数据。

**const修饰指针指向的数据**

cons tint*p;

或者：

int const*p;

两者完全一样。

意思：

可以修改 p

不能修改 *p

例如：

inta=10;
intb=20;
constint*p=&a;
p=&b;// √ 可以
*p=100;// × 错误

**const short *data**

**的含义表示：**

函数不能修改 data 指向的数据

但可以移动 data

**const修饰指针本身**

**int* const p=&a;**

意思：

不能修改 p

可以修改 *p