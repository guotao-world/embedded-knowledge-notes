# -*- coding: utf-8 -*-
"""
========================================
 Python 入门学习代码（适合零基础对照学习）
========================================

【怎么用】
1. 打开命令行（CMD 或 PowerShell），进入本文件所在目录；
2. 输入  python Python入门学习代码.py  回车运行；
3. 从上往下看，每一节都对应一类语法，看不懂的地方记下
   节号，随时来问我。

【小提示】
- 注释（# 开头或三引号包裹的内容）不会被运行，是给人看的说明；
- 代码里 print(...) 负责把内容显示到屏幕上。
"""

# ============================================================
# 第 1 节  变量：给数据起个名字
# ============================================================
print("========== Section 1: Variables ==========")

# 用 = 号把数据存进变量，= 号右边是数据，左边是名字
name = "Alice"          # 字符串（str）：用引号括起来的文本
age = 18                # 整数（int）
height = 1.75           # 浮点数（float）：带小数点的数
is_student = True       # 布尔值（bool）：只有 True / False 两种

print(name)             # 打印变量里存的内容
print(age + 1)          # 变量可以参与运算

# type() 可以查看一个数据是什么类型
print(type(name), type(age), type(height), type(is_student))

# 变量可以重新赋值，新值会覆盖旧值
age = 19
print("age is now:", age)

# ============================================================
# 第 2 节  输入和输出：和程序对话
# ============================================================
print("\n========== Section 2: Input & Output ==========")

# input() 会等待你在屏幕上打字，回车后把输入内容返回
your_name = input("Please enter your name: ")
print("Hello,", your_name)

# 注意：input() 拿到的永远是字符串
# 想当数字用，必须用 int() 或 float() 转换
your_age = input("Please enter your age: ")
your_age = int(your_age)          # 字符串转整数
print("Next year you will be:", your_age + 1)

# ============================================================
# 第 3 节  运算符：让数据动起来
# ============================================================
print("\n========== Section 3: Operators ==========")

