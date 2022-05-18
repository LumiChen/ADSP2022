import cv2


img = cv2.imread("image1.jpg", 0)

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        img[i, j] = 0.5 * img[i, j] + 255.5 * 0.5

cv2.imwrite("image3.jpg", img)