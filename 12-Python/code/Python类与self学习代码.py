# -*- coding: utf-8 -*-
"""
========================================
 Python 面向对象：类（class）与 self
========================================

这一份专门解决两个问题：
1. 类到底是什么？类和对象有什么关系？
2. 为什么类里面有的方法参数里有 self，有的却没有？

建议对照第 1 份基础代码来看，这里默认你已经掌握了
变量、函数、列表、字典这些基础语法。
"""

# ============================================================
# 第 1 节  类和对象：图纸 与 按图纸造出来的东西
# ============================================================
print("========== Section 1: Class & Object ==========")

# 类（class）相当于一张"图纸"，描述一类东西长什么样、会做什么
# 对象（object / 实例 instance）是照图纸造出来的具体一个

class Dog:
    pass                     # pass 表示"空内容"，占位用

# 类名加括号 = 按图纸造一个对象，这个过程叫"实例化"
d1 = Dog()
d2 = Dog()

print(type(d1))              # <class '__main__.Dog'>，d1 是 Dog 类型的对象
print(d1 is d2)              # False：同一个图纸能造出互不相干的两个对象

# ============================================================
# 第 2 节  实例属性与 __init__：self 第一次登场
# ============================================================
print("\n========== Section 2: __init__ and self ==========")

class Cat:
    # __init__ 是"构造方法"：造对象时 Python 自动调用它，
    # 用来给这个对象设置初始数据
    def __init__(self, name, age):
        self.name = name     # 把参数 name 存到"这个对象自己"身上
        self.age = age

# 造对象：小括号里的参数传给 __init__
# 注意：写 Cat("Mimi", 2) 时你只传了 2 个参数，
#       但 __init__ 写的是 3 个参数（self, name, age）——为什么？
#       因为第一个参数 self 不用你传，Python 自动把
#       "刚造出来的那个对象"塞进去。
c1 = Cat("Mimi", 2)
c2 = Cat("Tuanzi", 5)

# 每个对象都有自己的 name 和 age，互不干扰
print(c1.name, c1.age)       # Mimi 2
print(c2.name, c2.age)       # Tuanzi 5

# 想看懂 self，可以把这句话记死：
#   self = 正在被操作的那个对象自己
#   self.name = name 的意思是：把我这个对象身上 name 这块牌子，
#   贴上参数 name 的值。

# ============================================================
# 第 3 节  实例方法：为什么必须有 self
# ============================================================
print("\n========== Section 3: Instance Methods ==========")

class Bird:
    def __init__(self, name):
        self.name = name

    # 这是一个"实例方法"，它的特点：方法体里要使用
    # "这个对象自己的数据"（比如 self.name），
    # 所以必须写 self，告诉 Python "我操作的是谁"。
    def sing(self):
        print(f"{self.name} is singing!")

    def introduce(self, words):
        print(f"{self.name} says: {words}")

b1 = Bird("Xiaohong")
b1.sing()                    # 你只写了 b1.sing()，没传参数
# 但实际上 Python 自动翻译成了：Bird.sing(b1)
# 也就是把 b1 传给了 self —— 所以 sing 里能用 self.name

b1.introduce("Hello!")       # 只传了 words 一个参数，self 还是自动传入

# 关键结论：
#   实例方法 = 需要"操作这个对象自己"的方法，第一个参数必须写 self。
#   调用时 self 不用你填，Python 自动把对象传进去。

# ============================================================
# 第 4 节  什么时候可以没有 self：静态方法
# ============================================================
print("\n========== Section 4: Static Methods ==========")

class Calculator:
    # 普通写法：把功能当函数直接写在外面也行，但放类里更整齐
    # 关键：这个方法既不碰对象数据（self.xxx），也不碰类数据，
    #       就是一段"和谁都没关系"的纯逻辑，
    #       所以不需要 self，用 @staticmethod 声明成"静态方法"。
    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def is_even(num):
        return num % 2 == 0

# 静态方法用"类名.方法名()"调用，传几个参数就写几个，没有 self
print(Calculator.add(3, 4))          # 7
print(Calculator.is_even(10))        # True

# 实例对象也能调静态方法，但一般不这么用
cal = Calculator()
print(cal.add(1, 2))                 # 3（能运行，但不推荐）

# 判断标准（背下来）：
#   方法里要用 self.xxx（对象自己的数据）→ 实例方法 → 写 self
#   方法里谁的数据都不用 → 静态方法 → @staticmethod，不写 self
#   方法里要用 类自己的数据（见下一节）→ 类方法 → 写 cls

# ============================================================
# 第 5 节  类方法：用 cls 代替 self
# ============================================================
print("\n========== Section 5: Class Methods ==========")

