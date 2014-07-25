# -*- coding: utf-8 -*-

import cv2
import cv2.cv as cv
import numpy as np


if __name__ == '__main__':

    file_in = 'pic.jpg'

    print "> 이미지 로딩"
    img_color = cv2.imread(file_in)
    img_gray = cv2.cvtColor(img_color, cv.CV_RGB2GRAY)
    img_gray = cv2.equalizeHist(img_gray)
    print "  --> ok : ", file_in, img_gray.shape

    print "> 얼굴인식 ..."
    cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    detected_rects = cascade.detectMultiScale(img_gray,
                                     scaleFactor=1.3,
                                     minNeighbors=4,
                                     minSize=(20, 20),
                                     flags=cv.CV_HAAR_SCALE_IMAGE)

    # 인식된 얼굴 없음
    if len(detected_rects) == 0:
        print "  --> fail to detect faces!"
        exit(1)

    # 얼굴인식 성공
    print "  --> ok : ", len(detected_rects), " faces detected!"

    # 상대좌표 --> 절대좌표
    detected_rects[:, 2:] += detected_rects[:, :2]

    count = 0
    img_faces = ""
    # 인식된 얼굴을 모두 옆으로 붙여 하나의 이미지로 만든다.
    for x1, y1, x2, y2 in detected_rects:
        img_face = img_color[y1:y2, x1:x2]
        # 같은 사이즈로 붙이기 위해 리사이징
        resized_image = cv2.resize(img_face, (100, 100))
        if count == 0:
            img_faces = resized_image
        else:
            img_faces = np.concatenate((img_faces, resized_image), axis=1)

        count += 1

    # 최종 인식된 얼굴 show !!
    cv2.imshow('img_face', img_faces)

    # 키를 누를 때까지 프로그램이 종료되지 않도록 대기
    cv2.waitKey(0)
    cv2.destroyAllWindows()


