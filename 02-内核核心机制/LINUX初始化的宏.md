# LINUX初始化的宏

**initcall 的实现机制**

**在内核编译时，所有被\*\_initcall标记的函数指针被放入一个特殊的ELF 段（如.initcall2.init）。**

**内核启动时，do_initcalls()会遍历这些段，按等级从小到大顺序调用每个函数指针。**

**也就是说：**

-   **postcore_initcall→ 放入.initcall2.init段**
-   **subsys_initcall→ 放入.initcall4.init段**
-   **启动时先执行段 2，后执行段 4。**

```c
/* initcalls are now grouped by functionality into separate
* subsections. Ordering inside the subsections is determined
* by link order.
* For backwards compatibility, initcall() puts the call in
* the device init subsection.
*
* The `id' arg to __define_initcall() is needed so that multiple initcalls
* can point at the same handler without causing duplicate-symbol build errors.
*/
#define __define_initcall(fn,id) \
static initcall_t __initcall_##fn##id __used \
__attribute__((__section__(".initcall"#id".init")))=fn; \
LTO_REFERENCE_INITCALL(__initcall_##fn##id)
/*
* Early initcalls run before initializing SMP.
*
* Only for built-in code, not modules.
*/
#define early_initcall(fn) __define_initcall(fn,early)
/*
* A "pure" initcall has no dependencies on anything else, and purely
* initializes variables that couldn't be statically initialized.
*
* This only exists for built-in code, not for modules.
* Keep main.c:initcall_level_names[] in sync.
*/
#define pure_initcall(fn) __define_initcall(fn,0)
#define core_initcall(fn) __define_initcall(fn,1)
#define core_initcall_sync(fn) __define_initcall(fn,1s)
#define postcore_initcall(fn) __define_initcall(fn,2)
#define postcore_initcall_sync(fn) __define_initcall(fn,2s)
#define arch_initcall(fn) __define_initcall(fn,3)
#define arch_initcall_sync(fn) __define_initcall(fn,3s)
#define subsys_initcall(fn) __define_initcall(fn,4)
#define subsys_initcall_sync(fn) __define_initcall(fn,4s)
#define fs_initcall(fn) __define_initcall(fn,5)
#define fs_initcall_sync(fn) __define_initcall(fn,5s)
#define rootfs_initcall(fn) __define_initcall(fn,rootfs)
#define device_initcall(fn) __define_initcall(fn,6)
#define device_initcall_sync(fn) __define_initcall(fn,6s)
#define late_initcall(fn) __define_initcall(fn,7)
#define late_initcall_sync(fn) __define_initcall(fn,7s)
#define __initcall(fn) device_initcall(fn)
#define __exitcall(fn) \
static exitcall_t __exitcall_##fn##__exit_call = fn
#define console_initcall(fn) \
static initcall_t __initcall_##fn\
__used __section(.con_initcall.init)=fn
#define security_initcall(fn) \
static initcall_t __initcall_##fn\
__used __section(.security_initcall.init)=fn
struct obs_kernel_param{const char*str;int(*setup_func)(char*);int early;};
```