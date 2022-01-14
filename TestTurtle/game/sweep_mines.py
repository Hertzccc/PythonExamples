#####################################################################
#
# author:  sheisc@163.com
#
#####################################################################

import random
import turtle


# 10 行
ROWS = 10
# 10 列
COLS = 10

MINES_PERCENTAGE = 0.2
# 地雷数
NUM_OF_MINES = int(ROWS * COLS * MINES_PERCENTAGE)

GRID_X_MAX = COLS
GRID_Y_MAX = ROWS

# SCREEN_X_MAX = GRID_X_MAX * 3 / 2
# SCREEN_Y_MAX = GRID_Y_MAX * 3 / 2
# SCREEN_X_MIN = -GRID_X_MAX / 2
# SCREEN_Y_MIN = -GRID_Y_MAX / 2

SCREEN_X_MAX = GRID_X_MAX * 6 / 5
SCREEN_Y_MAX = GRID_Y_MAX * 6 / 5
SCREEN_X_MIN = -GRID_X_MAX / 5
SCREEN_Y_MIN = -GRID_Y_MAX / 5

NO_FLAG = 0
OPEN_FLAG = 1
YELLOW_FLAG = 2

MINE_MARK = -1
GAME_OVER = False
map = []
flags = []


# global my_pen, my_screen
my_pen = turtle.Pen()
my_screen = my_pen.getscreen()

total_open_count = 0



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


def set_open_flag(r, c):
    global total_open_count
    if flags[r][c] != OPEN_FLAG:
        total_open_count += 1
        # print(total_open_count)
        flags[r][c] = OPEN_FLAG
    # print("total_open_count = ", total_open_count)


def draw_number_of_mines(x, y):
    r, c = convert_XY_to_RC(x, y)
    draw_a_block(x, y, "white")
    my_pen.penup()
    my_pen.goto(x + 0.4, y + 0.2)
    my_pen.write(map[r][c], align="left", font=("Arial", 10, "normal"))
    set_open_flag(r, c)


def open_empty_grids(r, c):
    if 0 <= r < ROWS and 0 <= c < COLS:
        x, y = convert_RC_to_XY(r, c)
        if flags[r][c] != OPEN_FLAG:
            if map[r][c] == 0:
                set_open_flag(r, c)
                draw_a_block(x, y, (255, 255, 255))
                open_empty_grids(r - 1, c - 1)
                open_empty_grids(r - 1, c)
                open_empty_grids(r - 1, c + 1)
                open_empty_grids(r, c - 1)
                open_empty_grids(r, c + 1)
                open_empty_grids(r + 1, c - 1)
                open_empty_grids(r + 1, c)
                open_empty_grids(r + 1, c + 1)
            elif map[r][c] > 0:
                draw_number_of_mines(x, y)


def is_finished():
    global GAME_OVER
    if total_open_count == (COLS * ROWS - NUM_OF_MINES):
        # print("total_open_count = ", total_open_count)
        my_screen.textinput("YOU WIN !", "Please enter your name:")
        # save("sweep_mines.eps")
        GAME_OVER = True



def handle_left_click(sx, sy):
    global GAME_OVER, total_open_count
    # print("def handle_left_click(", sx, ",", sy, ")")
    if 0.0 <= sx < GRID_X_MAX and 0.0 <= sy < GRID_Y_MAX:
        x = int(sx)
        y = int(sy)
        #
        if GAME_OVER:
            return
        my_screen.tracer(0)
        # print(x, y)
        r, c = convert_XY_to_RC(x, y)
        if flags[r][c] != OPEN_FLAG:
            if map[r][c] == MINE_MARK:
                GAME_OVER = True
                draw_a_block(x, y, (255, 0, 0))
                save("sweep_mines.eps")
                my_screen.textinput("GAME OVER !", "Do you want to play again?")
                return

            elif map[r][c] == 0:  # 显示没有地雷的连通的多个空位置
                open_empty_grids(r, c)
            else: # 显示地雷的个数
                draw_number_of_mines(x, y)
        my_screen.tracer(1)
        is_finished()

    else:   # 在空白处点击，则重新开始游戏
        if GAME_OVER:
            repaint()




