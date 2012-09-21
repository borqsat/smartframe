#!/usr/bin/env python

from PIL import Image, ImageChops
import sys, math, operator, os

# return the diff rate of two image files.
# 1: totally different
# 0: the same

#TODO: Because monkeyrunner can not load PIL native library, so it's workaround
#to wrap PIL in a script. If we found a better way to resolve the issue, we
# should import PIL dierctly in monkeyrunner.
def main():
    # if no enough arguments, return 1
    if len(sys.argv) != 3:
        exit()
    
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    
    # if either file does not exist, return 1
    if (not os.path.exists(f1) or not os.path.exists(f2)):
        exit()
    
    if (not os.path.isfile(f1) or not os.path.isfile(f2)):
        exit()
    
    im1 = Image.open(f1)
    im2 = Image.open(f2)
    
    # if image size is not equal, retuan 1
    if (im1.size[0] != im2.size[0] or im1.size[1] != im2.size[1]):
        # if the image size is different, print -1 and then exit
        exit()
    
    # get the difference between the two images 
    h = ImageChops.difference(im1, im2)
    size = float(im1.size[0]*im1.size[1])
    diff = 0
    for p in list(h.getdata()):
        if (p != (0, 0, 0, 0)):
            diff += 1
    print str(diff/size)
    
def exit():
    print '1'
    sys.exit()

if __name__ == '__main__':
    main()