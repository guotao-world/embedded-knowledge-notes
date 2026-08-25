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
git clone https://github.com/guotao-world/test.git
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

### 强制推送到远程

```bash
# 回退版本后，强制推送到远程（覆盖历史）
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

## 四、本地项目推送到 GitHub 新仓库

### 4.1 操作步骤

在 GitHub 上创建空仓库后，把本地文件夹推上去：

```bash
# 1. 进入本地项目目录
cd F:\github_workspace\xxxxxxxx

# 2. 初始化 Git 仓库
git init

# 3. 添加所有文件到暂存区
git add .

# 4. 创建首次提交
git commit -m "initial commit"

# 5. 将默认分支重命名为 main
git branch -M main

# 6. 添加远程仓库地址
git remote add origin https://github.com/你的用户名/photography-knowledge-notes.git

# 7. 推送到远程并设置 upstream
git push -u origin main
```

### 4.2 常见问题：push 失败（仓库已含 README）

如果 GitHub 仓库创建时勾选了 **Add a README file**，远程仓库已经有一次提交，而本地仓库没有共同历史，直接 push 会失败。

**解决方法：** 先从远程拉取代码，允许合并两个没有共同历史起点的仓库，再推送。

```bash
# 从远程 main 分支拉取，允许合并不相关历史
git pull origin main --allow-unrelated-histories

# 拉取成功后再推送
git push
```

> **说明：** `--allow-unrelated-histories` 参数用于允许合并两个没有共同提交历史的 Git 仓库。正常情况下（如日常协作开发）不需要这个参数，只有在本地仓库和远程仓库各自独立创建时才需要。

---

## 五、使用 SSH 操作 GitHub 仓库 (window)

### 5.1 生成 SSH Key

查看是否已经存在 SSH Key：

```bash
dir %USERPROFILE%\.ssh
```

如果不存在，生成 SSH Key：

```bash
ssh-keygen -t ed25519 -C "你的GitHub邮箱"
```

示例：

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

生成后：

- **私钥：** `C:\Users\用户名\.ssh\id_ed25519`
- **公钥：** `C:\Users\用户名\.ssh\id_ed25519.pub`

> **注意：** `id_ed25519` 是私钥，不要泄露。`id_ed25519.pub` 是公钥，可以上传到 GitHub。

### 5.2 查看 SSH 公钥

Windows CMD：

```bash
type %USERPROFILE%\.ssh\id_ed25519.pub
```

复制输出内容：

```
ssh-ed25519 AAAAC3xxxxxxxxxxxxxxxx 用户名@电脑名
```

### 5.3 GitHub 添加 SSH Key

操作路径：

```
GitHub → Settings → SSH and GPG keys → New SSH key
```

填写：

- **Title：** 例如 `Windows-PC`
- **Key：** 粘贴刚才复制的公钥内容

点击 **Add SSH key**。

### 5.4 测试 SSH 连接

执行：

```bash
ssh -T git@github.com
```

第一次连接输入：

```
yes
```

成功显示：

```
Hi 用户名! You've successfully authenticated, but GitHub does not provide shell access.
```

说明 SSH 配置成功。

### 5.5 使用 SSH 克隆仓库

```bash
git clone git@github.com:xxxxxx/xxxxxx.git
```

之后就可以正常的 pull 及 push 了。

### 5.6 已有 HTTPS 仓库切换为 SSH

如果是已经通过 HTTPS 克隆完了的仓库，通过以下方式切换源：

```bash
# 查看当前远程地址
git remote -v

# 切换为 SSH 地址
git remote set-url origin git@github.com:xxxxxx/xxxxxx.git

# 验证切换结果
git remote -v
```

之后就可以正常的 pull 及 push 了。

---

## 六、其他指令

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

## 七、github常规使用流程

```
        原作者的 GitHub Repository
        original-user/repository
                  │
                  │ Fork
                  ↓
        我的 GitHub Repository
        my-user/repository
                  │
                  │ Clone
                  ↓
              我的电脑
                  │
                  │ 修改代码
                  ↓
              git commit
                  │
                  │ git push
                  ↓
        我的 GitHub Repository
        my-user/repository
                  │
                  │ Pull Request（PR）
                  ↓
        原作者的 GitHub Repository
        original-user/repository
                  │
                  │ 审核 / Merge
                  ↓
          原作者 Repository
          正式加入我的修改

```

---

## 八、常见问题

### Q：分支与仓库的关系？

**A：** Branch 不是独立存在的，它属于某一个 Git Repository。

### Q：Fork是什么？有什么作用？与clone的区别是什么？PR是什么？

**A：** Fork：把别人的 GitHub 仓库（Repository）复制一份到自己的 GitHub 账号下，同时保留与原仓库的关联关系，主要用于没有原仓库写权限时参与开源项目开发。 Clone：把 GitHub 上的仓库下载到自己的电脑，方便本地修改和开发。 PR（Pull Request）：向原仓库提交一个合并请求，请求项目维护者审核并把你的修改合并到原项目中。


### Q：远程仓库比本地新怎么办？GitHub上的 main 分支已经有新的提交，但是你的本地没有。

**A：** 解决方法：先拉取远程代码，自动合并成功。或出现冲突，查看**git status**，解决冲突后add、commit、push。如果你确定远程内容不要了，可以强制覆盖 GitHub指令为git push -f origin main

### Q：hard回退与soft回退有什么区别。

**A：** soft回退会保留工作区，可以修改commit信息后重新提交。hard回退不保留工作区，把commit、add、代码全部丢弃，hard 最危险，因为它会直接丢弃本地未保存修改。

### Q：git pull 表示什么？

**A：** 拉取远程更新，实际上等价于 `git fetch` + `git merge`。`--allow-unrelated-histories` 表示允许合并没有关联历史的两个 Git 仓库。

开源项目非常经典的模式：

```
Fork → Clone → Branch → Commit → Push → PR
```
