# -*- coding: utf-8 -*-

import cv2

# 最簡單的以灰度直方圖作為相似比較的實現
def compareImage(image1, image2, size=(256, 256)):
    # 先計算直方圖
    # 幾個引數必須用方括號括起來
    # 這裡直接用灰度圖計算直方圖，所以是使用第一個通道，
    # 也可以進行通道分離後，得到多個通道的直方圖
    # bins 取為16
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 可以比較下直方圖
    #plt.plot(range(256), hist1, 'r')
    #plt.plot(range(256), hist2, 'b')
    #plt.show()
    # 計算直方圖的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree[0]

# 計算單通道的直方圖的相似值
def compareImage2(image1, image2):
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 計算直方圖的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree[0]

if __name__ == '__main__':
    img1 = cv2.imread('chk_imgs/02.png')
    img2 = cv2.imread('chk_imgs/02-1.png')
    img3 = cv2.imread('chk_imgs/02-2.png')
    img4 = cv2.imread('chk_imgs/01.png')
    img5 = cv2.imread('chk_imgs/03.png')
    img6 = cv2.imread('chk_imgs/04.png')

    print(compareImage(img1, img2), compareImage2(img1, img2))
    print(compareImage(img1, img3), compareImage2(img1, img3))
    print(compareImage(img1, img4), compareImage2(img1, img4))
    print(compareImage(img1, img5), compareImage2(img1, img5))
    print(compareImage(img1, img6), compareImage2(img1, img6))

    cv2.waitKey(0)