class Student:
    # 类属性：写在类里面、方法外面的变量，
    # 属于"整个类"而不是某个对象，所有对象共用
    school = "No.1 High School"

    def __init__(self, name, grade):
        self.name = name              # 实例属性：属于每个对象自己
        self.grade = grade

    # 实例方法：能访问 self.xxx
    def show(self):
        print(f"{self.name}, grade {self.grade}, {Student.school}")

    # 类方法：第一个参数约定写成 cls（class 的缩写），
    # 它代表"这个类本身"，用来操作类属性或批量造对象。
    # 它不用 self，因为不需要某个具体对象的数据。
    @classmethod
    def get_school(cls):
        return cls.school

    # 类方法常用场景：提供一个"工厂方法"，方便地造对象
    @classmethod
    def create_from_grade(cls, name, grade):
        return cls(name, grade)

    # 静态方法对比：不碰任何数据
    @staticmethod
    def is_valid_grade(g):
        return 1 <= g <= 12

s1 = Student("Alice", 10)

# 实例方法：self 自动传入
s1.show()

# 类方法：cls 自动传入（不需要你传）
print(Student.get_school())          # No.1 High School

# 类方法造对象：本质还是调 __init__，但把创建逻辑集中管理
s2 = Student.create_from_grade("Bob", 11)
s2.show()

# 静态方法调用
print(Student.is_valid_grade(13))    # False

# ============================================================
# 第 6 节  三种方法放一起对比（重点中的重点）
# ============================================================
print("\n========== Section 6: Side-by-side Comparison ==========")

class Account:
    # 类属性：所有账户共用
    bank = "MyBank"

    def __init__(self, owner, balance):
        self.owner = owner            # 实例属性
        self.balance = balance

    # ① 实例方法：有 self —— 要用"这个账户自己"的钱
    def deposit(self, amount):
        self.balance += amount
        return self.balance

    # ② 类方法：有 cls —— 要访问"整个类"的银行名，但不用具体账户
    @classmethod
    def get_bank(cls):
        return cls.bank

    # ③ 静态方法：无 self 也无 cls —— 只是算账规则，谁的数据都不碰
    @staticmethod
    def interest_after(rate, years):
        # 简单单利计算示例
        return rate * years

acc = Account("Tom", 1000)
print(acc.deposit(500))                    # 实例方法，self = acc
print(Account.get_bank())                  # 类方法，cls = Account
print(Account.interest_after(0.03, 2))     # 静态方法，什么都不传

# ============================================================
# 第 7 节  常见坑：方法里忘了写 self 会怎样？
# ============================================================
print("\n========== Section 7: Common Pitfall ==========")

# 下面这个类的写法是错的（故意的，给你看报错）：
class Wrong:
    def __init__(self, name):
        self.name = name

    def show_name():          # 忘了写 self！
        print(self.name)

w = Wrong("Test")
# w.show_name()
# ↑ 取消上面这行的注释再运行，会报：
#   TypeError: Wrong.show_name() takes 0 positional arguments but 1 was given
# 意思是：show_name 明明没写参数，Python 却硬塞了一个进来。
# 那个"硬塞进来"的东西就是 w（对象自己）！
# 这正说明了：Python 调实例方法时，一定会自动把对象传给第一个参数。

# 正确写法：一定要留出第一个位置给 self
class Right:
    def __init__(self, name):
        self.name = name

    def show_name(self):
        print(self.name)

r = Right("OK")
r.show_name()

# ============================================================
# 第 8 节  综合小例子：写一个完整的"小狗"类
# ============================================================
print("\n========== Section 8: Mini Project ==========")

class Dog:
    # 类属性：所有狗共用的信息
    species = "Canis familiaris"

    def __init__(self, name, age):
        self.name = name        # 实例属性：每只狗自己的
        self.age = age

    # 实例方法：用到 self.name / self.age
    def bark(self):
        print(f"{self.name}: Woof!")

    def birthday(self):
        self.age += 1
        print(f"{self.name} is now {self.age} years old.")

    # 类方法：用到类属性 species
    @classmethod
    def get_species(cls):
        return cls.species

    # 类方法：方便地造一只小奶狗
    @classmethod
    def create_puppy(cls, name):
        return cls(name, 0)

    # 静态方法：纯逻辑，谁的数据都不用
    @staticmethod
    def is_puppy(age):
        return age < 1

# 用类方法造对象
puppy = Dog.create_puppy("Mochi")
puppy.bark()
print(Dog.get_species())               # Canis familiaris
print(Dog.is_puppy(puppy.age))         # True
puppy.birthday()                       # Mochi is now 1 years old.

# ============================================================
# 最后总结（背下来）
# ============================================================
#
# 方法类型        第一个参数     什么时候用
# -----------------------------------------------
# 实例方法        self          要用"某个对象自己的数据"（self.xxx）
# 类方法          cls           要用"整个类共用的数据"（类属性），
#                               @classmethod 修饰
# 静态方法        无            谁的数据都不用，只是一段工具逻辑，
#                               @staticmethod 修饰
#
# self 不是 Python 关键字，只是大家都遵守的命名约定；
# 它和 cls 都不需要你调用时传，Python 自动帮你填。
#
# 判断口诀：见 self → 我在动"这个对象"；见 cls → 我在动"这个类"；
#          都没有 → 我谁也不动。
