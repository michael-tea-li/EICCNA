#本脚本由乾颐堂达叔编写
#用于日常工作
#时间不多，懒得优化，凑合用用，好在处理的是不着急的事情


import os
from PIL import Image, ImageDraw, ImageFont


#定义函数用于添加水印，font为字体文件，image为通过Image.open()方法打开的图片对象，text为水印字符串
def AddWaterMark(font, image, text):
    # 打开字体文件，自备一个字体文件
    Font = ImageFont.truetype(font, 24)
    # 添加背景
    new_img = Image.new('RGBA', (image.size[0] * 3, image.size[1] * 3), (0, 0, 0, 0))
    new_img.paste(image, image.size)
    # 添加水印
    font_len = len(text)
    # 将图像转化为RGBA图像
    rgba_image = new_img.convert('RGBA')
    # 生成和待添加水印图片一样大的图片
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    # 画图
    image_draw = ImageDraw.Draw(text_overlay)
    # 绘制多个水印，设置水印的位置
    for i in range(0, rgba_image.size[0], font_len * 20):
        for j in range(0, rgba_image.size[1], 50):
            # 设置文本颜色和透明度和位置
            image_draw.text((i, j), text, font=Font, fill=(255, 102, 102, 80))
    # 水印方向设置
    text_overlay = text_overlay.rotate(20)
    # 将生成的图片覆盖到待添加水印的图片上
    image_with_text = Image.alpha_composite(rgba_image, text_overlay)
    # 裁切图片
    image_with_text = image_with_text.crop((image.size[0], image.size[1], image.size[0] * 2, image.size[1] * 2))
    return image_with_text


#定义函数，获取当前目录及子目录下的所有文件
def GetAllPngs(PngPath, All_IMG_NameList):
    CurrentList = os.listdir(PngPath) #读取当前目录下所有对象形成列表
    for obj in CurrentList: #遍历列表
        Current_path = os.path.join(PngPath,obj) #将所有对象形成绝对路径
        if os.path.isdir(Current_path): #如果是目录则执行自我迭代
            GetAllPngs(Current_path, All_IMG_NameList) #检查是否有子目录
        elif os.path.isfile(Current_path):
            All_IMG_NameList.append(Current_path) #返回绝对路径和文件名
        else:
            pass
    return All_IMG_NameList


if __name__ == '__main__':
    font = 'd:/mingliu.ttc' #字体文件目录
    text = '乾颐堂达叔出品 www.qytang.com'  #要添加的水印文本
    PngPath = 'D:/temp/'  #生成的Png图片目录
    AllPngNameList = []  #用于存储处理前图片绝对路径
    GetAllPngs(PngPath, AllPngNameList)  #获取处理前图片绝对路径列表

    #使用for循环遍历列表，将每个图片都加上水印并保存
    for IMG in AllPngNameList:
        image = Image.open(IMG)
        MarkedPng = AddWaterMark(font , image, text)
        Result = IMG.replace('jpg', 'png')
        MarkedPng.save(Result)
