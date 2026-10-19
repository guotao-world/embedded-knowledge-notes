# Python 异常处理与文件读写问答

> 进阶阶段的真实提问记录：学完基础语法与面向对象后，下一步学什么、异常处理、文件读写。
> 可运行示例代码在 [code/](code/) 目录。

---

## 目录

- 01 基础语法和面向对象学完之后，接下来学什么？
- 02 异常处理和文件读写怎么学？
- 03 Python 有 catch 关键字吗？为什么不是 try catch？
- 04 为什么 except 能表示异常？它和 try 看起来没什么关联？

---

## 01 基础语法和面向对象学完之后，接下来学什么？

**问题：** 学完基础语法（变量、列表、字典、循环、函数）和面向对象（类、self、cls、类变量）之后，Python 接下来还需要学什么？

### 回答要点

接下来不是学"更多语法"，而是学"能写真实程序"的能力，分三个阶段：

**① 能写真实脚本（立刻学）**

- 异常处理 try/except：程序出错不崩溃、报错看得懂；
- 文件读写 + 路径操作（open / pathlib）：处理日志和配置文件；
- 模块与包 + pip + venv：import 机制、安装第三方库、隔离环境。

**② 写得好用（熟练后用）**

- 常用标准库：json / yaml / re / subprocess / datetime；
- 装饰器（@staticmethod 同源）、列表推导式、*args / **kwargs、lambda。

**③ 嵌入式场景按需学（用到再学）**

- pyserial 串口调试脚本；
- paramiko SSH 批量操作开发板；
- matplotlib 画波形 / 数据可视化。

### 提醒

Python 在嵌入式学习里是辅助工具，主战场是 C / 内核 / 驱动；每个主题学到"会用"就停，用到哪学到哪，效率最高。

---

## 02 异常处理和文件读写怎么学？

**问题：** 异常处理和文件读写这两个主题，有没有一份可以直接运行的学习代码？

### 回答要点

有。完整学习代码：[code/Python异常处理与文件读写学习代码.py](code/Python异常处理与文件读写学习代码.py)，共 8 节，全部可运行：

| 节 | 内容 |
|---|---|
| 1 | 不捕获异常会怎样（崩溃反例，注释里有开关可亲眼看崩溃） |
| 2 | try / except 基本用法（捕获后程序继续运行） |
| 3 | 捕获指定异常 + 多个异常 + else / finally（执行顺序） |
| 4 | 常见内置异常一览（FileNotFoundError / IndexError / KeyError / TypeError） |
| 5 | 主动抛出异常 raise |
| 6 | 写文件（with 自动关闭 + 覆盖 / 追加模式） |
| 7 | 读文件（读全部 / 读成行列表 / 逐行读） |
| 8 | 综合小任务：带异常保护的配置文件读取（文件不存在、格式错误都不崩溃，返回默认值） |

### 核心口诀

- `try` 包住可能出错的代码，`except` 接住错误，接住后程序继续跑；
- `with open("文件", "r", encoding="utf-8") as f:` 代码块结束自动关文件，不用手动 close；
- Windows 上处理中文文件务必写 `encoding="utf-8"`，否则容易乱码。

### 执行流程记忆图

- try 块：可能出错的代码照常跑；
- 出错 → except 接住，程序不崩、继续往下走；
- 没出错 → else 才执行（可选）；
- finally：无论如何都会执行，常用于收尾（关文件、关连接）。

---

## 03 Python 有 catch 关键字吗？为什么不是 try catch？

**问题：** 别的语言（Java / C++ / JavaScript）都是 try-catch，为什么 Python 是 try-except？Python 有 catch 吗？

### 回答要点

Python **没有 catch 关键字**，异常处理三个关键字是 `try` / `except` / `finally`（外加可选 `else`）。Python 的 except 就是别的语言里 catch 的角色：

```python
# Java / C++ / JS
try { ... } catch (Exception e) { ... } finally { ... }

# Python
try:
    ...
except Exception as e:
    ...
finally:
    ...
```

**为什么不是 try catch？** 纯粹是语言设计时的历史选择，没有对错之分：

- catch 是 C++ / Java / JavaScript 那一路的传统（"抓住异常"）；
- Python 设计者参考了更早的 ABC、Modula-3 等语言，选了 except——语义是"把异常这个例外情况排除 / 接住"，和 catch 意思一样，只是换了个词（Ruby 用 rescue，Swift 用 catch）。

### 记忆心法

在 Python 里看到 except，就当它是 catch 看，语法位置一一对应。Python 的世界里没有 catch。

---

## 04 为什么 except 能表示异常？它和 try 看起来没什么关联？

**问题：** except 的字面意思是"除了……之外"，跟 try 看起来没什么关联，为什么它能处理异常？

### 回答要点

**try 和 except 靠的不是词义关联，而是"异常"这个隐形主角**：异常从 try 块里产生，被 except 块接住。

- try 的字面义 = 尝试：正常流程照常跑；
- except 的字面义 = 除了……之外：把列出的错误情形单独处理；
- 整句读法："试着运行这段代码；除了出现这些错误的情形（那就要特殊处理），其他都算正常。"

**为什么不用 catch 的思路？** catch 是"动词 + 宾语"（抓异常），词义上显得与 try 关联；except 是"排除情形"，配合 try 的"尝试"，表达的语义是"默认正常、例外除外"——这正是 Python 的 EAFP 哲学（先尝试，出问题再处理）。

**try 和 except 是语法上的固定配对**，靠缩进分组，不需要词义互相解释。Python 里同类配对还有 if/elif/else、for/else、with/as——都是语法规定。
