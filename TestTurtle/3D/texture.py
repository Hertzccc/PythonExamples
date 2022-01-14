import sys

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import random

x_degree = 90.0
y_degree = 0.0
z_degree = 0.0


# 记录3维空间上的6个面，每个面有4个点，每个点对应2维图片上的一个点
vertices = [
    ((0.0, 0.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 1.0, 0.0), (1.0, 1.0, 0.0, 1.0, 1.0), (0.0, 1.0, 0.0, 0.0, 1.0)),
    ((0.0, 0.0, 0.0, 0.0, 0.0), (1.0, 0.0, 0.0, 1.0, 0.0), (1.0, 0.0, -1.0, 1.0, 1.0), (0.0, 0.0, -1.0, 0.0, 1.0)),
    ((1.0, 0.0, 0.0, 0.0, 0.0), (1.0, 1.0, 0.0, 1.0, 0.0), (1.0, 1.0, -1.0, 1.0, 1.0), (1.0, 0.0, -1.0, 0.0, 1.0)),
    ((1.0, 1.0, 0.0, 0.0, 0.0), (0.0, 1.0, 0.0, 1.0, 0.0), (0.0, 1.0, -1.0, 1.0, 1.0), (1.0, 1.0, -1.0, 0.0, 1.0)),
    ((0.0, 1.0, 0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0, 0.0), (0.0, 0.0, -1.0, 1.0, 1.0), (0.0, 1.0, -1.0, 0.0, 1.0)),
    ((0.0, 0.0, -1.0, 0.0, 0.0), (1.0, 0.0, -1.0, 1.0, 0.0), (1.0, 1.0, -1.0, 1.0, 1.0), (0.0, 1.0, -1.0, 0.0, 1.0)),

    # ((-1.0, -1.0, 1.0, 0.0, 0.0), (1.0, -1.0, 1.0, 1.0, 0.0), (1.0, 1.0, 1.0, 1.0, 1.0), (-1.0, 1.0, 1.0, 0.0, 1.0)),
    # ((-1.0, -1.0, -1.0, 0.0, 0.0), (-1.0, 1.0, -1.0, 1.0, 0.0), (1.0, 1.0, -1.0, 1.0, 1.0), (1.0, -1.0, -1.0, 0.0, 1.0)),
    # ((-1.0, 1.0, -1.0, 0.0, 0.0), (-1.0, 1.0, 1.0, 1.0, 0.0), (1.0, 1.0, 1.0, 1.0, 1.0), (1.0, 1.0, -1.0, 0.0, 1.0)),
    # ((-1.0, -1.0, -1.0, 0.0, 0.0), (1.0, -1.0, -1.0, 1.0, 0.0), (1.0, -1.0, 1.0, 1.0, 1.0), (-1.0, -1.0, 1.0, 0.0, 1.0)),
    # ((1.0, -1.0, -1.0, 0.0, 0.0), (1.0, 1.0, -1.0, 1.0, 0.0), (1.0, 1.0, 1.0, 1.0, 1.0), (1.0, -1.0, 1.0, 0.0, 1.0)),
    # ((-1.0, -1.0, -1.0, 0.0, 0.0), (-1.0, -1.0, 1.0, 1.0, 0.0), (-1.0, 1.0, 1.0, 1.0, 1.0), (-1.0, 1.0, -1.0, 0.0, 1.0)),
]


# 绘制图形
def Draw():
    global x_degree, y_degree, z_degree
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glEnable(GL_DEPTH_TEST)
    glLoadIdentity()
    # 透视投影时：
    #   沿z轴平移，z轴正向指向观察者，
    #   观察者的视线是沿z轴负的方向，
    #   当z坐标越小时，表示物体离观察者越远，物体看起来要更小(-20.0比-10.0更小)
    # 正射投影时：
    #   只要在剪切范围内，修改z坐标后，所看到的3维图形没有发生变化.
    glTranslate(0.0, 0.0, -10.0)
    # 分别绕x,y,z轴旋转
    glRotatef(x_degree, 1.0, 0.0, 0.0)
    glRotatef(y_degree, 0.0, 1.0, 0.0)
    glRotatef(z_degree, 0.0, 0.0, 1.0)
    # 立方体有6个面，i表示第i个面
    i = 0
    while i < len(vertices):
        # 开始绘制立方体的每个面，同时设置纹理映射
        glBindTexture(GL_TEXTURE_2D, i)
        # 绘制3维空间中的一个四边形
        glBegin(GL_QUADS)
        # 立方体的每个面有4个顶点, j表示第j个顶点
        j = 0
        vi = vertices[i]
        while j < len(vi):
            x3, y3, z3, x2, y2 = vi[j]
            # 设置纹理坐标
            glTexCoord2f(x2, y2)
            # 绘制顶点
            glVertex3f(x3, y3, z3)
            j += 1
        i += 1
        # 维空间中的一个四边形绘制结束
        glEnd()

    # 刷新屏幕，产生动画效果
    glutSwapBuffers()

    # 修改各坐标轴的旋转角度，通过random.random()随机产生一个0到1之间的小数
    x_degree += random.random()/5
    y_degree += random.random()/5
    z_degree += random.random()/5


# 加载纹理
def load_texture():
    # 提前准备好的6个图片: 1.jpg, 2.jpg, ..., 6.jpg
    imgFiles = ['./pic/' + str(i) + '.jpg' for i in range(1, 7)]
    for i in range(6):
        # 从外存加载图片
        img = Image.open(imgFiles[i])
        width, height = img.size
        img = img.tobytes('raw', 'RGBX', 0, -1)
        # 生成并设置纹理(相当于物体表面上的贴图）
        glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, i)
        glTexImage2D(GL_TEXTURE_2D, 0, 4,
                     width, height, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, img)
        glTexParameterf(GL_TEXTURE_2D,
                        GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D,
                        GL_TEXTURE_MIN_FILTER, GL_NEAREST)


# 初始化opengl的相关设置
def init_opengl(width, height):
    load_texture()
    glEnable(GL_TEXTURE_2D)
    # 蓝色背景 (红，绿，蓝，透明度)
    glClearColor(0.0, 0.0, 1.0, 0.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    # 背面剔除，消隐
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_POLYGON_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
    glHint(GL_POLYGON_SMOOTH_HINT, GL_FASTEST)
    glLoadIdentity()

    # https://learnopengl-cn.readthedocs.io/zh/latest/01%20Getting%20started/08%20Coordinate%20Systems/
    # (1) 观察的角度为45.0
    # (2) float(width) / float(height) 代表窗口的宽与高的比例
    #     透视投影，远小近大（3维空间里的相同长度和方向的两条边，远处的边在投影后要更短）,
    # (3) 指定要绘制的空间范围，近远剪切平面即距离观察者的距离分别为0.1和100
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)

    # 正射投影：分别在远处的边和近处的, 具有相同长度和方向的两条边, 在投影之后仍然一样长，看起来没有“远小近大”的效果
    # glOrtho(-4.0, 4.0, -3.0, 3.0, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


# 实始化窗口的相关设置
def init(width=800, height=600, title='Texture'):
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(title)
    init_opengl(width, height)
    glutDisplayFunc(Draw)
    # 指定窗口空闲时，调用Draw函数进行绘制
    glutIdleFunc(Draw)


if __name__ == '__main__':
    init()
    glutMainLoop()
