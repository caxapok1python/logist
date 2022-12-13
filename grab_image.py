import cv2
import numpy as np


def apply_filter(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (13, 13), 0)
    _, filter = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY_INV)
    filter = cv2.bitwise_not(filter, np.ones(filter.shape, filter.dtype))
    return filter


cap = cv2.VideoCapture(0)

while True:
    try:
        ret, image = cap.read()
        cv2.imwrite('../tmp/tmp.png', image)
        print(image.shape)
        th = apply_filter(image)
        cv2.imwrite(f'../tmp/filter.png', th)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        break

cap.release()
cv2.destroyAllWindows()