a = 10
b = 3
print("a + b =", a + b)       # 加法
print("a - b =", a - b)       # 减法
print("a * b =", a * b)       # 乘法
print("a / b =", a / b)       # 除法，结果一定是浮点数
print("a // b =", a // b)     # 整除：只保留整数部分
print("a % b =", a % b)       # 取余：除法剩下的余数
print("a ** b =", a ** b)     # 乘方：10 的 3 次方

# 比较运算，结果一定是 True 或 False
print("a > b:", a > b)
print("a == b:", a == b)      # 注意：判断相等用两个等号 ==

# 逻辑运算：and（且）、or（或）、not（非）
print("a > 5 and b < 5:", a > 5 and b < 5)
print("a < 5 or b < 5:", a < 5 or b < 5)
print("not True:", not True)

# ============================================================
# 第 4 节  字符串：文本的各种玩法
# ============================================================
print("\n========== Section 4: Strings ==========")

greeting = "Hello, World!"
print(len(greeting))          # len() 求长度（有几个字符）
print(greeting.upper())       # 转大写（注意：不会改原字符串）
print(greeting.lower())       # 转小写

# 索引：从 0 开始数，用 [数字] 取出单个字符
print(greeting[0])            # 第一个字符 'H'
print(greeting[-1])           # -1 表示最后一个字符 '!'

# 切片：用 [起点:终点] 取一段，终点不包含
print(greeting[0:5])          # 'Hello'
print(greeting[:5])           # 开头省略表示从 0 开始
print(greeting[7:])           # 结尾省略表示一直到末尾

# 格式化字符串：f-string，用 {} 往文本里填变量（最常用！）
name2 = "Bob"
score = 92.5
print(f"{name2} got {score} points in the exam.")

# ============================================================
# 第 5 节  列表：一排有序的数据
# ============================================================
print("\n========== Section 5: Lists ==========")

fruits = ["apple", "banana", "orange"]
print(fruits)
print(len(fruits))            # 列表长度
print(fruits[0])              # 下标访问，同样从 0 开始
print(fruits[-1])             # 最后一个

# 增删改
fruits.append("grape")        # 末尾添加
print(fruits)
fruits.insert(1, "pear")      # 在指定位置插入
print(fruits)
fruits.remove("banana")       # 按值删除
print(fruits)
fruits[0] = "watermelon"      # 修改指定位置的值
print(fruits)

# 遍历：用 for 循环把每个元素取出来
for fruit in fruits:
    print("I like", fruit)

# 列表里可以放任何类型，甚至可以混合
mixed = [1, "two", 3.0, True]
print(mixed)

# ============================================================
# 第 6 节  元组、字典、集合
# ============================================================
print("\n========== Section 6: Tuple, Dict, Set ==========")

# 元组 tuple：和列表很像，但创建后不能增删改
point = (10, 20)
print(point[0], point[1])
# point[0] = 99   # 去掉这行注释会报错，元组不可修改

# 字典 dict：用"键"查"值"，键值对存放
student = {
    "name": "Tom",
    "age": 16,
    "city": "Tianjin",
}
print(student["name"])            # 用键取值
student["age"] = 17               # 修改值
student["grade"] = "A"            # 新增键值对
print(student)
print(student.keys())             # 所有键
print(student.values())           # 所有值

# 遍历字典：items() 同时取出键和值
for key, value in student.items():
    print(key, "->", value)

# 集合 set：无序、自动去重
numbers = {1, 2, 2, 3, 3, 3}
print(numbers)                    # 重复的只保留一个
numbers.add(4)
print(numbers)

# ============================================================
# 第 7 节  条件判断：让程序做选择
# ============================================================
print("\n========== Section 7: If / Elif / Else ==========")

score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 60:
    print("Grade: C")
else:
    print("Grade: D")

# 注意缩进！Python 用缩进表示代码块，if 下面缩进的
# 语句只有当条件成立时才执行。

# ============================================================
# 第 8 节  循环：重复做一件事
# ============================================================
print("\n========== Section 8: Loops ==========")

# for 循环：适合知道要循环多少次 / 遍历序列
total = 0
for i in range(1, 6):       # range(1, 6) 生成 1,2,3,4,5（不含6）
    total = total + i       # 累加
print("sum of 1..5 =", total)

# while 循环：适合"满足条件就一直做"
count = 0
while count < 3:
    print("count is", count)
    count = count + 1       # 千万别忘写这行，否则会死循环！

# break 提前结束循环，continue 跳过本次进入下一次
for n in range(1, 10):
    if n == 3:
        continue            # 3 不打印，继续下一个
    if n == 7:
        break               # 到 7 直接停止整个循环
    print("n =", n)

# ============================================================
# 第 9 节  函数：把一段逻辑打包，重复使用
# ============================================================
print("\n========== Section 9: Functions ==========")

# def 定义函数，括号里是参数，return 返回结果
def add(x, y):
    result = x + y
    return result

def say_hello(who):
    print(f"Hello, {who}!")

# 调用函数
print(add(3, 5))
print(add(100, 200))
say_hello("World")
say_hello("Python")

# 参数可以给默认值，调用时可以省略
def greet(who, greeting="Hi"):
    print(f"{greeting}, {who}!")

greet("Alice")                 # 用默认值 "Hi"
greet("Bob", "Good morning")   # 自己指定

# 函数里也可以没有 return，这时返回 None
def show():
    print("this function returns nothing")

print(show())                  # 打印出 None

# ============================================================
# 第 10 节  综合小例子：把上面学到的串起来
# ============================================================
print("\n========== Section 10: Mini Project ==========")

# 做一个简单的"成绩单"程序：记录姓名和成绩，算平均分，判断等级

def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "D"

def main():
    students = []                       # 用列表存所有学生
    print("Enter student info, type 'done' to finish.")

    while True:
        name_input = input("Student name: ")
        if name_input == "done":        # 输入 done 结束
            break
        score_input = int(input("Score: "))
        students.append((name_input, score_input))   # 元组存进列表

    if len(students) == 0:
        print("No students entered.")
        return

    print("\n----- Report -----")
    total_score = 0
    for name_item, score_item in students:
        total_score = total_score + score_item
        print(f"{name_item}: {score_item} -> Grade {get_grade(score_item)}")

    average = total_score / len(students)
    print(f"Average score: {average:.1f}")
    print("------------------")

# 程序从这一行开始真正运行：只有直接运行本文件时才执行 main()
# （以后学到 import 时会明白这句的作用）
if __name__ == "__main__":
    main()
