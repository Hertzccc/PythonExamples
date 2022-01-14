from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = 'OpenGL Python Teapot'
x_degree = 180
y_degree = 0 #-45
z_degree = 0

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 800)
    glutCreateWindow(name)

    glClearColor(0., 0., 1., 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [-20., 2., -2., 1.]
    lightZeroColor = [1.8, 1.0, 0.8, 1.0]  # green tinged
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)
    glutDisplayFunc(display)
    # glutIdleFunc(display)
    timer()
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40., 1., 1., 40.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0, 0, 10,
              0, 0, 0,
              0, 1, 0)
    glPushMatrix()
    glutMainLoop()
    return


def timer(value=0):
    display()
    glutTimerFunc(20, timer, 0)


def display():
    global  x_degree, y_degree, z_degree
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [1.0, 0., 0., 1.]
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)

    glTranslatef(0.0, 0.0, -6.0)

    # 绕X轴旋转
    glRotatef(x_degree, 1, 0, 0);
    # 绕Y轴旋转
    # glRotatef(y_degree, 0, 1, 0);
    # 绕Z轴旋转
    #glRotatef(z_degree, 0, 0, 1);

    # 茶壶
    # glutSolidTeapot(2.0) #, 20, -20)
    glutWireTeapot(1.0)

    # 球
    glTranslatef(3.0, 3.0, 0.0)
    glutSolidSphere(1, 50, 50);

    # 圆锥体
    glTranslatef(-6.0, -6.0, 0.0)
    glutSolidCone(1, 2, 50, 50)

    # 类似于甜甜圈的环面
    glTranslatef(6.0, 0.0, 0.0)
    glutWireTorus(0.4, 0.8, 10, 50)

    # 四面体
    glTranslatef(-6.0, 6.0, 0.0)
    glutSolidTetrahedron()




    x_degree -= 1
    y_degree -= 1
    z_degree -= 1
    glPopMatrix()
    glutSwapBuffers()

    return


if __name__ == '__main__':
    main()
