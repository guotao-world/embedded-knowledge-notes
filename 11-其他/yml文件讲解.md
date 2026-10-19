# YML 文件讲解

## 一、YML 基础概念

YML（YAML Ain't Markup Language）是一种人类可读的数据序列化格式，GitHub Actions 工作流文件使用 YML 格式定义自动化任务。

### 关键字段说明

| 字段 | 含义 |
|------|------|
| `name: Makefile CI` | 工作流名称，CI 代表持续集成（Continuous Integration） |
| 符号 `-` | 同一类成员分组（列表项），只有一组时可以省略 |
| `build:` | 定义了一个任务（job） |
| `runs-on: ubuntu-latest` | 指定运行环境，给开一台 Ubuntu 虚拟机 |
| `steps` | 步骤列表，按照后面的序列依次执行 |
| `if: startsWith(github.ref, 'refs/tags/')` | 条件判断，表示必须有 tag 触发才执行 |
| `env: GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}` | 设置环境变量，GitHub Actions 自动提供一个临时 token |
| `uses: actions/checkout@v4` | 调用别人已经写好的 GitHub Action 插件 |

### run 与 uses 的区别

| 关键字 | 作用 |
|--------|------|
| `run` | 在 Ubuntu 虚拟机里面执行 Shell 命令 |
| `uses` | 加载一个别人写好的自动化模块（Action） |

> GitHub Action 本质上就是一个自动化脚本包，`uses` 相当于 import 一个现成的功能模块。

---

## 二、完整示例：自动更新 README 目录

以下是本仓库使用的 `.github/workflows/update-toc.yml`，每次 push 到 main 分支时自动扫描所有 md 文件并更新 README 目录。

```yaml
name: Update README TOC

# 监听 main 分支的 push 事件
on:
  push:
    branches:
      - main

# 权限配置：需要写入仓库内容（push 修改后的 README.md）
permissions:
  contents: write

jobs:
  update-toc:
    runs-on: ubuntu-latest

    steps:
      # 1. 检出仓库代码
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          # 获取完整历史，避免浅克隆导致的问题
          fetch-depth: 0
          # 持久化凭证，使后续 git push 能自动认证
          persist-credentials: true
          # 显式传入 token
          token: ${{ secrets.GITHUB_TOKEN }}

      # 2. 设置 Python 环境
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'

      # 3. 运行目录生成脚本
      - name: Generate TOC
        run: python scripts/generate_toc.py

      # 4. 检测 README.md 是否变化，如果有变化则提交
      - name: Commit and push if changed
        run: |
          set -e

          # 配置 git 用户
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"

          # 检查 README.md 是否有变化
          if git diff --quiet README.md; then
            echo "README.md 无变化，无需提交"
          else
            echo "README.md 有变化，正在提交..."
            git add README.md
            # 使用 [skip ci] 避免循环触发
            git commit -m "update README toc [skip ci]"
            # 明确推送到 main 分支
            git push origin main
            echo "README.md 已提交并推送"
          fi
```

---

## 三、逐段代码说明

### 1. name — 工作流名称

```yaml
name: Update README TOC
```

工作流的显示名称，会出现在 GitHub Actions 页面的运行列表中。

### 2. on — 触发条件

```yaml
on:
  push:
    branches:
      - main
```

定义什么时候触发这个工作流：

- `push`：当有代码推送时触发
- `branches: - main`：只监听 main 分支的 push

其他常见触发方式：

| 触发方式 | 含义 |
|---------|------|
| `push` | 代码推送时 |
| `pull_request` | PR 创建或更新时 |
| `schedule` | 定时触发（cron 表达式） |
| `workflow_dispatch` | 手动触发 |
| `release` | Release 发布时 |

### 3. permissions — 权限配置

```yaml
permissions:
  contents: write
```

限制 `GITHUB_TOKEN` 的权限范围，最小权限原则：

| 权限 | 含义 |
|------|------|
| `contents: write` | 允许读写仓库内容（提交、推送） |
| `contents: read` | 只读仓库内容 |
| `pull-requests: write` | 允许操作 PR |
| `issues: write` | 允许操作 Issues |

> 不配置时使用仓库默认权限；显式配置更安全，避免 token 权限过大。

### 4. jobs — 任务定义

```yaml
jobs:
  update-toc:
    runs-on: ubuntu-latest
```

- `jobs`：工作流中的任务集合，可以有多个 job
- `update-toc`：job 的 ID（自定义）
- `runs-on: ubuntu-latest`：运行环境，可选 `ubuntu-latest`、`windows-latest`、`macos-latest`

多个 job 默认并行执行，可用 `needs` 关键字设置依赖顺序。

### 5. steps — 步骤详解

每个 job 由多个 step 组成，按顺序执行。

#### Step 1：检出代码

```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
    persist-credentials: true
    token: ${{ secrets.GITHUB_TOKEN }}
```

- `uses: actions/checkout@v4`：官方 Action，把仓库代码克隆到虚拟机
- `fetch-depth: 0`：获取完整 git 历史（默认只取最近 1 层，浅克隆可能导致 git push 失败）
- `persist-credentials: true`：保存 git 凭证，后续 `git push` 自动认证
- `token`：传入临时 token，`secrets.GITHUB_TOKEN` 是 GitHub 自动生成的，不是个人账户密码

#### Step 2：设置 Python

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.x'
```

官方 Action，安装指定版本的 Python。`3.x` 表示最新的 Python 3 版本。

#### Step 3：运行脚本

```yaml
- name: Generate TOC
  run: python scripts/generate_toc.py
```

`run` 关键字直接执行 Shell 命令。这里运行仓库中的 Python 脚本，自动扫描 md 文件并生成目录。

#### Step 4：提交并推送

```yaml
- name: Commit and push if changed
  run: |
    set -e
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    if git diff --quiet README.md; then
      echo "README.md 无变化，无需提交"
    else
      git add README.md
      git commit -m "update README toc [skip ci]"
      git push origin main
    fi
```

逐行说明：

| 代码 | 作用 |
|------|------|
| `run: \|` | 多行脚本，`\|` 表示保留换行 |
| `set -e` | 任何命令出错立即退出，避免错误被忽略 |
| `git config user.name` | 设置提交者名称（bot 身份） |
| `git diff --quiet README.md` | 检查 README 是否有变化，无变化返回 0 |
| `git commit -m "..."` | 提交，`[skip ci]` 让这次提交不触发工作流，避免无限循环 |
| `git push origin main` | 推送到 main 分支，必须明确指定分支 |

---

## 四、常见问题

### Q: `${{ secrets.GITHUB_TOKEN }}` 会泄漏账户吗？

不会。这是 GitHub 自动生成的**临时 token**：
- 每次工作流运行时自动创建，结束后失效
- 权限受 `permissions` 字段限制
- GitHub 会自动在日志中屏蔽，不会打印出来
- 不是你的个人账户密码

### Q: 为什么 `git push` 要写 `origin main`？

不写分支时，git 可能因为默认推送策略不同而失败。明确写 `git push origin main` 最稳妥。

### Q: `[skip ci]` 有什么用？

工作流提交 README 后，如果不加 `[skip ci]`，这次 push 又会触发工作流，导致无限循环。GitHub 识别到 commit message 中包含 `[skip ci]` 时会跳过运行。

### Q: `fetch-depth: 0` 为什么需要？

`actions/checkout` 默认只浅克隆最近 1 次提交（`fetch-depth: 1`），这会导致 `git push` 时缺少历史信息。设为 `0` 表示获取完整历史。
