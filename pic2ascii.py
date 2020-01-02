from __future__ import print_function
from PIL import Image, ImageEnhance
import sys

# =a 00 = 0 (aka 0)             5f (aka 1) = 95
# =b 08 = 8                     87 (aka 2) = 135
# =c 12 = 18                    af (aka 3) = 175
# =d 1C = 28                    d7 (aka 4) = 215
# =e 26 = 38
# =f 30 = 48
# =g 3A = 58
# =h 44 = 68
# =i 4E = 78
# =j 58 = 88
# =k 62 = 98
# =l 6C = 108
# =m 76 = 118
# =n 80 = 128
# =o 8A = 138
# =p 94 = 148
# =q 9E = 158
# =r A8 = 168
# =s B2 = 178
# =t BC = 188
# =u C6 = 198
# =v D0 = 208
# =w DA = 218
# =x E4 = 228
# =y EE = 238
# =z FF = 255 (aka 5)

# This array contains all of the values associated with grayscale tones in an
# array indexed at 0 (so 0 is |=a, 1 is |=b, etc). "|=z" is in here twice due
# to a quirk of the math.
bwvals = ["|=a","|=b","|=c","|=d","|=e","|=f","|=g","|=h","|=i","|=j","|=k",
          "|=l","|=m","|=n","|=o","|=p","|=q","|=r","|=s","|=t","|=u","|=v",
          "|=w","|=x","|=y","|=z"]
charwidth = 46
brightness_factor = 1.5
resize_algorithm = Image.NEAREST
outputchar = '@'

class Pixel:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    def _repr_(self):
        return "Pixel(%d, %d, %d)" % (self.r, self.g, self.b)

    # This function checks musifyrgb and calls musifybw if necessary, returning
    # either the grayscale code or the heximal rgb code
    # Returns something in format |=i or |345
    def __str__(self):
        mr = musifyrgb(self.r)
        mg = musifyrgb(self.g)
        mb = musifyrgb(self.b)
        if mr == mg and mr == mb:
            rawtotal = self.r + self.g + self.b
            bwval = int(round((rawtotal+3)/30))
            return bwvals[bwval]
        else:
            return "|%d%d%d" % (mr, mg, mb)

# This function gets called every time to convert from 0-255 values to 0-5 values
def musifyrgb(raw):
    return round(raw/51)

# This function opens the file resizes it according to a hard-coded value
# (currently 50) for width, and returns it as an array of arrays
def getPixels(filename):
    img = Image.open(filename, 'r')
    benhancer = ImageEnhance.Brightness(img)
    brighter = benhancer.enhance(brightness_factor)
    w, h = img.size
    scaling = charwidth/float(w)
    resized = brighter.resize((charwidth, int(round(scaling*h*6/11))), resize_algorithm)
    w, h = resized.size
    pix = [Pixel(r, g, b) for (r, g, b) in list(resized.getdata())]
    return [pix[n:n+w] for n in range(0, w*h, w)]

# This returns an array with width elements
def processRow(row):
    prevcode = ""
    output = []
    for pixel in row:
        currcode = str(pixel)
        if currcode == prevcode and currcode != "|=a":
            output.append("")
        else:
            output.append(currcode)
            prevcode = currcode
    return output

# The result of this is an array with height elements, each element is an array
# with width elements
def processImage(rows):
    return [processRow(row) for row in rows]

# This function makes it go
if __name__ == "__main__":
    filename = sys.argv[1]
    rows = processImage(getPixels(filename))
    for row in rows:
        for pixel in row:
            if str(pixel) == "|=a":
                print("|_", end='')
            else:
                print("%s%s" % (pixel, outputchar), end='')
        print("|/", end='')
