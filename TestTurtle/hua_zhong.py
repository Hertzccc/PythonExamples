#####################################################################
#
# author:  sheisc@163.com
#
#####################################################################

import turtle
import datetime

t = turtle.Pen()
t2 = turtle.Pen()
hua_bu = t.getscreen()
# x0 = 1.7
# y0 = 0
ban_jin = 1
# hours = 23
# minutes = 58
# seconds = 35
BEI_SHU = 0.8
# shi_qv = "悉尼时间"
# shi_cha = 2
hh_mm_ss = [
    (0,0,0),
    (0,0,0),
]
xin_xi = (
    (-1.7, 0, 0, "北京时间"),
    (1.7, 0, 2, "悉尼时间"),
)

def xie_shi_jian():
    i = 0
    hua_bu.tracer(0)
    t2.clear()
    while i < len(xin_xi):
        x0, y0, shi_cha, shi_qv = xin_xi[i]
        gen_xin_shi_jian(i)
        shi_fen_miao(i)
        t2.penup()
        t2.goto(x0,y0 - 1.3 * ban_jin)
        t2.pendown()
        hours, minutes, seconds = hh_mm_ss[i]
        # print(hh_mm_ss[i])
        # s = "{0:02d}:{1:02d}:{2:02d}".format(hours, minutes, seconds)
        # h = (hours + shi_cha + 24) % 24
        s = (shi_qv + "{0:02d}:{1:02d}:{2:02d}").format(hours, minutes, seconds)
        t2.write(s, align="center", font=("Arial", int(16 / BEI_SHU), "normal"))
        i += 1
    hua_bu.tracer(1)
    hua_bu.ontimer(xie_shi_jian, 1000)


def hua_gu_ding_bu_fen():
    i = 0
    hua_bu.tracer(0)
    while i < len(xin_xi):
        x0, y0, shi_cha, shi_qv = xin_xi[i]
        t.penup()
        t.goto(x0, y0 - 1 * ban_jin)
        t.pendown()
        t.setheading(0)
        t.pensize(10)
        t.circle(ban_jin, steps=100)
        t.penup()
        t.goto(x0, y0)
        t.dot(5)
        t.setheading(90)
        xie_shu_zi(i)
        # xie_shi_jian()
        i += 1
    hua_bu.tracer(1)


def hua_tu():
    hua_gu_ding_bu_fen()
    i = 0
    xie_shi_jian()


def shi_fen_miao(i):
    # x0, y0, shi_cha, shi_qv = xin_xi[i]
    hours, minutes, seconds = hh_mm_ss[i]
    # h = (hours + shi_cha + 24) % 24
    # 画时针
    jiao_du = hours * 30 + (minutes / 60) * 30 + (seconds / 3600) * 30
    hua_biao_zhen(jiao_du, 5, 0.4 * ban_jin, i)
    # 画分针
    jiao_du = minutes * 6 + (seconds / 60) * 6
    hua_biao_zhen(jiao_du, 3, 0.7 * ban_jin, i)
    # 画秒针
    jiao_du = seconds * 6
    hua_biao_zhen(jiao_du, 1, 0.9 * ban_jin, i)



def xie_shu_zi(k):
    # k = 0
    # while k < len(xin_xi):
    x0, y0, shi_cha, shi_qv = xin_xi[k]
    i = 1
    t.penup()
    t.goto(x0, y0 - 0.035 * ban_jin)
    while i <= 12:
        t.right(30)
        t.forward(ban_jin * 0.8)
        t.write(i, align="center", font=("Arial", int(15 / BEI_SHU), "bold"))
        t.backward(ban_jin * 0.8)
        i += 1
        # k += 1


# 更新当前时间
def gen_xin_shi_jian(i):
    # global seconds, minutes, hours
    hours, minutes, seconds = hh_mm_ss[i]
    seconds += 1
    seconds %= 60
    if seconds == 0:
        minutes += 1
        minutes %= 60
        if minutes == 0:
            hours += 1
            hours %= 24
    hh_mm_ss[i] = (hours, minutes, seconds)





# 初始化
def init():
    # global t, hua_bu
    # global seconds, minutes, hours
    # 获取当前系统的时间
    time = datetime.datetime.today()
    # 记录当前时间
    hh_mm_ss[0] = (time.hour,time.minute,time.second)
    hh_mm_ss[1] = (time.hour + xin_xi[1][2], time.minute, time.second)
    hua_bu.setup(1200, 600, 0, 0)
    hua_bu.setworldcoordinates(-4 * BEI_SHU, -2 * BEI_SHU, 4 * BEI_SHU, 2 * BEI_SHU)
    hua_bu.colormode(255)
    t.hideturtle()
    t2.hideturtle()
    hua_tu()


# 保存绘图的结果
def save():
    canvas = hua_bu.getcanvas()
    # 保存画布上的内容到文件main.eps中
    canvas.postscript(file='line.eps')

def hua_biao_zhen(jiao_du,size,chang_du,i):
    x0, y0, shi_cha, shi_qv = xin_xi[i]
    t2.penup()
    t2.goto(x0, y0)
    t2.pendown()
    t2.setheading(90)
    t2.pensize(size)
    t2.right(jiao_du)
    t2.forward(chang_du)




def main():
    # 初始化
    init()
    # 开始绘制
    #
    save()
    # 开始事件循环, 作为一个海龟绘图程序的结束语句
    hua_bu.mainloop()



if __name__ == '__main__':
    main()





