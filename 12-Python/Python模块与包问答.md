# Python 模块与包问答

> 进阶阶段的真实提问记录：学完异常处理与文件读写后，进入模块、包、pip、venv 的学习。
> 可运行示例代码在 [code/](code/) 目录。

---

## 目录

- 01 学完基础语法、面向对象、异常处理、文件读写之后，接下来学什么？
- 02 模块与包怎么学？
- 03 python -m 里的 -m 是什么意思？
- 04 pip 是什么的缩写？
- 05 怎么把代码打包成 pkg？
- 06 不打包，直接 import xxx.py 文件可以吗？

---

## 01 学完基础语法、面向对象、异常处理、文件读写之后，接下来学什么？

**问题：** 基础语法、面向对象、异常处理、文件读写都学完了，Python 接下来还需要学什么？

### 回答要点

"能写真实程序"三件套（异常处理、文件读写、模块与包）已完成 2/3，下一步学最后一块：**模块与包 + pip + venv**。

**模块/包：** 一个文件拆成多个，import 互相引用——代码不再全堆一个文件；
**pip：** 装第三方库（pip install xxx）——pyserial / paramiko 等嵌入式场景库都靠它；
**venv：** 每个项目独立环境，装的库互不污染。

再往后按顺序：标准库实战（json / re / subprocess / datetime）→ 装饰器 / 推导式 / *args **kwargs → 嵌入式按需（pyserial / paramiko / matplotlib）。

---

## 02 模块与包怎么学？

**问题：** 模块与包这个主题，有没有一份可以直接运行的学习代码？

### 回答要点

有。完整学习代码：[code/Python模块与包学习代码.py](code/Python模块与包学习代码.py)，共 9 节，全部可运行。配套文件：

- [code/mymod.py](code/mymod.py)：自建模块（被主文件 import）；
- [code/mypkg/](code/mypkg/)：自建包（目录 + __init__.py + math_tools.py）。

| 节 | 内容 |
|---|---|
| 1 | 为什么需要模块（单文件 vs 多文件） |
| 2 | 导入标准库 import math / os |
| 3 | import 的四种姿势（import / from import / as 别名 / import *） |
| 4 | 自建模块 import mymod |
| 5 | __name__ == "__main__" 是什么 |
| 6 | 包（package）：mypkg/math_tools.py |
| 7 | pip：装第三方库的命令（在终端里敲） |
| 8 | venv：虚拟环境命令（在终端里敲） |
| 9 | 综合小任务：os + 自建模块组合使用 |

### 核心要点

- **模块 = 一个 .py 文件**；**包 = 一个目录 + 若干模块**（目录名就是包名）；
- **import 本质**：在搜索路径里找到同名 .py 文件 → 执行它 → 使用里面的名字；
- **__name__ == "__main__"**：直接运行该文件时为 "__main__"（测试代码执行），被 import 时为模块名（测试代码不执行）；
- **查找顺序**：当前目录 → PYTHONPATH → 标准库 → site-packages（pip 装的库）。

---

## 03 python -m 里的 -m 是什么意思？

**问题：** python -m venv myenv 里的 -m 是什么？

### 回答要点

`-m` = **module**（模块），意思是：把后面的名字当作"模块"来运行，而不是当作"文件路径"来运行。

```bash
python 文件名.py        # 按"文件路径"找，运行这个文件
python -m 模块名        # 按"模块名"在 Python 的搜索路径里找，运行这个模块
```

**为什么官方推荐这么写？** 电脑上可能装了多个 Python 环境，直接敲 pip / venv 用的是 PATH 里碰巧排在前面的那个；`python -m pip` 保证用的是**当前这个 python 所属环境**的工具，不会装错地方。

```bash
python -m venv myenv              # 用当前 python 创建虚拟环境
python -m pip install pyserial    # 用当前 python 的 pip 装库
python -m http.server 8000        # 标准库模块：起一个本地网页服务器
```

