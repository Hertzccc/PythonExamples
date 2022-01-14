# -*- coding: utf-8 -*-
#####################################################################
#
# author:  sheisc@163.com
#
#####################################################################
import turtle

import random
import datetime


# 用于绘制钟的乌龟，目前的库函数circle()在画圈时，速度很慢.
# 而钟的外形是一个圆，在运行时，这个圆不需要更新,
# 只需要在初始化时，绘制一次即可.
clock_turtle = turtle.Pen()
clock_turtle.hideturtle()
# 用于绘制钟的秒针，分针，时针，这部分在运行时，要动态变化
hand_turtle = turtle.Turtle()
# 当前窗口
cur_screen = clock_turtle.getscreen()
# 设置窗口大小为800 * 600, 位于显示器的左上角
cur_screen.setup(800, 600, 0, 0)

# 全局变量，用于存放当前时间（几时几分几秒）
seconds = 0
minutes = 0
hours = 0

# 钟的半径
R = 120
# 钟的中心点的横坐标和纵坐标
clock_X = -200
clock_Y = 150

# 绘制钟上圆周上的数字：从1至12
def write_numbers(t:turtle.Pen):
    number = 1
    while number <= 12:
        t.right(30)
        t.forward(R * 0.8)
        t.write(number, align="center", font=("Arial", 10, "bold"))
        t.backward(R * 0.8)
        number += 1


# 海龟回到钟的中心
def goto_clock_center(t:turtle.Pen):
    t.penup()
    t.home()
    t.left(90)
    t.goto(clock_X, clock_Y)


# 绘制表针，可以是秒针，分针，或者时针
def draw_hand(t:turtle.Pen, r_angle, color, size, length):
    t.right(r_angle)
    t.pensize(size)
    t.pencolor(color)
    t.pendown()
    t.forward(length)
    t.penup()
    t.backward(length)


# 更新当前时间
def update_time():
    global seconds, minutes, hours
    seconds += 1
    seconds %= 60
    if seconds == 0:
        minutes += 1
        minutes %= 60
        if minutes == 0:
            hours += 1
            hours %= 24

# 绘制秒针
def draw_second_hand(t:turtle.Pen):
    # 对秒针而言，走一圈要花60秒，每秒对应的度数为（360/6）度， 即6度
    goto_clock_center(hand_turtle)
    angle = seconds * 6
    draw_hand(hand_turtle, angle, "black", 1, R * 0.7)

# 绘制分针
def draw_minute_hand(t:turtle.Pen):
    # 对分针而言，走一圈要花60分钟，每分钟对应的度数为（360/6）度， 即6度
    goto_clock_center(hand_turtle)
    angle = (minutes + seconds / 60.0) * 6
    draw_hand(hand_turtle, angle, "black", 2, R * 0.5)

# 绘制时针
def draw_hour_hand(t:turtle.Pen):
    # 对时针而言，走一圈要花12个小时，刻度从1到12,共12个刻度，每个小时对应的度数为30度
    goto_clock_center(hand_turtle)
    angle = (hours % 12 + minutes / 60.0 + seconds / 3600.0)  *  30
    draw_hand(hand_turtle, angle, "black", 3, R * 0.35)


# 显示16:20:00这样的时间
def draw_HH_MM_SS(t:turtle.Pen):
    goto_clock_center(hand_turtle)
    # {0}表示第0个参数
    # {0:02d} 表示把第0个参数显示为10进制的整数，如果少于2位数字，则高位补0，比如，8会表示为08
    s = "{0:02d}:{1:02d}:{2:02d}".format(hours, minutes, seconds)
    hand_turtle.write(s, align="center", font=("Arial", 16, "normal"))

# 绘制钟的固定部分, 屏幕刷新时，不用变化的部分
def draw_clock(t:turtle.Pen):
    t.penup()
    t.home()
    # 从中心点的正下方开始画圆
    t.goto(clock_X, clock_Y - R)
    t.pensize(3)
    t.pendown()
    t.circle(R)
    goto_clock_center(t)
    # 绘制中心点
    t.dot(10)
    write_numbers(t)


# 刷新屏幕， 重新绘制变化的部分
def repaint():
    update_time()

    # 禁用海龟动画
    cur_screen.tracer(0)

    # 从屏幕中删除海龟的绘图，海龟回到原点并设置所有变量为默认值。
    hand_turtle.reset()
    hand_turtle.hideturtle()

    # 显示 16:20:00
    draw_HH_MM_SS(hand_turtle)
    # 绘制秒针
    draw_second_hand(hand_turtle)
    # 绘制分针
    draw_minute_hand(hand_turtle)
    # 绘制时针
    draw_hour_hand(hand_turtle)

    # 允许海龟动画
    cur_screen.tracer(1)
    # 设置定时器(闹钟)，1000毫秒后要调用repaint()函数
    # 通过定时器， 我们实际上又变相地做到了循环
    cur_screen.ontimer(repaint, 1000)



def init():
    global seconds, minutes, hours
    # 获取当前系统的时间
    t = datetime.datetime.today()
    # 记录当前时间
    seconds = t.second
    minutes = t.minute
    hours = t.hour

    # 禁用海龟动画
    cur_screen.tracer(0)

    # 由clock_turtle来绘制不变的部分
    draw_clock(clock_turtle)


def save_screen():
    # 得到画布
    canvas = cur_screen.getcanvas()
    # 保存画布上的内容到文件main.eps中
    canvas.postscript(file='main.eps')


def draw():
    # 初始化
    init()
    # 绘制
    repaint()
    # 保存当前屏幕
    save_screen()


    # 开始事件循环，作为一个海龟绘图程序的结束语句
    cur_screen.mainloop()

# 如果clock.py是由于 python clock.py而被执行,
# 即clock.py是作为主模块，则以下if条件会成立，
# 而如果clock.py是在另一个python文件中被import，
# 比如用户执行的是python main.py, 而在main.py中，存在import clock,
# 则clock.py被main.py导入时，以下if条件不成立,
# 因为在这种情况下，主模块是main.py
if __name__ == '__main__':
    draw()