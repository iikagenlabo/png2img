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

# RGB値から1bitのon/off判定をする
def rgb1bit(rgb):
    col = ((rgb[0]>>7) | (rgb[1]>>7) | (rgb[2]>>7))
    if col != 0:
        return 1
    else:
        return 0

# 8, 16bpp出力
def outputColorPixel(width, height, image, outstr):
    #  パレット読み込み
    if image.mode == 'P':
        palette = np.array(image.getpalette()).reshape(-1, 3)
        getPixel = lambda x,y: palette[image.getpixel((x, y))]
    else:
        getPixel = lambda x,y: image.getpixel((x, y))

    for y in range(height):
        x_cnt = 0
        for x in range(width):
            #  行の先頭に空白を入れる
            if x_cnt == 0:
                print("    ", end="")
            pixel = getPixel(x, y)
            print(outstr(pixel) + ",", end="")
            x_cnt = x_cnt + 1
            if x_cnt >= 8:
                x_cnt = 0
                print()
        print()

def output1BitPixel(width, height, image):
    #  パレット読み込み
    if image.mode == 'P':
        palette = np.array(image.getpalette()).reshape(-1, 3)
        getPixel = lambda x,y: palette[image.getpixel((x, y))]
    else:
        getPixel = lambda x,y: image.getpixel((x, y))

    for y in range(height):
        x_cnt = 0
        bitcnt = 0
        bitpix = 0
        for x in range(width):
            #  行の先頭に空白を入れる
            if x_cnt == 0 and bitcnt == 0:
                print("    ", end="")
            pixel = getPixel(x, y)

            # pixelをon/offに変換
            bitpix <<= 1
            bitpix |= rgb1bit(pixel)

            # 8bitたまったらテキスト出力
            bitcnt = bitcnt + 1
            if bitcnt == 8:
                print("0x{:02X},".format(bitpix), end="")
                bitcnt = 0
                bitpix = 0
                x_cnt = x_cnt + 1
                if x_cnt >= 8:
                    x_cnt = 0
                    print()

        # あまりのbitがあれば出力する
        if bitcnt > 0:
            pitpix <<= (8 - bitcnt)
            print("0x{:02X},".format(bitpix), end="")

        # 4行ごとに改行
        if (y % 4) == 3:
            print()

        print()     # 改行

def main():
    # オプション解析
    argparser = argparse.ArgumentParser()

    argparser.add_argument('pngfile', help='A filename of png image')
    argparser.add_argument('-8', '--bpp8', action='store_true', help='Output with 8bpp hex text')
    argparser.add_argument('-1', '--bpp1', action='store_true', help='Output with 1bpp hex text')
    args = argparser.parse_args()

    # 出力形式を選択
    outstr = rgb2hexstr
    if args.bpp8 == True:
        outstr = rgb8bithexstr

    image = Image.open(args.pngfile)
    width, height = image.size

    print("    // w,h:", width, height)

    if args.bpp1 != True:
        outputColorPixel(width, height, image, outstr)
    else:
        output1BitPixel(width, height, image)

if __name__ == '__main__':
    main()
