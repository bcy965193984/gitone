import os
import sys
import cv2
import matplotlib.pyplot as plt
import numpy as np
cwd=sys.argv[0]
#cwd=cwd+"\\.."
########拼接大图###########
path = rf'{cwd}\..\cameras'  # 刚拍完等待拼接图像的文件夹
images = []
# 遍历子文件夹下的图片名称
myList = os.listdir(path)
# 输出子文件内有多少张图片
print(f'total number of images detected {len(myList)}')
# 读取每张图片
for imgName in myList:
    curImg = cv2.imread(f'{path}/{imgName}')
    images.append(curImg)  # 将每个子文件夹下的图片存进images数组中

# 拼接这些图片，得到一张大图
stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)  # 创建一个stitcher实例
(status, bigimg) = stitcher.stitch(images)
if (status == 0):  # 状态码为0的时候，进行处理
    print('Panorma Generated')
    Img_Name = rf'{cwd}\..\Image mosaicking\bigimg.png'#拼接完大图的存放位置
    cv2.imwrite(Img_Name,bigimg)#保存到指定文件夹
else:
    print('Panorma Generated Unsuccessful')

##########图像匹配并矫正#########
# 匹配多个对象
# bigimg = cv2.imread('C:\\Users\\15539.DESKTOP-NVHRE6B\\Desktop\\project\\tong\\wd\\1.png')#拼接完的大图
icon = cv2.imread(rf'{cwd}\..\features\1.png')  # 匹配的模板
bigimg_gray = cv2.cvtColor(bigimg, cv2.COLOR_BGR2GRAY)
icon_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)
h1, w1 = icon.shape[:2]

res = cv2.matchTemplate(bigimg_gray, icon_gray, cv2.TM_CCOEFF_NORMED)
threshold = 0.8

loc = np.where(res >= threshold)

p = 0
t = 0
b = 1

for pt in zip(*loc[::-1]):  # *号表示可选参数
    if (p != 0 and t != 0):
        if (pt[0] < p + 10 and pt[0] > p - 10 and pt[1] < t + 10 and pt[1] > t - 10):  # 把重复的去掉
            continue
    bottom_right = (pt[0] + w1, pt[1] + h1)  # pt[0]，pt[1]为定位图像最左上角坐标

    p = pt[0]
    t = pt[1]

    # 根据截取的板槽进行矫正
    inputPts = np.float32([[p - 203, t - 148], [p - 126, t - 182],
                           [p + 5, t + 55], [p + 97, t + 3]])
    outputPts = np.float32([[0, 0], [80, 0],
                            [0, 330], [80, 330]])

    M = cv2.getPerspectiveTransform(inputPts, outputPts)  # 位置关系
    dst = cv2.warpPerspective(bigimg, M, (80, 330))
    # bigimg = np.hstack((bigimg,dst))#横着拼
    Img_Name =rf'{cwd}\..\results\\' + str(b) + '.png'  # 存放矫正完图像的文件夹
    b = b + 1
    cv2.imwrite(Img_Name, dst)  # 保存到指定文件夹

###########测量温度############
paths = rf'{cwd}\..\results' # 矫正完的文件夹
image = []
# 遍历子文件夹下的图片名称
myLists = os.listdir(paths)
# 输出子文件内有多少张图片
print(f'total number of images detected {len(myLists)}')
c = 1
# 读取每张图片
for imgName in myLists:
    img = cv2.imread(f'{paths}/{imgName}')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度
    x, y = img.shape[:2]
    copy = img.copy()


    def get_tem(x, y):  # 得到x,0到x,80所有点灰度值的最大值
        max_tem = 0  # 最大灰度值
        max_i = 0  # 最大灰度值时的y坐标
        for i in range(y):
            wd = gray_img[x, i]  # 获得固定点灰度值,x和y得反过来
            if (max_tem < wd):
                max_tem = wd
                max_i = i
        return max_tem, max_i

    t = x / 55  # 每一块包括的像素点数量
    s = []  # 存放每一块的最大灰度值
    for i in range(1, 56):  #
        res, max_i = get_tem(int((i - 0.5) * t), y)
        # print(res)
        s.append(res)

        # 看看最高温度点是在哪里取到的
        # cv2.line(copy, (max_i, int((i - 0.5) * t)), (max_i,int((i - 0.5) * t)), (0, 0, 255),5)#划线看看是否分正确了
    # plt.imshow(copy[:,:,::-1])
    # plt.show()

    print("------")
    for i in range(55):  # 分55行
        if (s[i] > 230):
            print(i + 1)
            cv2.line(copy, (0, int((i - 0.5) * t)), (80, int((i - 0.5) * t)), (0, 255, 255), 2)  # 划线看看是否分正确了

    print("*****")
    for i in range(5):  # 分5个区域
        ave = 0
        for j in range(i * 11, i * 11 + 11):  # 算出每11块的平均值
            ave = ave + s[j];
        ave = ave / 11  # 算出每11块的平均值
        for j in range(i * 11, i * 11 + 11):  # 如果有超出10%的，就预警
            if (s[j] > ave * 1.03):
                print(j + 1)
                cv2.line(copy, (0, int((j - 0.5) * t)), (80, int((j - 0.5) * t)), (0, 0, 255), 2)  # 划线看看是否分正确了
    cv2.imwrite(rf'{cwd}\..\drawed\\' + str(c) + '.png', copy)
    c = c + 1

##########拼图#########
path1 = rf'{cwd}\..\drawed'  # 画完的文件夹
image1 = []
# 遍历子文件夹下的图片名称
myList1 = os.listdir(path1)
# 输出子文件内有多少张图片
print(f'total number of images detected {len(myList1)}')
# 读取每张图片
i=0
for imgName in myList1:
    if (i == 0):
        i=1
        result = cv2.imread(f'{path1}\\1.png')
    else:
        img = cv2.imread(f'{path1}/{imgName}')
        result = np.hstack((result, img))
    cv2.imwrite(rf'{cwd}\..\Image mosaicking\result.png', result)