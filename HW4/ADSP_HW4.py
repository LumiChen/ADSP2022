import numpy as np
import cv2
from skimage.metrics import structural_similarity

img1 = cv2.imread("image1.jpg", 0)
img2 = cv2.imread("image3.jpg", 0)


def SSIM(image1, image2, c1, c2):
    mux = np.mean(image1)
    muy = np.mean(image2)

    covxy = 0
    vary = 0
    varx = 0
    for i in range(image1.shape[0]):
        for j in range(image1.shape[1]):
            covxy += (image1[i, j] - mux) * (image2[i, j] - muy)
            varx += (image1[i, j] - mux)**2
            vary += (image2[i, j] - muy)**2
    covxy = covxy / (image1.shape[0] * image1.shape[1])
    varx = varx / (image1.shape[0] * image1.shape[1])
    vary = vary / (image2.shape[0] * image2.shape[1])

    L = 255
    temp = (((2 * mux * muy) + ((c1 * L)**2)) * ((2 * covxy) + ((c2 * L)**2))) / \
           (((mux**2) + (muy**2) + ((c1 * L)**2)) * (varx + vary + ((c2 * L)**2)))

    return temp


c1 = 1 / np.sqrt(255)
c2 = 1 / np.sqrt(255)
ssim = SSIM(img1, img2, c1, c2)
a = structural_similarity(img1, img2)
print(ssim)
print(a)