**心法：** python -m xxx = "让当前这个 Python，把 xxx 当作模块跑一遍"。venv 和 math、os 一样都是标准库模块，只是它的功能是"创建环境"，平时当命令用。

---

## 04 pip 是什么的缩写？

**问题：** pip 是什么的缩写？

### 回答要点

pip 的官方解释是一个**递归缩写**：**Pip Installs Packages**（"pip 安装包"）——类似 GNU = "GNU's Not Unix" 的递归缩写风格。

通俗理解就是：**Python 的包管理器**，负责下载、安装、卸载别人写好的模块（pip install pyserial）。

两个背景：

- pip 是 2008 年 Ian Bicking 写的，替代更老的 easy_install；
- 最初叫 pyinstall，为避免和 PyInstaller（打包工具）混淆改名 pip。

现在也有人展开为 "Package Installer for Python"（Python 包安装器）——意思正确，但不是官方定义。

**心法：** pip = Python 装第三方模块的工具，pip install 库名 = 把别人的模块装进你的环境。

---

## 05 怎么把代码打包成 pkg？

**问题：** 怎么把自己写的代码打包成"包"（可安装分发的 pkg）？

### 回答要点

先区分两个"包"：

- **代码组织上的包** = 目录 + __init__.py（mypkg/ 就是），这层已会；
- **分发安装上的包** = 能通过 pip install 装进环境的项目，加一个 pyproject.toml 配置即可。

**最小打包流程：**

```
项目目录/
├── mypkg/               # 源码包
│   ├── __init__.py
│   └── math_tools.py
└── pyproject.toml       # 打包配置
```

pyproject.toml 最小可用版：

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "mypkg"
version = "0.1.0"
description = "My math tools package"

[tool.setuptools]
packages = ["mypkg"]
```

然后（在项目目录下）：

```bash
pip install -e .        # -e = 可编辑安装（开发用，改了源码立即生效）
python -c "from mypkg.math_tools import add; print(add(1, 2))"
```

**更进一步（分享给别人）：**

```bash
pip install build
python -m build         # 生成 dist/ 下的 .whl 和 .tar.gz
```

- .whl 文件（wheel）就是"成品安装包"，发给别人，对方 pip install xxx.whl 就能装；
- 发布到 PyPI（pip install twine upload）离学习阶段较远，个人 / 嵌入式场景用不上。

**建议：** 自己做项目，pip install -e . 就够了；PyPI 发布先不用学。

---

## 06 不打包，直接 import xxx.py 文件可以吗？

**问题：** 不打包，直接 import 一个 .py 文件可以吗？

### 回答要点

**可以**——import mymod 就是"不打包、直接 import 同目录 .py 文件"的实例。

**原理：** import xxx 的本质 = Python 在"模块搜索路径"里找到 xxx.py 文件 → 执行它 → 让你能用里面的名字。打包（pip install）只是把文件复制到"全系统都能搜到的目录"（site-packages），**不是 import 的前提**。

**搜索路径（sys.path）从上到下：**

| 位置 | 说明 |
|---|---|
| 当前脚本所在目录 | 同目录的 .py 直接 import 就中 |
| PYTHONPATH 环境变量 | 手动加的额外路径 |
| 标准库目录 | math、os 这些自带模块 |
| site-packages | pip 安装的第三方库 |

**什么时候才需要打包：**

- 同一个项目、同目录/子目录 → 直接 import，够了；
- 别的项目/别的机器也要用 → 打包装进 site-packages；
- 发布给别人用 → 打包 + 上 PyPI。

**两个直接 import 的小坑：**

- 文件名就是模块名，不能以数字开头（import 2file 报错），也别用关键字；
- 想 import 子目录里的文件：目录做成"包"（有 __init__.py），用 from mypkg import math_tools 更规范。

**心法：** 打包 = 让"不在旁边"的文件也能被 import；旁边放着的文件，直接 import 就好。
