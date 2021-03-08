import cv2
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.cm as cm


# takes a 7x7 block and gives a and b
def reg_77(block):
    xs = []
    ys = []
    # extraction of xs and ys :
    for i in range(0, 7):
        for j in range(0, 7):
            if (block[i][j] >= 0.95):
                xs.append(i)
                ys.append(j)
    ys.reverse()
    # regression calculation : using this function gives almost same values as manual calculation
    if (len(xs) < 2):
        return (0, 0)
    else:
        try:
            a = np.polyfit(xs, ys, 1)
        except Exception as e:
            a = (0, 0)
            pass
        return a


# takes img and rturn list of blocks:
def img_to_blocks(img):
    blocks = []
    i = 0
    j = 0
    while (i < 28):
        j = 0
        while (j < 28):
            blocks.append(img[i:i + 7, j:j + 7])
            j = j + 7
        i = i + 7
    return blocks


def extract(img):
    inverted_img = (255.0 - img)
    img = inverted_img / 255.0
    values = []
    blocks = img_to_blocks(img)
    for block in blocks:
        a, b = reg_77(block)
        values.append(a)
        values.append(b)
    return values
