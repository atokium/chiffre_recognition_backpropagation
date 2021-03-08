import cv2
import numpy as np
from skimage.transform import resize, pyramid_reduce


def resize_image(img, size=(28, 28)):
    h, w = img.shape[:2]
    c = img.shape[2] if len(img.shape) > 2 else 1
    if h == w:
        return cv2.resize(img, size, cv2.INTER_AREA)
    dif = h if h > w else w
    interpolation = cv2.INTER_AREA if dif > (size[0] +
                                             size[1]) // 2 else cv2.INTER_CUBIC
    x_pos = (dif - w) // 2
    y_pos = (dif - h) // 2
    if len(img.shape) == 2:
        mask = np.zeros((dif, dif), dtype=img.dtype)
        mask.fill(255)
        mask[y_pos:y_pos + h, x_pos:x_pos + w] = img[:h, :w]
    else:
        mask = np.zeros((dif, dif, c), dtype=img.dtype)
        mask.fill(255)
        mask[y_pos:y_pos + h, x_pos:x_pos + w, :] = img[:h, :w, :]

    # return it by puttin the small image on top of the mask
    return cv2.resize(mask, size, interpolation)


# crop image to 28x28 with canvas centred with same aspect ratio
def crop(img):
    h, w = img.shape[:2]
    # invert to detect edges
    imgray = 255 - img
    #Binarize the image and call it thresh.
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST,
                                           cv2.CHAIN_APPROX_SIMPLE)

    rects = [cv2.boundingRect(cnt) for cnt in contours]

    top_x = min([x for (x, y, w, h) in rects])
    top_y = min([y for (x, y, w, h) in rects])
    bottom_x = max([x + w for (x, y, w, h) in rects])
    bottom_y = max([y + h for (x, y, w, h) in rects])
    # put the section in a new image
    out = img[top_y:bottom_y, top_x:bottom_x]

    # turn it into what we want :
    out = resize_image(out)
    return out


# manual stuff :
# read image from file :
#img = cv2.imread('temp.jpg', 0)
#out = crop(img)
# write image
#cv2.imwrite('out.jpg', out)
