import numpy as np
from skimage.io import imread, imsave
from skimage.transform import rotate as skrotate

import util

def rotate(img, degree):
    img1 = skrotate(img, degree, resize=True)
    return (img1 * 255).astype(np.uint8)


def rotate_dir(dir):
    for f in util.globfiles(dir):
        img = imread(f)
        img = rotate(img, -90)
        imsave(f, img)


def bgr2rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def bgr2rgb1(img):
    b, g, r = cv2.split(img)
    return cv2.merge((r, g, b))

def bgr2rgb2(img):
    return img[..., [2, 1, 0]]

def bgr2rbg3(img):
    return img[:,:,::-1]
