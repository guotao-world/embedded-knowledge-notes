# linux 定时器

## 一、软件定时器精准吗？

普通 `timer_list`（ms 级）并不精准，只保证不会早于设定时间。

有高精度定时器 `hrtimer`（us 级），实际上可能也有几十 μs 延迟。

---

## 二、Linux 定时器模板

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/timer.h>
#include <linux/jiffies.h>

static struct timer_list test_timer;

/*
 * 定时器回调函数
 */
static void timer_callback(struct timer_list *timer)
{
    printk(KERN_INFO "timer callback!\n");

    /*
     * 周期性启动定时器
     * 1秒后再次进入 callback
     */
    mod_timer(&test_timer,
              jiffies + msecs_to_jiffies(1000));
}

/*
 * 模块加载函数
 */
static int __init timer_test_init(void)
{
    printk(KERN_INFO "timer init\n");

    /*
     * 初始化 timer
     * timer_callback: 定时器超时后调用的函数
     * 0: flags
     */
    timer_setup(&test_timer, timer_callback, 0);

    /*
     * 启动定时器
     * 当前时间 + 1000ms
     */
    mod_timer(&test_timer, jiffies + msecs_to_jiffies(1000));

    return 0;
}

/*
 * 模块卸载函数
 */
static void __exit timer_test_exit(void)
{
    printk(KERN_INFO "timer exit\n");

    /*
     * 删除定时器
     * 等待正在执行的 callback 结束
     */
    del_timer_sync(&test_timer);
}

module_init(timer_test_init);
module_exit(timer_test_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("test");
MODULE_DESCRIPTION("simple kernel timer example");
```

---

## 三、关键 API

| API | 作用 |
|-----|------|
| `timer_setup(timer, callback, flags)` | 初始化定时器 |
| `mod_timer(timer, expires)` | 启动/修改定时器，expires 为绝对 jiffies 值 |
| `del_timer(timer)` | 删除定时器（不等待回调） |
| `del_timer_sync(timer)` | 删除定时器（等待正在执行的回调结束） |
| `msecs_to_jiffies(ms)` | 毫秒转 jiffies |
| `jiffies` | 当前内核节拍计数 |

> 周期性定时器需要在 callback 中再次调用 `mod_timer()` 来重新启动。
