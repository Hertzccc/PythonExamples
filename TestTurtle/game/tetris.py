import random
import turtle
import playsound
# import os
# import threading


# 10 行
ROWS = 20
# 10 列
COLS = 10

# 已经出现的俄罗斯方块个数
seq_of_blocks = 0
# 当前得分
total_score = 0

# 世界坐标系右上角
SCREEN_X_MAX = 15
SCREEN_Y_MAX = 20
# 世界坐标系左下角
SCREEN_X_MIN = -5
SCREEN_Y_MIN = 0

# my_map[]中的某个元素是否有方块
OCCUPIED_MARK = 1
EMPTY_MARK = 0
# 是否在处理按键事件
HANDLING_KEY_PRESS = 0

# 存放已经落地的方块
my_map = []

# 依次顺时针旋转90度， I型的俄罗斯方块
# ((0, 0), (1, 0), (2, 0), (3, 0)) 表示由4个小正方形构成，
# 其中，(1, 0)表示其中的一个小正方形左下角的坐标
I_blocks = (
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 0), (0, 1), (0, 2), (0, 3)),
)

# 依次顺时针旋转90度， L型的俄罗斯方块
L_blocks = (
    ((0, 0), (1, 0), (2, 0), (0, 1)),
    ((0, 0), (0, 1), (0, 2), (1, 2)),
    ((2, 0), (0, 1), (1, 1), (2, 1)),
    ((0, 0), (1, 0), (1, 1), (1, 2)),
)

# 田字型的俄罗斯方块
O_blocks = (
    ((0, 0), (1, 0), (0, 1), (1, 1)),
)

# 依次顺时针旋转90度， S型的俄罗斯方块
S_blocks = (
    ((0, 0), (1, 0), (1, 1), (2, 1)),
    ((1, 0), (0, 1), (1, 1), (0, 2)),
)

# 依次顺时针旋转90度， Z型的俄罗斯方块
Z_blocks = (
    ((1, 0), (2, 0), (0, 1), (1, 1)),
    ((0, 0), (0, 1), (1, 1), (1, 2)),
)

# 依次顺时针旋转90度， T型的俄罗斯方块
T_blocks = (
    ((0, 0), (1, 0), (2, 0), (1, 1)),
    ((0, 0), (0, 1), (0, 2), (1, 1)),
    ((1, 0), (0, 1), (1, 1), (2, 1)),
    ((1, 0), (0, 1), (1, 1), (1, 2)),
)

# 所有可能的俄罗斯方块
TETRIS = [
    I_blocks,
    L_blocks,
    O_blocks,
    S_blocks,
    Z_blocks,
    T_blocks,
]

# 俄罗斯方块开始时的位置
X_START = 4
Y_START = ROWS - 1

# 用来提示下一个俄罗斯方块的位置(x, y)
X_NEXT = COLS + 1
Y_NEXT = int(ROWS * 0.8)

# X_SEQ = COLS + 1
# Y_SEQ = int(ROWS *0.7)

# 当前得分所在的(x, y)
X_SCORE = COLS + 1
Y_SCORE = int(ROWS * 0.6)


# (x, y, cur_block_id, next_block_id, rotate_num)
# 刚在上方出现的俄罗斯方块的位置，及其编号，及下一个方块的编号，当前俄罗斯方块的旋转角度编号
my_context = [
    X_START,
    Y_START,
    random.randint(0, len(TETRIS) - 1),
    random.randint(0, len(TETRIS) - 1),
    0,
]

# 超过这个得分时，即为胜利
WINNER_SCORE = 10


# global my_pen, my_screen
t = turtle.Pen()
hua_bu = t.getscreen()

# 从屏幕中删除海龟的绘图，海龟回到原点并设置所有变量为默认值。
moving_pen = turtle.Pen()


# 定时器周期，单位毫秒
timer_period = 1000


