#####################################################################
#
# author:  sheisc@163.com
#
#####################################################################
# import util.clone
import os

X_MAX = 9
Y_MAX = 9

PASS_MARK = 0
BLOCK_MARK = 1
EXIT_MARK = 7

RIGHT = 2
DOWN = 3
LEFT = 4
UP = 5

HAS_FINISHED = False

map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 0, 1],  # 5
    [1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 10
]

stack = []

def is_legal(r, c):
    return (c >= 0) and (c <= X_MAX) and (r >= 0) and (r <= Y_MAX)


def is_passable(m, r, c):
    return is_legal(r, c) and (m[r][c] == PASS_MARK or m[r][c] == EXIT_MARK)


def set_value(m, r, c, val):
    m[r][c] = val


def get_value(m, r, c):
    return m[r][c]



def print_map(m):
    for row in m:
        i = 0
        s = ""
        while i < len(row):
            val = row[i]
            if val == RIGHT:
                s += ("\t{0:c}".format(0x2192))
            elif val == DOWN:
                s += ("\t{0:c}".format(0x2193))
            elif val == LEFT:
                s += ("\t{0:c}".format(0x2190))
            elif val == UP:
                #s += ("\t{0:c}".format(0x2191))
                s += ("\t{0:c}".format(0x2613))
            elif val == EXIT_MARK:
                s += ("\t{0:c}".format(0x270C))
            elif val == BLOCK_MARK:
                s += "\t1"
            else:
                s += "\t0"
            i += 1
        print(s+"\n")


def explore(map, loop_once=False):
    global HAS_FINISHED
    while len(stack) > 0:
        n = len(stack)
        state = stack[n - 1]
        r = state[0]
        c = state[1]
        val = get_value(map, r, c)

        if val == EXIT_MARK:
            HAS_FINISHED = True
            print("\n********************** Mission Complete *********************\n")
            break

        if val == PASS_MARK:
            if is_passable(map, r, c + 1):
                stack.append([r, c + 1])
            set_value(map, r, c, RIGHT)
        elif val == RIGHT:
            if is_passable(map, r + 1, c):
                stack.append([r + 1, c])
            set_value(map, r, c, DOWN)
        elif val == DOWN:
            if is_passable(map, r, c - 1):
                stack.append([r, c - 1])
            set_value(map, r, c, LEFT)
        elif val == LEFT:
            if is_passable(map, r - 1, c):
                stack.append([r - 1, c])
            set_value(map, r, c, UP)
        else: # We have explored the NORTH direction
            stack.pop()


        print("\nSTACK: \n")
        print(stack)
        print("\nMAP:\n")
        print_map(map)
        print("")

        if loop_once:
            break


# map = [
#     [1,1,1,1,1,1,1,1,1,1],
#     [0,0,0,0,0,0,0,0,0,1],
#     [1,0,0,0,1,1,1,1,0,1],
#     [1,1,1,0,0,0,1,0,0,1],
#     [1,0,0,0,1,1,1,1,0,1],  # 5
#     [1,0,1,1,1,1,1,0,0,1],
#     [1,0,1,0,0,1,1,0,0,1],
#     [1,0,1,1,0,0,0,1,1,1],
#     [1,0,0,0,0,0,0,0,0,7],
#     [1,1,1,1,1,1,1,1,1,1],  # 10
# ]


# # RIGHT
# print("{0:c}".format(0x2192))
# # DOWN
# print("{0:c}".format(0x2193))
# # LEFT
# print("{0:c}".format(0x2190))
# # UP
# print("{0:c}".format(0x2191))
# # CROSS
# print("{0:c}".format(0x00D7))
# # VICTORY
# print("{0:c}".format(0x270C))
#
# print("\n Right {0:c} \t Down {1:c} \t Left {2:c} \t Up {3:c} \t Cross {4:c} \t VICTORY {5:c}".format(
#     0x2192, 0x2193, 0x2190, 0x2191, 0x00D7, 0x270C))

def main():
    sub_dir = os.getcwd()
    print(sub_dir)
    stack.append((1, 0))
    explore(map)



if __name__ == '__main__':
    main()
