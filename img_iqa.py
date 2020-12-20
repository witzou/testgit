# -*-coding=UTF-8-*-

"""
在无参考图下，检测图片质量的方法
"""

import os
import cv2
import numpy as np
from skimage import filters
import pdb

class BlurDetection:

    def __init__(self, strDir):
        print("图片检测对象已经创建...")
        self.strDir = strDir

    def _getAllImg(self, strType='jpg'):

        """
        根据目录读取所有的图片
        :param strType: 图片的类型
        :return:  图片列表
        """

        names = []
        for root, dirs, files in os.walk(self.strDir):  # 此处有bug  如果调试的数据还放在这里，将会递归的遍历所有文件
            for file in files:
                # if os.path.splitext(file)[1]=='jpg':
                names.append(str(file))
        return names

    def _imageToMatrix(self, image):
        """
        根据名称读取图片对象转化矩阵
        :param strName:
        :return: 返回矩阵
        """
        imgMat = np.matrix(image)
        # pdb.set_trace()

        return imgMat

    def _blurDetection(self, imgName):

        # step 1 图像的预处理
        img2gray, reImg = self.preImgOps(imgName)
        imgMat=self._imageToMatrix(img2gray)/255.0
        x, y = imgMat.shape
        score = 0
        for i in range(x - 2):
            for j in range(y - 2):
                score += (imgMat[i + 2, j] - imgMat[i, j]) ** 2

        score=score/10

        # # step3: 绘制图片并保存  不应该写在这里  抽象出来   这是共有的部分
        # newImg = self._drawImgFonts(reImg, str(score))
        # newDir = self.strDir + "/_blurDetection_/"
        # if not os.path.exists(newDir):
        #     os.makedirs(newDir)
        # newPath = newDir + imgName
        # cv2.imwrite(newPath, newImg)  # 保存图片
        # # cv2.imshow(imgName, newImg)
        # # cv2.waitKey(0)

        return score

    def _SMDDetection(self, imgName):

        # step 1 图像的预处理
        img2gray, reImg = self.preImgOps(imgName)
        f=self._imageToMatrix(img2gray)/255.0
        x, y = f.shape
        score = 0
        for i in range(x - 1):
            for j in range(y - 1):
                score += np.abs(f[i+1,j]-f[i,j])+np.abs(f[i,j]-f[i+1,j])
        score=score/100

        # # strp3: 绘制图片并保存  不应该写在这里  抽象出来   这是共有的部分
        # newImg = self._drawImgFonts(reImg, str(score))
        # newDir = self.strDir + "/_SMDDetection_/"
        # if not os.path.exists(newDir):
        #     os.makedirs(newDir)
        # newPath = newDir + imgName
        # cv2.imwrite(newPath, newImg)  # 保存图片
        # # cv2.imshow(imgName, newImg)
        # # cv2.waitKey(0)

        return score

    def _SMD2Detection(self, imgName):
        """
        灰度方差乘积
        :param imgName:
        :return:
        """
        # step 1 图像的预处理
        img2gray, reImg = self.preImgOps(imgName)
        f=self._imageToMatrix(img2gray)/255.0
        x, y = f.shape
        score = 0
        for i in range(x - 1):
            for j in range(y - 1):
                score += np.abs(f[i+1,j]-f[i,j])*np.abs(f[i,j]-f[i,j+1])
        score=score

        # # strp3: 绘制图片并保存  不应该写在这里  抽象出来   这是共有的部分
        # newImg = self._drawImgFonts(reImg, str(score))
        # newDir = self.strDir + "/_SMD2Detection_/"
        # if not os.path.exists(newDir):
        #     os.makedirs(newDir)
        # newPath = newDir + imgName
        # cv2.imwrite(newPath, newImg)  # 保存图片
        # # cv2.imshow(imgName, newImg)
        # # cv2.waitKey(0)
        return score

    def _Variance(self, imgName):
        """
               灰度方差乘积
               :param imgName:
               :return:
               """
        # step 1 图像的预处理
        img2gray, reImg = self.preImgOps(imgName)
        f = self._imageToMatrix(img2gray)
        score = np.var(f)

        # # strp3: 绘制图片并保存  不应该写在这里  抽象出来   这是共有的部分
        # newImg = self._drawImgFonts(reImg, str(score))
        # newDir = self.strDir + "/_Variance_/"
        # if not os.path.exists(newDir):
        #     os.makedirs(newDir)
        # newPath = newDir + imgName
        # cv2.imwrite(newPath, newImg)  # 保存图片
        # # cv2.imshow(imgName, newImg)
        # # cv2.waitKey(0)
        return score


    def _Vollath(self,imgName):
        """
                       灰度方差乘积
                       :param imgName:
                       :return:
                       """
        # step 1 图像的预处理
        img2gray, reImg = self.preImgOps(imgName)
        f = self._imageToMatrix(img2gray)
        source=0
        x,y=f.shape
        for i in range(x-1):
            for j in range(y):
                source+=f[i,j]*f[i+1,j]
        source=source-x*y*np.mean(f)

        # # strp3: 绘制图片并保存  不应该写在这里  抽象出来   这是共有的部分
        # newImg = self._drawImgFonts(reImg, str(source))
        # newDir = self.strDir + "/_Vollath_/"
        # if not os.path.exists(newDir):
        #     os.makedirs(newDir)
        # newPath = newDir + imgName
        # cv2.imwrite(newPath, newImg)  # 保存图片
        # # cv2.imshow(imgName, newImg)
        # # cv2.waitKey(0)
        return source

    def _Tenengrad(self,imgName):
        """
                       灰度方差乘积
                       :param imgName:
                       :return:
                       """
        # step 1 图像的预处理
        img2gray, reImg = self.preImgOps(imgName)
        f = self._imageToMatrix(img2gray)

        tmp = filters.sobel(f)
        source = np.sum(tmp**2)
        source = np.sqrt(source)

        # # strp3: 绘制图片并保存  不应该写在这里  抽象出来   这是共有的部分
        # newImg = self._drawImgFonts(reImg, str(source))
        # newDir = self.strDir + "/_Tenengrad_/"
        # if not os.path.exists(newDir):
        #     os.makedirs(newDir)
        # newPath = newDir + imgName
        # cv2.imwrite(newPath, newImg)  # 保存图片
        # cv2.imshow(imgName, newImg)
        # cv2.waitKey(0)

        return source


    def _lapulaseDetection(self, imgName):

        """
        :param strdir: 文件所在的目录
        :param name: 文件名称
        :return: 检测模糊后的分数
        """

        # step1: 预处理
        img2gray, reImg = self.preImgOps(imgName)
        # step2: laplacian算子 获取评分
        resLap = cv2.Laplacian(img2gray, cv2.CV_64F)
        score = resLap.var()

        # print("Laplacian %s score of given image is %s", str(score))
        # # strp3: 绘制图片并保存  不应该写在这里  抽象出来   这是共有的部分
        # newImg = self._drawImgFonts(reImg, str(score))
        # newDir = self.strDir + "/_lapulaseDetection_/"
        # if not os.path.exists(newDir):
        #     os.makedirs(newDir)
        # newPath = newDir + imgName
        # # 显示
        # cv2.imwrite(newPath, newImg)  # 保存图片

        # cv2.imshow(imgName, newImg)
        # cv2.waitKey(0)
        # step3: 返回分数
        return score

    def Test_Tenengrad(self):

        logfile = open("logTenengrad.txt",'w')
        imgList = self._getAllImg(self.strDir)

        for i in range(len(imgList)):
            score = self._Tenengrad(imgList[i])
            stringstream = str(imgList[i]) + "," + str(score)
            print(stringstream)
            logfile.write(stringstream+"\n")
        logfile.close()


    def TestVariance(self):

        logfile = open("logVariance.txt",'w')

        imgList = self._getAllImg(self.strDir)
        for i in range(len(imgList)):
            score = self._Variance(imgList[i])
            stringstream = str(imgList[i]) + "," + str(score)
            print(stringstream)
            logfile.write(stringstream + "\n")
        logfile.close()


    def TestSMD2(self):

        logfile = open("logSMD2.txt",'w')
        imgList = self._getAllImg(self.strDir)
        for i in range(len(imgList)):
            score = self._SMD2Detection(imgList[i])
            stringstream = str(imgList[i]) + "," + str(score)
            print(stringstream)
            logfile.write(stringstream + "\n")
        logfile.close()
        return


    def TestSMD(self):

        logfile = open("logSMD.txt",'w')
        imgList = self._getAllImg(self.strDir)
        for i in range(len(imgList)):
            score = self._SMDDetection(imgList[i])
            stringstream = str(imgList[i]) + "," + str(score)
            print(stringstream)
            logfile.write(stringstream + "\n")
        logfile.close()
        return


    def TestBrener(self):

        logfile = open("logBrener.txt",'w')
        imgList = self._getAllImg(self.strDir)

        for i in range(len(imgList)):
            score = self._blurDetection(imgList[i])
            stringstream = str(imgList[i]) + "," + str(score)
            print(stringstream)
            logfile.write(stringstream + "\n")
        logfile.close()
        return


    #拉普拉斯算子
    def TestLapulase(self):

        logfile = open("logLapulase.txt",'w')
        imgList = self._getAllImg(self.strDir)
        for i in range(len(imgList)):
            score = self._lapulaseDetection(imgList[i])
            stringstream = str(imgList[i]) + "," + str(score)
            print(stringstream)
            logfile.write(stringstream + "\n")
        logfile.close()
        return


    def preImgOps(self, imgName):
        """
        图像的预处理操作
        :param imgName: 图像的而明朝
        :return: 灰度化和resize之后的图片对象
        """
        strPath = self.strDir + imgName
        img = cv2.imread(strPath)  # 读取图片
        # cv2.moveWindow("", 1000, 100)
        # cv2.imshow("原始图", img)
        # 预处理操作

        reImg = cv2.resize(img, (800, 900), interpolation=cv2.INTER_CUBIC)  #
        img2gray = cv2.cvtColor(reImg, cv2.COLOR_BGR2GRAY)  # 将图片压缩为单通道的灰度图
        return img2gray, reImg

    def _drawImgFonts(self, img, strContent):
        """
        绘制图像
        :param img: cv下的图片对象
        :param strContent: 书写的图片内容
        :return:
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontSize = 3
        # 照片 添加的文字    /左上角坐标   字体   字体大小   颜色        字体粗细
        cv2.putText(img, strContent, (0, 200), font, fontSize, (0, 255, 0), 3)
        return img



if __name__ == "__main__":

    # BlurDetection = BlurDetection(strDir="D:/document/ZKBH/bug/face/")
    # BlurDetection.Test_Tenengrad () # TestSMD

    # BlurDetection.Test_Tenengrad()
    # BlurDetection.TestBrener()
    # BlurDetection.TestDect()
    # BlurDetection.TestSMD()
    # BlurDetection.TestSMD2()
    # BlurDetection.TestVariance()

    BlurDetection = BlurDetection(strDir="F:/navinfo/data/02/")
    BlurDetection.Test_Tenengrad() # Tenengrad
    BlurDetection.TestBrener()
    BlurDetection.TestSMD2()
    BlurDetection.TestSMD()
    BlurDetection.TestLapulase()
    BlurDetection.TestVariance()




