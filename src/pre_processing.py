#!/usr/bin/env python2.7

import cv2
import numpy as np
import sys

def remove_noise(img):
    denoised = cv2.fastNlMeansDenoisingColored(img, None, 21, 21, 7, 21)
    return denoised

def desaturate(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    desaturated = np.zeros(hsv.shape, hsv.dtype)
    for j in range(hsv.shape[0]):
        for i in range(hsv.shape[1]):
            new_s = hsv[j, i, 1] - 50
            new_v = hsv[j, i, 2]
            if new_s < 0:
                new_s = 0
            if new_v < 0:
                new_v = 0
            new_hsv = [hsv[j, i, 0],
                       new_s,
                       new_v]
            desaturated[j, i] = new_hsv
    bgr = cv2.cvtColor(desaturated, cv2.COLOR_HSV2BGR)
    return bgr


if __name__ == "__main__":
    filename = sys.argv[1]
    img = cv2.imread(filename)
    after_noise = remove_noise(img)
    after_desaturation = desaturate(after_noise)
    cv2.imshow("Processed image", after_desaturation)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
