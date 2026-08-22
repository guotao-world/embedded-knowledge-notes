# LINUX 初始化的宏

## 一、initcall 的实现机制

在内核编译时，所有被 `*_initcall` 标记的函数指针被放入一个特殊的 ELF 段（如 `.initcall2.init`）。

内核启动时，`do_initcalls()` 会遍历这些段，按等级从小到大顺序调用每个函数指针。

也就是说：

- `postcore_initcall` → 放入 `.initcall2.init` 段
- `subsys_initcall` → 放入 `.initcall4.init` 段
- 启动时先执行段 2，后执行段 4

---

## 二、initcall 等级定义

```c
/* initcalls are now grouped by functionality into separate
 * subsections. Ordering inside the subsections is determined
 * by link order.
 * For backwards compatibility, initcall() puts the call in
 * the device init subsection.
 */
#define __define_initcall(fn, id) \
    static initcall_t __initcall_##fn##id __used \
    __attribute__((__section__(".initcall" #id ".init"))) = fn;

#define early_initcall(fn)      __define_initcall(fn, early)
#define pure_initcall(fn)       __define_initcall(fn, 0)
#define core_initcall(fn)       __define_initcall(fn, 1)
#define core_initcall_sync(fn)  __define_initcall(fn, 1s)
#define postcore_initcall(fn)   __define_initcall(fn, 2)
#define postcore_initcall_sync(fn) __define_initcall(fn, 2s)
#define arch_initcall(fn)       __define_initcall(fn, 3)
#define arch_initcall_sync(fn)  __define_initcall(fn, 3s)
#define subsys_initcall(fn)     __define_initcall(fn, 4)
#define subsys_initcall_sync(fn) __define_initcall(fn, 4s)
#define fs_initcall(fn)         __define_initcall(fn, 5)
#define fs_initcall_sync(fn)    __define_initcall(fn, 5s)
#define rootfs_initcall(fn)     __define_initcall(fn, rootfs)
#define device_initcall(fn)     __define_initcall(fn, 6)
#define device_initcall_sync(fn) __define_initcall(fn, 6s)
#define late_initcall(fn)       __define_initcall(fn, 7)
#define late_initcall_sync(fn)  __define_initcall(fn, 7s)

#define __initcall(fn) device_initcall(fn)
```

---

## 三、等级顺序

| 等级 | 宏 | 典型用途 |
|------|-----|---------|
| early | `early_initcall` | 最早期初始化，SMP 之前 |
| 0 | `pure_initcall` | 纯初始化，无依赖 |
| 1 | `core_initcall` | 核心子系统 |
| 2 | `postcore_initcall` | 核心之后的初始化 |
| 3 | `arch_initcall` | 架构相关初始化 |
| 4 | `subsys_initcall` | 子系统初始化（如 SPI 总线） |
| 5 | `fs_initcall` | 文件系统 |
| rootfs | `rootfs_initcall` | 根文件系统 |
| 6 | `device_initcall` | 设备驱动（最常用） |
| 7 | `late_initcall` | 后期初始化 |

> 带 `_sync` 后缀的版本会等待该等级所有非 sync 的 initcall 执行完毕后再执行。
