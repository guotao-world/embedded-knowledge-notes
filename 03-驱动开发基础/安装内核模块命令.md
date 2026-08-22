# 安装内核模块命令

## 一、命令对比

| 命令 | 作用 | 场景 |
|------|------|------|
| `insmod` | 原始加载器 | 开发调试用 |
| `depmod` | 构建依赖数据库 | 模块安装后执行 |
| `modprobe` | 生产级加载器 | 自动解析依赖 |
| `rmmod` | 卸载模块 | 移除已加载模块 |

---

## 二、depmod 说明

`depmod` 默认不是固定更新 `/lib/modules` 下某一个目录，而是更新当前运行内核对应的模块目录。

使用 `uname -r` 查看当前内核版本名称：

```bash
depmod $(uname -r)
```

---

## 三、没有 depmod 时

```
modprobe → 找不到 modules.dep → 无法解析依赖
```

所以在拷贝新的 `.ko` 文件到 `/lib/modules/$(uname -r)/` 后，必须先执行 `depmod`，再用 `modprobe` 加载。

---

## 四、典型流程

```bash
# 1. 拷贝模块
scp chrdevbase.ko root@192.168.55.71:/lib/modules/4.19.232/

# 2. 构建依赖
depmod

# 3. 加载（自动处理依赖）
modprobe chrdevbase

# 4. 卸载
modprobe -r chrdevbase
```
