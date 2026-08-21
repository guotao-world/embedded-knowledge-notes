# linux定时器

**Q:软件定时器精准吗？**

**A：**普通 timer_list(ms级)并不精准，只保证不会早于设定时间。有高精度定时器hrtimer(us级)实际上可能也有几十 μs延迟

**linux定时器模板：**

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
* 1秒后再次进入callback
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
/* * 初始化timer * * timer_callback: * 定时器超时后调用的函数 * * 0: * flags */ timer_setup(&test_timer, timer_callback, 0);
/* * 启动定时器 * * 当前时间 + 1000ms */ mod_timer(&test_timer, jiffies + msecs_to_jiffies(1000));
return 0;}
/* * 模块卸载函数 */static void __exit timer_test_exit(void){ printk(KERN_INFO "timer exit\n");
/* * 删除定时器 * * 等待正在执行的callback结束 */ del_timer_sync(&test_timer);}
module_init(timer_test_init);module_exit(timer_test_exit);
MODULE_LICENSE("GPL");MODULE_AUTHOR("test");MODULE_DESCRIPTION("simple kernel timer example");
```