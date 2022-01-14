#####################################################################
#
# author:  sheisc@163.com
#
#####################################################################

import turtle
from fonts.hz import *
import random



SIZE = 16

# 每个16点字阵的汉字要占34个字节，其中2个字节对应其gb2312编码, 32字节对应其点阵(位图)
LEN = 34

# 10 行
ROWS = 16
# 10 列
COLS = 80
# 当前要显示的字符的开始位置
offset = 0

my_pen = turtle.Pen()
my_screen = my_pen.getscreen()
bmps = []


def draw_a_block(x, y, col):
    # print(x, y)
    my_pen.penup()
    my_pen.goto(x, y)
    my_pen.pendown()
    old_c = my_pen.fillcolor()
    my_pen.fillcolor(col)
    my_pen.begin_fill()
    my_pen.goto(x + 1, y)
    my_pen.goto(x + 1, y + 1)
    my_pen.goto(x, y + 1)
    my_pen.goto(x, y)
    my_pen.end_fill()
    my_pen.fillcolor(old_c)




# 迷宫列表中的行号和列号(r, c) 转换成海龟画图坐标中的(x, y)
def convert_RC_to_XY(r, c):
    return c, ROWS - 1 - r


# 海龟画图坐标中的(x, y) 转换成迷宫列表中的行号和列号(r, c)
def convert_XY_to_RC(x, y):
    return ROWS - 1 - y, x


# 获取位图bmp第r行，第c列对应位的值， 要么是0, 要么是1
def get_bit(bmp, r, c):
    r %= 16
    c %= 16
    # 在hz_gb2312列表保存的位图，每一行的位与窗口上显示的每一行的顺序是相反的
    c = 15 - c
    b2 = (bmp[r * 2 + 1] | (bmp[r * 2] << 8))
    if (b2 & (1 << c)) == 0:
        return 0
    else:
        return 1




# x为gb2312编码， 在hz_gb2312这个列表中查找，看看是否存在相同编码的汉字
# 如果存在，则返回其点阵，否则返回32个0.
def get_bitmap(x):
    for i in range(len(hz_gb2312)//LEN):
        cur = (hz_gb2312[i*LEN] << 8) | hz_gb2312[i*LEN + 1]
        if x == cur:
            return hz_gb2312[i*LEN + 2: i*LEN + LEN]
    # return [0xAA] * 16 + [0x55] * 16
    return [0x00] * 32


# 打印点阵（位图）
def print_bmp(bmp):
    s = ""
    for x in bmp:
        s += "0x{0:02x}, ".format(x)
    print(s)


# 在r0, c0处显示一个汉字s
def draw_char(r0, c0, bmp):
    # 获取字符对应的gb2312编码

    for r in range(SIZE):
        for c in range(SIZE):
            if r0 + r < ROWS and c0 + c < COLS:
                x, y = convert_RC_to_XY(r0 + r, c0 + c)
                if get_bit(bmp, r, c) == 1:
                    draw_a_block(x, y, (255, 255, 0))




def repaint():
    global offset

    r0 = 0
    c0 = 0


    # print_bmp(bmp)

    # 画绿色背景
    for r in range(ROWS):
        for c in range(COLS):
            x, y = convert_RC_to_XY(r, c)
            draw_a_block(x, y, (0, 255, 0))
    # 每次在窗口上显示(COLS//SIZE)个汉字
    if len(bmps) > 0:
        i = 0
        while i < COLS//SIZE:
            k = (offset + i) % len(bmps)
            draw_char(r0, c0 + i * SIZE, bmps[k])
            i += 1
    offset += 1
    offset %= len(bmps)
    my_screen.update()
    my_screen.ontimer(repaint, 2000)




# 初始化
def init():
    my_screen.colormode(255)
    my_screen.setup(800, 160, 0, 0)
    my_screen.setworldcoordinates(0, 0, COLS, ROWS)
    my_pen.hideturtle()
    my_pen.speed(0)
    my_screen.tracer(0)
    my_screen.title("Display fonts")

    s = '吴王好剑客 百姓多创瘢 楚王好细腰 宫中多饿死 '
    for c in s:
        g = c.encode('gb2312')
        if len(g) == 2:
            x = (g[0] << 8) | g[1]
        else:
            x = 0
        bmp = get_bitmap(x)
        bmps.append(bmp)


def main():
    # 初始化
    init()
    #
    repaint()

    # 开始事件循环, 作为一个海龟绘图程序的结束语句
    my_screen.mainloop()



if __name__ == '__main__':
    main()

