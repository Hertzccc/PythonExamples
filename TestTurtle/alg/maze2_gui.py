#####################################################################
#
# author:  sheisc@163.com
#
#####################################################################
import turtle
import math
import maze2
#import alg.maze.map as maze_map

# 更好的写法是通过这4个全局变量来设置坐标轴的显示范围
GUI_X_MAX = maze2.X_MAX + 1
GUI_Y_MAX = maze2.Y_MAX + 1
GUI_X_MIN = 0
GUI_Y_MIN = 0

# global my_pen, my_screen
my_pen = turtle.Pen()
my_screen = my_pen.getscreen()
# pass_block = turtle.Pen()
# road_block = turtle.Pen()


def draw_exit_mark(x, y):
    pos = my_pen.pos()
    h = my_pen.heading()

    my_pen.penup()
    my_pen.goto(x + 0.5, y + 0.5)
    my_pen.pendown()
    my_pen.dot(15)

    #
    my_pen.penup()
    my_pen.setheading(h)
    my_pen.setpos(pos)



def draw_a_block(x, y, col):
    pos = my_pen.pos()
    h = my_pen.heading()

    my_pen.penup()
    my_pen.goto(x, y)
    my_pen.pendown()
    old_c = my_pen.fillcolor()
    my_pen.fillcolor(col)
    my_pen.begin_fill()
    for i in range(4):
        my_pen.forward(1)
        my_pen.left(90)
    my_pen.end_fill()
    my_pen.fillcolor(old_c)

    #
    my_pen.penup()
    my_pen.setheading(h)
    my_pen.setpos(pos)



def draw_an_arrow(x, y, angle, line_len, edge_len):
    # 清空当前格中内容
    draw_a_block(x, y, "white")
    pos = my_pen.pos()
    h = my_pen.heading()
    # 移到格的中心
    my_pen.penup()
    my_pen.goto(x + 0.5, y + 0.5)
    my_pen.setheading(angle)
    #
    # 画线段
    my_pen.pensize(5)
    my_pen.pendown()
    # 倒退
    my_pen.backward(line_len * 2 / 3)
    my_pen.forward(line_len)
    my_pen.pensize(1)
    # 画三角形
    my_pen.penup()
    my_pen.right(90)
    my_pen.backward(edge_len/2)
    my_pen.pendown()
    my_pen.fillcolor("black")
    my_pen.begin_fill()
    for i in range(3):
        my_pen.forward(edge_len)
        my_pen.left(120)
    my_pen.end_fill()

    #
    my_pen.penup()
    my_pen.setheading(h)
    my_pen.setpos(pos)


# 迷宫列表中的行号和列号(r, c) 转换成海龟画图坐标中的(x, y)
def convert_RC_to_XY(r, c):
    return c, maze2.Y_MAX - r


# 海龟画图坐标中的(x, y) 转换成迷宫列表中的行号和列号(r, c)
def convert_XY_to_RC(x, y):
    return maze2.Y_MAX - y, x


# 由海龟画图坐标中的(x, y), 来获得迷宫列表中的(r, c)处的值
def get_value_in_maze(x, y):
    r, c = convert_XY_to_RC(x, y)
    return maze2.map[r][c]


# 更新海龟画图坐标中的(x, y)的图案
def update_one_pos(x, y):
    val = get_value_in_maze(x, y)
    if val == maze2.BLOCK_MARK:
        draw_a_block(x, y, (0, 255, 0))
    elif val == maze2.RIGHT:
        draw_an_arrow(x, y, 0, 0.3, 0.2)
    elif val == maze2.UP:
        draw_an_arrow(x, y, 90, 0.3, 0.2)
    elif val == maze2.LEFT:
        draw_an_arrow(x, y, 180, 0.3, 0.2)
    elif val == maze2.DOWN:
        draw_an_arrow(x, y, 270, 0.3, 0.2)
    elif val == maze2.PASS_MARK:
        draw_a_block(x, y, (255, 255, 255))
    elif val == maze2.EXIT_MARK:
        draw_exit_mark(x, y)



def repaint():
    #  如果迷宫算法还没有结束
    if not maze2.HAS_FINISHED:
        # 关闭海龟动画
        my_screen.tracer(0)
        # 运行迷宫算法，只探索一步
        maze2.explore(maze2.map, True)
        #
        n = len(maze2.stack)
        if n >= 2:
            i = 2
        elif n == 1:
            i = 1
        # 更新栈顶的1个或者2个位置
        while i > 0:
            r, c = maze2.stack[n - i]
            x, y = convert_RC_to_XY(r, c)
            update_one_pos(x, y)
            i -= 1
        # 开启海龟动画
        my_screen.tracer(1)
        # 设置定时器
        my_screen.ontimer(repaint, 500)
    else:
        save("maze_answer.eps")



# 初始化
def init():

    my_screen.colormode(255)
    my_screen.setup(600, 600, 0, 0)
    my_screen.setworldcoordinates(GUI_X_MIN, GUI_Y_MIN, GUI_X_MAX, GUI_Y_MAX)
    my_pen.hideturtle()
    my_pen.speed(0)
    #
    my_screen.tracer(0)

    for x in range(GUI_X_MIN, GUI_X_MAX):
        for y in range(GUI_Y_MIN, GUI_Y_MAX):
            update_one_pos(x, y)

    # 允许海龟动画
    my_screen.tracer(1)
    # 初始化迷宫算法的栈
    maze2.stack.append((1, 0))



    #pass_block.color("black", "green")


# 保存绘图的结果
def save(filename):
    canvas = my_screen.getcanvas()
    # 保存画布上的内容到文件main.eps中
    canvas.postscript(file=filename)


def main():
    # 初始化
    init()
    # 开始绘制
    repaint()
    #
    save("maze.eps")
    # 开始事件循环, 作为一个海龟绘图程序的结束语句
    my_screen.mainloop()



if __name__ == '__main__':
    main()