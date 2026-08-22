# YML 文件讲解

![GitHub Actions YML](../images/image2.png)

---

## 一、关键字段说明

| 字段 | 含义 |
|------|------|
| `name: Makefile CI` | CI 代表持续集成（Continuous Integration） |
| 符号 `-` | 同一类成员分组，只有一组时可以省略 |
| `build:` | 定义了一个任务 |
| `runs-on: ubuntu-latest` | 给开一台虚拟机 |
| `steps` | 步骤，按照后面的序列执行 |
| `if: startsWith(github.ref, 'refs/tags/')` | 表示必须有 tag 触发 |
| `env: GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}` | GitHub Actions 自动提供一个 token，允许 Action 创建 release、上传文件、修改仓库内容，不用手动生成 |
| `uses: actions/checkout@v4` | 调用别人已经写好的 GitHub Action 插件，不用自己写"创建 Release、上传附件"的脚本 |

---

## 二、run 与 use 的区别

| 关键字 | 作用 |
|--------|------|
| `run` | 在 Ubuntu 虚拟机里面执行命令 |
| `uses` | 加载一个别人写好的自动化模块 |

> GitHub Action 本质上就是一个自动化脚本包。
