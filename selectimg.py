import os
from random import shuffle
import shutil
import pdb

class ImgSelect:

    def __init__(self, strDir,dstDir):
        # print("图片选择对象已经创建...")
        self.strDir = strDir
        self.dstDir = dstDir


    def getImgList(self,num,strType='jpg'):

        """
        根据目录读取所有的图片
        :param strType: 图片的类型
        :return:  图片列表
        """
        files = os.listdir(self.strDir)
        shuffle(files)
        if len(files) > num:
            imglists = files[0:num]
        else :
            imglists = files

        # self.imglists = imglists
        return imglists


    def copyImgList(self,imglists):

        if not os.path.exists(self.dstDir):
            os.makedirs(self.dstDir)

        for imgname in imglists:
            print(imgname)
            if imgname.endswith(("jpg","png","bmp")):
                srcfile = os.path.join(self.strDir, imgname)
                dstfile = os.path.join(self.dstDir, imgname)
                shutil.copyfile(srcfile, dstfile)




if __name__=="__main__":

    imgselect = ImgSelect(strDir="F:/navinfo/data/02/",dstDir="F:/navinfo/data/05/")
    imglists = imgselect.getImgList(2)
    # print(imglists)
    imgselect.copyImgList(imglists)