# 用画笔t，在(x, y)处，用颜色pen_col, 背景色fill_col, 画一个长度为1的正方形
def draw_a_block(t:turtle.Pen, x, y, pen_col, fill_col):
    # print(x, y)
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(pen_col, fill_col)
    #
    t.begin_fill()
    t.goto(x + 1, y)
    t.goto(x + 1, y + 1)
    t.goto(x, y + 1)
    t.goto(x, y)
    t.end_fill()


# 二维列表中的行号和列号(r, c) 转换成海龟画图坐标中的(x, y)
def convert_RC_to_XY(r, c):
    return c, ROWS - 1 - r


# 海龟画图坐标中的(x, y) 转换成二维列表中的行号和列号(r, c)
def convert_XY_to_RC(x, y):
    return ROWS - 1 - y, x


# 获得俄罗斯方块的水平宽度
def get_width(blocks):
    x_min = COLS
    x_max = 0
    for x, _ in blocks:
        if x > x_max:
            x_max = x
        if x < x_min:
            x_min = x
    return x_max - x_min + 1




# 在(x, y)处绘制俄罗斯方块
def draw_blocks(t:turtle.Pen, x, y, blocks):
    for (bx, by) in blocks:
        # 白笔， 绿色背景
        draw_a_block(t, x + bx, y + by, (255, 255, 255), (0, 255, 0))



# mypen负责绘制不需要经常更新的部分
def update_mypen():
    hua_bu.tracer(0)
    for r in range(ROWS):
        for c in range(COLS):
            x, y = convert_RC_to_XY(r, c)
            if my_map[r][c] == OCCUPIED_MARK:
                draw_a_block(t, x, y, (255, 255, 255), (0, 255, 0))
            else:
                draw_a_block(t, x, y, (220, 220, 220), (255, 255, 255))
    hua_bu.tracer(1)


# moving_pen负责绘制经常需要更新的部分
def update_moving_pen():
    global  my_context
    hua_bu.listen()
    # print_map()
    (cur_x, cur_y, cur_block_id, next_block_id, rotate_num) = my_context
    hua_bu.tracer(0)
    # 从屏幕中删除海龟的绘图
    moving_pen.reset()
    moving_pen.hideturtle()
    #
    blocks = TETRIS[cur_block_id][rotate_num]
    draw_blocks(moving_pen, cur_x, cur_y, blocks)
    #
    draw_blocks(moving_pen, X_NEXT, Y_NEXT, TETRIS[next_block_id][0])
    # 当前分数
    moving_pen.penup()
    moving_pen.goto(X_SCORE, Y_SCORE)
    moving_pen.pencolor((0, 0, 0))
    # moving_pen.pendown()
    # print("total_score = ", total_score)
    s = "SCORE {0}".format(total_score)
    moving_pen.write(s,align="left", font=("Arial", 12, "bold"))
    hua_bu.tracer(1)
    if total_score >= WINNER_SCORE:
        hua_bu.textinput("YOU WIN!", "Please enter your name.")
        start_game()


# 定时器，即闹钟
def handle_timer():
    # print("Timer: ", threading.currentThread().ident)
    # print("handle_timer()")
    if not HANDLING_KEY_PRESS:
        handle_Down()
    hua_bu.ontimer(handle_timer, timer_period)


# 方块落地后， 要固定位置， 添加到列表中
def fix_blocks():
    global my_context, my_map
    (cur_x, cur_y, cur_block_id, next_block_id, rotate_num) = my_context
    blocks = TETRIS[cur_block_id][rotate_num]
    min_r = ROWS
    for bx, by in blocks:
        x = cur_x + bx
        y = cur_y + by
        if 0 <= x < COLS and 0 <= y < ROWS:
            r, c = convert_XY_to_RC(x, y)
            my_map[r][c] = OCCUPIED_MARK
            if r < min_r:
                min_r = r
    return min_r


