from PIL import Image
import sys
import os


def image_process(gif_path):
    try:
        im = Image.open(gif_path)
    except IOError:
        print("Load gif failed")
        sys.exit(1)
    cnt = 1
    mypalette = im.getpalette()  # 调色板

    try:
        while True:
            im.putpalette(mypalette)
            new_image = Image.new('RGBA', im.size)
            new_image.paste(im)
            for count, (r,g,b,a) in new_image.getcolors():
                if r == 146:
                    print("1",end="")
                else:
                    print("0",end="")
                # print(r,g,b,a)
            # new_image.save(os.path.join(save_path, str(cnt) + '.png'))
            cnt = cnt + 1
            im.seek(im.tell() + 1)
    except EOFError:
        pass

gif = 'D:\桌面\white_00c596fe7714e86ef395a34dd85b0a07\黑.gif'
image_process(gif)
#
#
# save = r'D:\桌面\white_00c596fe7714e86ef395a34dd85b0a07'
# image_process(gif, save)
#
#
# c = 1
# png = rf'D:\桌面\white_00c596fe7714e86ef395a34dd85b0a07\{c}.png'
# while c<=296:
#     image = Image.open(png)
#     print(image.getcolors())
#     c +=1"""
#
#
# # coding:utf-8
#
# def RGB_to_Hex(tmp):
#     rgb = tmp.split(',')  # 将RGB格式划分开来
#     strs = '#'
#     for i in rgb:
#         num = int(i)  # 将str转int
#         # 将R、G、B分别转化为16进制拼接转换并大写
#         strs += str(hex(num))[-2:].replace('x', '0').upper()
#
#     return strs
# i=1
# while i<=296 :
#     i +=1
#     print(RGB_to_Hex('0,0,0'))
