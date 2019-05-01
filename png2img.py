# png画像からドット位置のバイナリをテキストで出力する

import numpy as np
from PIL import Image
import argparse
import sys

# RGB値を16bit(RGB:565)のテキストに変換する
def rgb2hexstr(rgb):
    col = ((rgb[0]>>3)<<11) | ((rgb[1]>>2)<<5) | (rgb[2]>>3)
    return "0x{:04X}".format(col)

# RGB値を8bit(RGB:332)のテキストに変換する
def rgb8bithexstr(rgb):
    col = ((rgb[0]>>5)<<5) | ((rgb[1]>>5)<<2) | (rgb[2]>>6)
    return "0x{:02X}".format(col)

def main():
    # オプション解析
    argparser = argparse.ArgumentParser()

    argparser.add_argument('pngfile', help='A filename of png image')
    argparser.add_argument('-8', '--bpp8', action='store_true', help='Output with 8bpp hex text')
    args = argparser.parse_args()
#    print(args.pngfile)

    # 出力形式を選択
    outstr = rgb2hexstr
    if args.bpp8 == True:
        outstr = rgb8bithexstr

    image = Image.open(args.pngfile)
    width, height = image.size

    print("// w,h:", width, height)

    #  パレット読み込み
    if image.mode == 'P':
        palette = np.array(image.getpalette()).reshape(-1, 3)
        getPixel = lambda x,y: palette[image.getpixel((x, y))]
    else:
        getPixel = lambda x,y: image.getpixel((x, y))

    x_cnt = 0
    for y in range(height):
        for x in range(width):
            #  行の先頭に空白を入れる
            if x_cnt == 0:
                print("    ", end="")
            pixel = getPixel(x, y)
            # print(rgb2hexstr(pixel) + ",", end="")
            print(outstr(pixel) + ",", end="")
            x_cnt = x_cnt + 1
            if x_cnt >= 8:
                x_cnt = 0
                print()
        print()
        x_cnt = 0

if __name__ == '__main__':
    main()
