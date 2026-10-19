# Python print() 函数讲解

> print() 是 Python 最基础的输出函数。这份笔记整理了它的完整用法：基本输出、输出变量、sep / end / f-string 参数、输出到文件，以及与 C 语言 printf() 的对比。

---

## 1. 基本用法

print() 是 Python 的输出函数，用于将字符串、变量、计算结果等输出到终端，类似于 C 语言中的 printf()。

```python
print("Hello World")
print(123)
print(3 + 5)
```

运行结果：

```
Hello World
123
8
```

---

## 2. 输出变量

```python
name = "Tom"
age = 18
print(name)
print(age)
print(name, age)
```

运行结果：

```
Tom
18
Tom 18
```

注意：print() 可以同时输出多个参数，默认使用空格分隔。

---

## 3. 常用参数

### 3.1 sep：设置参数之间的分隔符

默认分隔符是一个空格。

```python
print("2026", "10", "19")
print("2026", "10", "19", sep="-")
```

运行结果：

```
2026 10 19
2026-10-19
```

### 3.2 end：设置输出结束后的内容

默认情况下，print() 输出结束后会换行，相当于结尾添加 \n。

```python
print("Hello")
print("World")
```

运行结果：

```
Hello
World
```

修改 end 后可以不换行：

```python
print("Hello", end=" ")
print("World")
```

运行结果：

```
Hello World
```

如果不想换行，也不想添加空格：

```python
print("Hello", end="")
print("World")
```

运行结果：

```
HelloWorld
```

### 3.3 f-string：格式化字符串

在字符串前添加 f，就可以使用 {} 将变量或表达式嵌入字符串。

```python
name = "Tom"
age = 18
print(f"姓名：{name}，年龄：{age}")
```

运行结果：

```
姓名：Tom，年龄：18
```

也可以直接计算表达式：

```python
a = 10
b = 20
print(f"a + b = {a + b}")
```

运行结果：

```
a + b = 30
```

---

## 4. 将内容输出到文件

默认情况下，print() 将内容输出到终端。通过 file 参数，可以将内容输出到文件对象。

```python
with open("output.txt", "w", encoding="utf-8") as f:
    print("Hello World", file=f)
    print("Python", file=f)
```

运行后，output.txt 文件的内容为：

```
Hello World
Python
```

注意："w" 表示写入模式。如果文件已经存在，原有内容通常会被清空。

---

## 5. 与 C 语言 printf() 对比

| 功能 | Python | C 语言 |
|---|---|---|
| 输出字符串 | print("Hello") | printf("Hello"); |
| 输出变量 | print(a) | printf("%d", a); |
| 输出多个变量 | print(a, b) | printf("%d %d", a, b); |
| 输出后不换行 | print(a, end="") | printf("%d", a); |
| 格式化字符串 | print(f"{a}") | printf("%d", a); |

Python 的 print() 会自动处理常见数据类型的转换，不需要像 C 语言一样为整数、浮点数分别指定 %d、%f 等格式符。

---

## 6. 常见注意事项

### 6.1 print() 不会修改变量

```python
a = 10
print(a)
print(a)
```

两次输出都是 10，因为 print() 只是输出数据，不会改变变量的值。

### 6.2 print() 默认会换行

```python
print("A")
print("B")
```

输出：

```
A
B
```

如果不希望换行，可以使用 end=""。

### 6.3 输出到终端不等于写入文件

```python
print(content)          # 将 content 输出到终端
print(content, file=f)  # 将 content 输出到文件对象 f
```

---

## 7. 初学阶段需要掌握的内容

优先掌握以下四种用法：

```python
# 1. 输出字符串
print("Hello World")

# 2. 输出变量
name = "Tom"
print(name)

# 3. 输出多个参数
a = 10
b = 20
print(a, b)

# 4. 使用 f-string 格式化字符串
print(f"a = {a}, b = {b}, sum = {a + b}")
```

---

## 总结

print() 是 Python 中最基础的输出函数。初学阶段重点掌握基本输出、多个参数、sep、end 和 f-string，就能满足大部分日常调试和输出需求。
