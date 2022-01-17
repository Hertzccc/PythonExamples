
################################ 引入class之前的做法 ###############################################


def print_1(stu, prefix):
    # 要访问学生的姓名, 学号和性别等信息时, 要通过列表的下标
    print("{0}\t Name:{1}; ID: {2}; Sex: {3}".format(prefix, stu[0], stu[1], stu[2]))


def test_1():
    # 用两个列表来存放张三和李四这两个学生的信息
    zs = ["Zhang San", 11, "Male"]
    ls = ["Li Si", 12, "Female"]
    # 打印张三和李四的学生信息
    print_1(zs, "PRINT_1")
    print_1(ls, "PRINT_1")


################################ 引入class之后的做法 ################################################


# 定义一个类Student, 用来表示学生的信息
class Student:
    def __init__(self, name, stu_id, sex):  # 构造函数/构造方法, 用来初始化一个学生
        # self.name表示一个成员变量, self指向需要被初始化的那个对象
        self.name = name
        self.stu_id = stu_id
        self.sex = sex

    def print(self, prefix):  # 成员函数
        # self指向调用这个成员函数的那个对象
        # 要访问学生的姓名, 学号和性别等信息时, 在成员函数内, 通过self.name, self.stu_id, self.sex来访问
        print("{0}\t Name:{1}; ID: {2}; Sex: {3}".format(prefix, self.name, self.stu_id, self.sex))


def print_2(stu, prefix):  # 全局函数
    # 要访问学生的姓名, 学号和性别等信息时, 可通过成员变量的名字, 不再像使用列表那样, 需要记住下标的编号, 名字比编号更容易记住
    print("{0}\t Name:{1}; ID: {2}; Sex: {3}".format(prefix, stu.name, stu.stu_id, stu.sex))


def test_2():  # 全局函数
    # 调用构造函数/方法, 来创建一个对象(实例), 实际上调用的函数的函数是在class中定义的__init__()函数
    zs = Student("Zhang San", 11, "Male")
    ls = Student("Li Si", 12, "Female")
    # 打印张三和李四的学生信息
    print_2(zs, "PRINT_2")
    print_2(ls, "PRINT_2")
    # 由于在Student中定义了成员函数print(), 可以直接调用这个函数来打印学生的信息
    zs.print("PRINT")
    ls.print("PRINT")


###############################################################################################################


def main():
    test_1()
    test_2()


if __name__ == '__main__':
    main()
