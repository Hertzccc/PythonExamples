import student


# 博士生也是学生, 所以可以复用已有的学生Student这个类的代码, 这个称为"继承"
class PhDStudent(student.Student):
    def __init__(self, name, stu_id, sex, salary):
        # 调用父类Student的构造函数先进行初始化
        student.Student.__init__(self, name, stu_id, sex)
        # 再初始化博士生新加入的数据成员, 博士生有工资收入
        # 工资self.salary是为博士生新添加的数据成员
        self.salary = salary

    def do_research(self):  # 为博士生新添加的成员函数, 博士生要做科研
        # self.print("")
        print("PhDStudent\t do_research(); salary = {0}; name = {1}".format(self.salary, self.name))

    def print(self, prefix):  # 改写父类Student中已有的成员函数print()
        print("{0}\t Name:{1}; ID: {2}; Sex: {3}; Salary: {4}".format(
                        prefix, self.name, self.stu_id, self.sex, self.salary))
        # 也可以先调用父类Student.print()
        # student.Student.print(self, prefix)
        # 再输出工资
        # print("salary = {0}".format(self.salary))


def main():
    # Wang Wu 是个博士生
    # 由于PhDStudent继承了Student, 所以Wang Wu是博士生, 也肯定是个学生
    ww = PhDStudent("Wang Wu", 30, "Male", 10000)
    ww.print("PhDStudent")
    ww.do_research()

    # Zhang San 是个学生, 但不是个博士生
    zs = student.Student("Zhang San", 11, "Male")
    zs.print("Student")
    # 普通学生, 没有do_research()这个成员函数
    #zs.do_research()


if __name__ == '__main__':
    main()