def handle_right_click(sx, sy):
    # print("def handle_right_click(", sx, ",", sy, ")")
    if 0.0 <= sx < GRID_X_MAX and 0.0 <= sy < GRID_Y_MAX and not GAME_OVER:
        x = int(sx)
        y = int(sy)
        my_screen.tracer(0)
        r, c = convert_XY_to_RC(x, y)
        if 0 <= r < ROWS and 0 <= c < COLS:
            if flags[r][c] != OPEN_FLAG:
                # flags[r][c] = not flags[r][c]
                if flags[r][c] == NO_FLAG:
                    flags[r][c] = YELLOW_FLAG
                    draw_a_block(x, y, "yellow")
                elif flags[r][c] == YELLOW_FLAG:
                    flags[r][c] = NO_FLAG
                    draw_a_block(x, y, (0, 255, 0))
        my_screen.tracer(1)




def is_contained(mines, x, y):
    for xi, yi in mines:
        if xi == x and yi == y:
            return True
    return False


def get_num_of_mines(r, c):
    count = 0
    for ri in range(r - 1, r + 2):
        for ci in range(c - 1, c + 2):
            if 0 <= ri < ROWS and 0 <= ci < COLS:
                if map[ri][ci] == MINE_MARK:
                    count += 1
    return count

# 1，2, 3, 4, 5, 6,7, 8 , 9, 10

def gen_mines(count):
    i = 0;
    mines = []
    while i < count:
        x = random.randint(0, GRID_X_MAX - 1)
        y = random.randint(0, GRID_Y_MAX - 1)
        if is_contained(mines, x, y):
            continue
        else:
            mines.append((x, y))
            r, c = convert_XY_to_RC(x, y)
            map[r][c] = MINE_MARK
            i += 1

    for x in range(GRID_X_MAX):
        for y in range(GRID_Y_MAX):
            r, c = convert_XY_to_RC(x, y)
            if map[r][c] != MINE_MARK:
                map[r][c] = get_num_of_mines(r, c)

    print_map()


def repaint():
    # 禁止海龟动画
    global GAME_OVER, total_open_count
    GAME_OVER = False
    total_open_count = 0
    my_screen.tracer(0)
    for x in range(GRID_X_MAX):
        for y in range(GRID_Y_MAX):
            draw_a_block(x, y, (0, 255, 0))
    my_screen.tracer(1)

    gen_maps()


def cheat():
    if GAME_OVER:
        return

    for x in range(GRID_X_MAX):
        for y in range(GRID_Y_MAX):
            r, c = convert_XY_to_RC(x, y)
            if map[r][c] == MINE_MARK:
                handle_right_click(x, y)

    for x in range(GRID_X_MAX):
        for y in range(GRID_Y_MAX):
            r, c = convert_XY_to_RC(x, y)
            if map[r][c] != MINE_MARK:
                handle_left_click(x, y)



def handle_middle_click(x, y):
    cheat()


# 初始化
def init():
    my_screen.colormode(255)
    my_screen.setup(600, 600, 0, 0)
    my_screen.setworldcoordinates(SCREEN_X_MIN, SCREEN_Y_MIN, SCREEN_X_MAX, SCREEN_Y_MAX)
    my_pen.hideturtle()
    my_pen.speed(0)
    my_screen.title("Sweep Mines")

    # repaint()
    # print_maps()
    # 添加左键点击的事件处理函数
    my_screen.onclick(handle_left_click, btn=1, add=True)
    # 添加右键点击的事件处理函数
    my_screen.onclick(handle_right_click, btn=3, add=True)
    # 添加中间滚轮按键点击的事件处理函数
    my_screen.onclick(handle_middle_click, btn=2, add=True)


def gen_maps():
    # global  total_open_count
    map.clear()
    flags.clear()
    for r in range(ROWS):
        map.append([])
        flags.append([])
        for c in range(COLS):
            map[r].append(0)
            flags[r].append(NO_FLAG)
    # 生成地雷
    gen_mines(NUM_OF_MINES)
    #
    # total_open_count = 0
    return map


def print_map():
    print("\n")
    for r in range(ROWS):
        s = ""
        for c in range(COLS):
            s += "\t{0}".format(map[r][c])
        print(s + "\n")
    print("\n")


# 保存绘图的结果
def save(filename):
    canvas = my_screen.getcanvas()
    # 保存画布上的内容到文件main.eps中
    canvas.postscript(file=filename)


def main():
    # 初始化
    init()
    #
    repaint()
    # cheat()

    # 开始事件循环, 作为一个海龟绘图程序的结束语句
    my_screen.mainloop()



if __name__ == '__main__':
    # main()
    main()

