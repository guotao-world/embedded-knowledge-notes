# Git 使用方法

## 一、基本配置

```bash
git config --global user.name "windows-pc"
git config --global user.email "xxxxxxx@xxxxxxx.com"
```

> 注意：这个邮箱很重要，在 GitHub 上是使用邮箱确定的 GitHub 账号，从而显示这个账号绑定的贡献者。

---

## 二、常用指令

### 克隆仓库

```bash
git clone https://github.com/guotao-lab/test.git
```

### 修改文件

```bash
vim Makefile
```

### 查看状态

```bash
git status
```

### 加入暂存区

```bash
# 指定文件
git add Makefile

# 或将所有有变化的内容加入暂存区
git add .
```

### 创建提交

```bash
git commit -m "update Makefile"
```

### 推送到远程

```bash
# 指定某个分支上传
git push origin main

# 让 Git 根据当前分支的配置自动决定推送到哪里
# 如果上一条指令加了 -u，则相当于配置好了 upstream 路径，之后可以直接 git push
git push -u origin main
git push
```

---

## 三、创建版本（Tag）

> 顺序：先提交（commit），再打标签（tag），再 push。

### 创建版本号

```bash
git tag v1.0.0
```

### 查看标签

```bash
git tag
```

### 推送标签

```bash
git push origin v1.0.0
```

### 既推送代码，也推送标签

```bash
git push origin main --tags
```

---

## 四、其他指令

### 查看远程仓库地址

```bash
git remote -v
```

### 修改 Git 代理

```bash
git config --global --list
git config --global http.proxy http://127.0.0.1:7897
git config --global https.proxy http://127.0.0.1:7897
```

### 检查配置来源

```bash
git config --show-origin --list
```

---

## 五、常规使用流程

```
① clone
   git clone xxx

② 创建分支
   git switch -c feature/rk3568-codec

③ 写代码
   codec.c
   device-tree.dts
   Kconfig
   Makefile

④ 编译
   make

⑤ 测试
   烧录 RK3568 → 启动 Linux → 测试 ALSA → aplay / arecord

⑥ 查看修改
   git diff

⑦ commit
   git add .
   git commit -m "ASoC: add xxx codec support"

⑧ push
   git push -u origin feature/rk3568-codec

⑨ 创建 MR
   feature/rk3568-codec → MR → main

⑩ 同事 Review

⑪ 修改

⑫ Review 通过

⑬ Merge

⑭ CI 自动编译/测试
```

---

## 六、常见问题

### Q：分支与仓库的关系？

**A：** Branch 不是独立存在的，它属于某一个 Git Repository。

### Q：为什么必须 Fork？

**A：** 严格来说不是必须 Fork。只有在一种典型情况下需要 Fork——你没有原仓库的写权限。

### Q：远程仓库比本地新怎么办？GitHub上的 main 分支已经有新的提交，但是你的本地没有。

**A：** 解决方法：先拉取远程代码，自动合并成功。或出现冲突，查看**git status**，解决冲突后add、commit、push。如果你确定远程内容不要了，可以强制覆盖 GitHub指令为git push -f origin main

开源项目非常经典的模式：

```
Fork → Clone → Branch → Commit → Push → PR
```