# 判断第 r 行是否已占满
def is_removable(r):
    for c in range(COLS):
        if my_map[r][c] == EMPTY_MARK:
            return False
    return True


# 删去第 row 行
def remove_row(row):
    global my_map
    # print_map()
    r = row - 1
    while r >= 0:
        for c in range(COLS):
            my_map[r + 1][c] = my_map[r][c]
        r -= 1
    for c in range(COLS):
        my_map[0][c] = EMPTY_MARK
    # print_map()


# 尝试删去已布满方块的行
def try_to_remove_rows():
    global total_score
    r = 0
    while r < ROWS:
        if is_removable(r):
            # 可以删去时，播放声音
            # playsound.playsound("./dida.mp3")
            remove_row(r)
            total_score += 1
        r += 1


# 判断如果移动后， 是否会与列表中已有的方块重叠
def is_clashing(tmp_context):
    # global my_context, my_map
    (cur_x, cur_y, cur_block_id, next_block_id, rotate_num) = tmp_context
    blocks = TETRIS[cur_block_id][rotate_num]
    for bx, by in blocks:
        x = cur_x + bx
        y = cur_y + by
        if 0 <= x < COLS and 0 <= y < ROWS:
            r, c = convert_XY_to_RC(x, y)
            if my_map[r][c] == OCCUPIED_MARK: # 落地
                return True
    return False


# 判断是否已经要着地
def is_landing():
    global my_context, my_map
    (cur_x, cur_y, cur_block_id, next_block_id, rotate_num) = my_context
    blocks = TETRIS[cur_block_id][rotate_num]
    for bx, by in blocks:
        x = cur_x + bx
        y = cur_y + by
        if 0 <= x < COLS and 0 <= y < ROWS:
            r, c = convert_XY_to_RC(x, y)
            if r == ROWS - 1 or my_map[r + 1][c] == OCCUPIED_MARK: # 落地
                return True
    return False


# 处理向上的按键, 处理俄罗斯方块的旋转
def handle_Up():
    global my_context, HANDLING_KEY_PRESS
    if HANDLING_KEY_PRESS:
        return
    HANDLING_KEY_PRESS = 1
    (cur_x, cur_y, cur_block_id, next_block_id, rotate_num) = my_context
    rotate_num += 1
    rotate_num %= len(TETRIS[cur_block_id])
    w = get_width(TETRIS[cur_block_id][rotate_num])

    if cur_x + w > COLS:
        cur_x = COLS - w
    tmp_context = (cur_x, cur_y, cur_block_id, next_block_id, rotate_num)
    if not is_clashing(tmp_context):
        my_context = tmp_context
        update_moving_pen()
    HANDLING_KEY_PRESS = 0



# 处理向下的按键， 处理俄罗斯方块的掉落
def handle_Down():
    global my_context, HANDLING_KEY_PRESS, seq_of_blocks
    if HANDLING_KEY_PRESS:
        return
    HANDLING_KEY_PRESS = 1

    (cur_x, cur_y, cur_block_id, next_block_id, rotate_num) = my_context
    if is_landing():
        min_r = fix_blocks()
        if min_r == 0:
            start_game()
            HANDLING_KEY_PRESS = 0
            return
        try_to_remove_rows()
        update_mypen()
        seq_of_blocks += 1
        # print("seq_of_blocks = ", seq_of_blocks)
        my_context = [
            X_START,
            Y_START,
            next_block_id,
            random.randint(0, len(TETRIS) - 1),
            0
        ]
    else:
        cur_y -= 1
        my_context = [
            cur_x,
            cur_y,
            cur_block_id,
            next_block_id,
            rotate_num
        ]

    update_moving_pen()
    HANDLING_KEY_PRESS = 0


