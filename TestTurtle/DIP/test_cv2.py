# encoding:utf-8

import cv2
# import numpy as np
# import matplotlib.pyplot as plt


def face_detection():

    cap = cv2.VideoCapture(0) # 使用第0个摄像头
    face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml') # 加载人脸特征库

    while(True):
        ret, frame = cap.read() # 读取一帧的图像
        if not ret:
            frame = cv2.imread('./data/lena.jpg')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 转灰

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(5, 5)) # 检测人脸
        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2) # 用矩形圈出人脸

        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # print("next frame")


    cap.release() # 释放摄像头
    cv2.destroyAllWindows()

def main():
    # 读取图片
    lena = cv2.imread('./data/lena.jpg')
    sea = cv2.imread('./data/sea.jpg')
    # 调整图片大小, 使两张图片都为512 * 512
    lena = cv2.resize(lena, (512, 512), interpolation=cv2.INTER_CUBIC)
    sea = cv2.resize(sea, (512, 512), interpolation=cv2.INTER_CUBIC)
    # 图像融合
    # dst = lena * alpha + sea * beta + gamma
    result = cv2.addWeighted(lena, 0.5, sea, 0.5, 0)
    # 显示图像
    cv2.imshow("lean", lena)
    cv2.imshow("sea", sea)
    cv2.imshow("result", result)
    # 保存融合后的图片
    cv2.imwrite("./data/result.jpg", result)
    # 等待用户按键
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    # main()
    face_detection()
