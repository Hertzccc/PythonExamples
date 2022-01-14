#####################################################################
#
# author:  sheisc@163.com
#
#####################################################################
import turtle
import math


DISTANCE = 12
TIME = 48
SPEED_JIA = 3
SPEED_YI = 2
# 更好的写法是通过这4个全局变量来设置坐标轴的显示范围
X_MAX = int(TIME * 1.25)
Y_MAX = int(DISTANCE * 1.25)
X_MIN = int(-TIME / 4)
Y_MIN = int(-DISTANCE / 4)


# global my_pen, my_screen
my_pen = turtle.Pen()
my_screen = my_pen.getscreen()

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


def gen_lawcka(start, dis, v, total_time):
    one_time = dis / v
    t = 0
    ts = []
    ps = []
    pos = start
    while t <= total_time:
        # print(t, pos)
        ts.append(t)
        ps.append(pos)
        t += one_time
        if pos == 0:
            pos = dis
        else:
            pos = 0
    return ts, ps



# 绘制坐标系
def draw_X_Y_axis(x_step, y_step):
    # 黑色画笔
    my_pen.pencolor((0, 0, 0))
    # 横轴X. 即画一条从(-4, 0) 到 （4, 0）的直线
    draw_line(my_pen, [X_MIN, X_MAX], [0, 0])
    # X坐标轴刻度
    x = X_MIN
    while x <= X_MAX:
        # 在画X轴时，已经画过原点刻度
        if x == 0:
            x += 1
            continue
        my_pen.penup()
        my_pen.goto(x, 0)
        if x % x_step == 0:
            my_pen.write(x)
            my_pen.dot(5)
        else:
            my_pen.dot(3)
        x += 1
    # X轴
    my_pen.penup()
    my_pen.goto(X_MAX - 0.4 * x_step, 0.2 * y_step)
    my_pen.write("X", font=("Arial", 16, "bold"))

    # 纵轴Y. 即画一条从(0, -4) 到 (0, 4)的直线
    draw_line(my_pen, [0, 0], [Y_MIN, Y_MAX])
    # Y坐标轴刻度
    y = Y_MIN
    while y <= Y_MAX:

        my_pen.penup()
        if y % y_step == 0:
            my_pen.goto(0 + 0.1 * x_step, y)
            my_pen.write(y)
            my_pen.goto(0, y)
            my_pen.dot(5)
        else:
            my_pen.dot(3)
        my_pen.goto(0, y)

        y += 1
    # Y轴
    my_pen.penup()
    my_pen.goto(0.4 * x_step, Y_MAX - 0.8 * y_step)
    my_pen.write("Y",  font=("Arial", 16, "bold"))
    # 红色画笔
    my_pen.pencolor(255, 0, 0)
    # 绘制坐标轴原点
    my_pen.goto(0, 0)
    # 画一个大小为4的点
    my_pen.dot(4)



def repaint():
    my_screen.tracer(0)
    my_pen.pencolor("black")
    xs , ys = gen_lawcka(0, DISTANCE, SPEED_JIA, TIME)
    draw_line(my_pen, xs, ys)
    my_pen.pencolor("red")
    xs, ys = gen_lawcka(DISTANCE, DISTANCE, SPEED_YI, TIME)
    draw_line(my_pen, xs, ys)
    my_screen.tracer(1)




# 初始化
def init():
    my_screen.setup(800, 600, 0, 0)
    my_screen.setworldcoordinates(X_MIN, Y_MIN, X_MAX, Y_MAX)
    # 每个像素的颜色由(红色分量, 绿色分量, 蓝色分量)构成，每个分量的取值从0到255
    my_screen.colormode(255)
    my_pen.hideturtle()
    my_pen.speed(0)
    my_pen.penup()
    my_screen.tracer(0)
    draw_X_Y_axis(5, 1)
    my_screen.tracer(1)



# 保存绘图的结果
def save(fname):
    canvas = my_screen.getcanvas()
    # 保存画布上的内容到文件main.eps中
    canvas.postscript(file=fname)


def main():
    # 初始化
    init()
    # 开始绘制
    repaint()
    save("lawcka.eps")

    # 开始事件循环, 作为一个海龟绘图程序的结束语句
    my_screen.mainloop()



if __name__ == '__main__':
    main()