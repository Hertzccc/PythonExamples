
import turtle

# import random
#
# r = random.randint(0, 10)
# print(r)
# if r != 1:
#     draw_branch(t, length - 15)

def draw_branch(t:turtle.Pen, length):

    # 绘制分形树
    if length > 5:
        # # 根据树枝长度决定画笔粗细
        # sz = int(length / 20)
        # if sz < 1:
        #     sz = 1
        # t.pensize(sz)

        # 乌龟沿当前方向前进length个像素，绘制主干
        t.forward(length)

        # 当前方向右转30度
        t.right(30)
        # 绘制右侧树枝
        draw_branch(t, length - 15)

        # 当前方向左转60度
        t.left(60)
        # 绘制左侧树枝
        draw_branch(t, length - 15)

        # 当前方向右转30度
        t.right(30)
        # 乌龟后退length个像素返回之前出发的位置
        t.backward(length)#


def draw_polygon(t:turtle.Pen, n, edge_len):
    i = 0
    degree = (n * 180 - 360)/n
    left_turn = 180 - degree
    while i < n:
        t.forward(edge_len)
        t.left(left_turn)
        i += 1



def draw_line(t:turtle.Pen, points:list):
    x = points[0][0]
    y = points[0][1]
    t.penup()
    t.goto(x,y)
    i = 1
    t.pendown()
    while i < len(points):
        t.goto(points[i][0], points[i][1])
        i += 1


def draw():
    # 获得画笔，海龟开始在窗口的中心，前进方向为水平方向
    t = turtle.Pen()

    # 海龟左转90度, 使其前进方向为90度
    t.left(90)
    # 笔举高，离开画布
    t.penup()
    # 后退260个像素
    t.backward(260)
    # 笔落下，接触画布
    t.pendown()
    # 设置画笔粗细
    t.pensize(1)
    # 画笔颜色
    t.pencolor('red')
    # 改变画笔形状为一只乌龟，缺省是箭头arrow，
    # 还可以为 'circle'-圆, 'square'-正方形, 'triangle'-三角形, 'classic'.
    t.shape("turtle")
    # 设置乌龟速度
    t.speed(6)


    # 调用递归函数, 绘制树枝
    draw_branch(t, 120)

    # # 画折线，给出5个点的坐标
    # points = [(0,0), (200, 0), (200, 200), (0, 200), (0,0)]
    # draw_line(t, points)
    #
    # # 画正多边形: 正6边形，边长为200
    # draw_polygon(t, 6, 200)

    # 隐藏乌龟图标
    t.hideturtle()

    # 获取屏幕对象
    screen = turtle.Screen()
    # 窗口大小
    #print(screen.window_width(), screen.window_height())
    # 得到画布
    canvas = screen.getcanvas()
    # 保存画布上的内容到文件main.eps中
    canvas.postscript(file='main.eps')
    # 等待用户点击，然后退出
    screen.exitonclick()



if __name__ == '__main__':
    #print(number)
    draw()