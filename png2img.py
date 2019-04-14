# png画像からドット位置のバイナリをテキストで出力する

import numpy as np
from PIL import Image
import sys

# RGB値を16bit(RGB:565)のテキストに変換する
def rgb2hexstr(rgb):
    col = ((rgb[0]>>3)<<11) | ((rgb[1]>>2)<<5) | (rgb[2]>>3)
    return "0x{:04X}".format(col)

def main():
    if len(sys.argv) != 2:
        print('Usage:png2img.py <pngfile>')
        return

    image = Image.open(sys.argv[1])
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
            pixel = getPixel(x, y)
            print(rgb2hexstr(pixel) + ",", end="")
            x_cnt = x_cnt + 1
            if x_cnt >= 8:
                x_cnt = 0
                print()
        print()
        x_cnt = 0

if __name__ == '__main__':
    main()
