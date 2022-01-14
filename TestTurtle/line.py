#####################################################################
#
# author:  sheisc@163.com
#
#####################################################################
import turtle
import math

# 更好的写法是通过这4个全局变量来设置坐标轴的显示范围
X_MAX = 4
Y_MAX = 4
X_MIN = -4
Y_MIN = -4

#################################################
# 用笔（即海龟) t来绘制折线，即多条线段
# xs: 折线中各点的横坐标
# ys: 折线中各点的纵坐标
# fill: 是否填充折线围成的多边形, 缺省值为0, 不填充.
# ###############################################
def draw_line(t: turtle.Pen, xs: list, ys: list, fill = 0):
    x = xs[0]
    y = ys[0]
    t.penup()
    t.goto(x,y)
    i = 1
    t.pendown()
    if fill:
        t.begin_fill()
    while i < len(xs) and i < len(ys):
        t.goto(xs[i], ys[i])
        i += 1
    if fill:
        t.end_fill()



###############################################
#
# 生成直线 y = k*x + b 上的多个点的坐标
#
# k为直线的斜率
# b为直线的截距(与Y轴的交点的纵坐标）
# x_start为横坐标x的开始位置
# x_end为横坐标x的结束位置
# step为步长，从开始位置x_start, 每步增加step， 直到x_end为止
#
################################################
def gen_line(k, b, x_start, x_end, step):
    xs = []
    ys = []
    x = x_start
    while x < x_end:
        y = k * x + b
        xs.append(x)
        ys.append(y)
        x += step
    return xs, ys


def repaint():
    # 关闭海龟动画
    # my_screen.tracer(0)
    # 产生直线 y = x + 1 上的点，x从-2到2, 每步增加0.01
    xs, ys = gen_line(1, 1, -2, 2, 0.01)
    draw_line(my_pen, xs, ys)
    # 产生直线 y = x上的点，x从-1到2, 每步增加0.01
    xs, ys = gen_line(1, 0, -1, 2, 0.01)
    draw_line(my_pen, xs, ys)
    # 绘制一段封闭的折线，并填充为黄色
    my_pen.fillcolor((255, 255, 0))
    # 5个点，坐标分别为(2, 2), (3, 2), (3, 3), (2, 3), (2, 2)
    # 首尾两个点的坐标一样，都是(2, 2)，则可以构成一个封闭的多边形
    # 这5个点的横坐标构成列表 [2, 3, 3, 2, 2]
    # 这5个点的纵坐标构成列表 [2, 2, 3, 3, 2]
    draw_line(my_pen, [2, 3, 3, 2, 2], [2, 2, 3, 3, 2], 1)
    # 允许海龟动画
    # my_screen.tracer(1)

# 绘制坐标系
def draw_X_Y_axis():
    # 设置我们自定义的坐标系
    # 使窗口的左下角的坐标为（-4, -4）
    # 使窗口的右上角的坐标为 (4, 4)
    my_screen.setworldcoordinates(-4, -4, 4, 4)
    # 每个像素的颜色由(红色分量, 绿色分量, 蓝色分量)构成，每个分量的取值从0到255
    my_screen.colormode(255)
    my_pen.hideturtle()
    my_pen.speed(0)
    my_pen.penup()
    # 黑色画笔
    my_pen.pencolor((0, 0, 0))
    # 横轴X. 即画一条从(-4, 0) 到 （4, 0）的直线
    draw_line(my_pen, [-4, 4], [0, 0])
    # X坐标轴刻度
    x = -4
    while x <= 4:
        my_pen.penup()
        my_pen.goto(x, 0)
        my_pen.write(x)
        my_pen.dot(3)
        x += 1
    # X轴
    my_pen.penup()
    my_pen.goto(3.8, 0.2)
    my_pen.write("X", font=("Arial", 16, "bold"))

    # 纵轴Y. 即画一条从(0, -4) 到 (0, 4)的直线
    draw_line(my_pen, [0, 0], [-4, 4])
    # Y坐标轴刻度
    y = -4
    while y <= 4:
        # 在画X轴时，已经画过原点刻度
        if y == 0:
            y += 1
            continue
        my_pen.penup()
        my_pen.goto(0 + 0.03, y)
        my_pen.write(y)
        my_pen.goto(0, y)
        my_pen.dot(3)
        y += 1
    # Y轴
    my_pen.penup()
    my_pen.goto(0.2, 3.8)
    my_pen.write("Y",  font=("Arial", 16, "bold"))
    # 红色画笔
    my_pen.pencolor((255, 0, 0))
    # 绘制坐标轴原点
    my_pen.goto(0, 0)
    # 画一个大小为4的点
    my_pen.dot(4)


# 初始化
def init():
    global my_pen, my_screen
    my_pen = turtle.Pen()
    my_screen = my_pen.getscreen()
    my_screen.setup(800, 800, 0, 0)
    # 画坐标轴
    draw_X_Y_axis()


# 保存绘图的结果
def save():
    canvas = my_screen.getcanvas()
    # 保存画布上的内容到文件main.eps中
    canvas.postscript(file='line.eps')


def main():
    # 初始化
    init()
    # 开始绘制
    repaint()
    #
    save()
    # 开始事件循环, 作为一个海龟绘图程序的结束语句
    my_screen.mainloop()



if __name__ == '__main__':
    main()