# encoding:utf-8

# 操作系统相关函数
import os

# 图像处理/展现的相关函数库
import matplotlib.pyplot as painter
import PIL




def main():
    # 获取当前目录
    root_dir = os.getcwd()
    print(root_dir)
    # 当前目录/data
    data_path = os.path.join(root_dir, 'data')
    # 测试用的图像
    lena_dir = os.path.join(data_path, 'lena.jpg')
    sea_dir = os.path.join(data_path, 'sea.jpg')
    # 载入图像
    lena_img = PIL.Image.open(lena_dir)
    sea_img = PIL.Image.open(sea_dir)


    # 逆时针旋转 45 度, 根据需要放大图片
    rot_img = lena_img.rotate(45, expand=1)
    # 调整图片大小为512 * 512, 因为 sea.jpg为512 * 512，
    # 要进行图片融合，需要把两张图片处理成一样大
    rot_img = rot_img.resize((512,512))

    # 图像融合
    # result_img = lena_img * (1 – alpha) + sea_img* alpha
    blend_img = PIL.Image.blend(rot_img, sea_img, 0.5)


    # 存储图像
    rot_img.save(os.path.join(data_path, 'rotate.jpg'))
    blend_img.save(os.path.join(data_path, 'blend.jpg'))


    #plt.subplot(221)
    # 显示图片  2行 * 2列, 占用第1个
    painter.subplot(2, 2, 1)
    painter.title("Lena")
    painter.imshow(lena_img)
    # 不显示坐标轴
    painter.axis('off')
    #plt.show()

    # 显示图片  2行 * 2列, 占用第2个
    painter.subplot(2, 2, 2)
    # 设置标题
    painter.title("Sea")
    # 在图中显示图片sea_img
    painter.imshow(sea_img)
    # 不显示坐标轴
    painter.axis('off')

    # 显示图片  2行 * 2列, 占用第3个
    painter.subplot(2, 2, 3)
    painter.title("Rotate")
    painter.imshow(rot_img)
    # 不显示坐标轴
    painter.axis('off')

    # 显示图片  2行 * 2列, 占用第4个
    painter.subplot(2, 2, 4)
    painter.title("Blend")
    painter.imshow(blend_img)
    # 不显示坐标轴
    painter.axis('off')

    # 保存图片
    fig = painter.gcf()
    fig.savefig(os.path.join(data_path, 'figure.png'))
    # fig.suptitle("Python Image Library")
    # 显示整个图
    painter.show()



if __name__ == "__main__":
    main()