# 处理向左的按键， 处理俄罗斯方块的左移
def handle_Left():
    global my_context, HANDLING_KEY_PRESS
    # print("handle_Left: ", threading.currentThread().ident)
    if HANDLING_KEY_PRESS:
        return
    HANDLING_KEY_PRESS = 1
    (cur_x, cur_y, cur_block_id, next_block_id, rotate_num) = my_context
    tmp_context = (cur_x - 1, cur_y, cur_block_id, next_block_id, rotate_num)
    if cur_x > 0 and not is_clashing(tmp_context):
        cur_x -= 1
        my_context = (cur_x, cur_y, cur_block_id, next_block_id, rotate_num)
        update_moving_pen()
    HANDLING_KEY_PRESS = 0


# 处理向右的按键， 处理俄罗斯方块的右移
def handle_Right():
    global my_context, HANDLING_KEY_PRESS
    if HANDLING_KEY_PRESS:
        return
    HANDLING_KEY_PRESS = 1
    (cur_x, cur_y, cur_block_id, next_block_id, rotate_num) = my_context
    tmp_context = (cur_x + 1, cur_y, cur_block_id, next_block_id, rotate_num)
    blocks = TETRIS[cur_block_id][rotate_num]
    w = get_width(blocks)
    if cur_x < COLS - w and not is_clashing(tmp_context):
        cur_x += 1
        my_context = (cur_x, cur_y, cur_block_id, next_block_id, rotate_num)
        update_moving_pen()
    HANDLING_KEY_PRESS = 0


# 设置游戏需要用到的相关数据
def start_game():
    global HANDLING_KEY_PRESS, total_score, seq_of_blocks
    HANDLING_KEY_PRESS = 0
    total_score = 0
    seq_of_blocks = 0
    gen_maps()
    # print_map()

    #
    hua_bu.tracer(0)
    for r in range(ROWS):
        for c in range(COLS):
            x, y = convert_RC_to_XY(r, c)
            if my_map[r][c] == OCCUPIED_MARK:
                # 白色画笔，绿色背景
                draw_a_block(t, x, y, (255, 255, 255), (0, 255, 0))
            else:
                # 灰色画笔，白色背景
                draw_a_block(t, x, y, (220, 220, 220), (255, 255, 255))
    hua_bu.tracer(1)


# 初始化界面，键盘和定时器
def init():
    hua_bu.colormode(255)
    hua_bu.setup(600, 600, 0, 0)
    hua_bu.setworldcoordinates(SCREEN_X_MIN, SCREEN_Y_MIN, SCREEN_X_MAX, SCREEN_Y_MAX)
    t.hideturtle()
    moving_pen.hideturtle()
    t.speed(0)
    hua_bu.title("Tetris")

    start_game()


    # 键盘
    hua_bu.onkey(handle_Up, "Up")
    hua_bu.onkeypress(handle_Down, "Down")
    hua_bu.onkey(handle_Left, "Left")
    hua_bu.onkey(handle_Right, "Right")
    hua_bu.listen()

    # 定时器
    handle_timer()


# 生成全部为0的List, 共ROWS 行 COLS 列
def gen_maps():
    my_map.clear()
    for r in range(ROWS):
        my_map.append([])
        for c in range(COLS):
            my_map[r].append(EMPTY_MARK)
            # if r < 8:
            #     my_map[r].append(EMPTY_MARK)
            # else:
            #     my_map[r].append(OCCUPIED_MARK)

    return my_map


# 判断当前行是否全为0
def is_zero_row(r):
    for c in range(COLS):
        if my_map[r][c] != EMPTY_MARK:
            return False
    return True


# 输出 ROWS行 COLS 列的List
def print_map():
    print("\n")
    for r in range(ROWS):
        if is_zero_row(r):
            continue
        s = ""
        for c in range(COLS):
            s += "\t{0}".format(my_map[r][c])
        print(s + "\n")
    print("\n")




def main():
    # 初始化
    init()
    # 开始事件循环, 作为一个海龟绘图程序的结束语句
    hua_bu.mainloop()



if __name__ == '__main__':
    main()

