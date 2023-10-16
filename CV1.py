import cv2 as cv
import numpy as np
from PIL import Image


def get_color_limit(color):
    c = np.uint8([[color]])
    hsvC = cv.cvtColor(c, cv.COLOR_BGR2HSV)
    print(hsvC)
    lower_limit = hsvC[0][0][0] - 10, 100, 100
    upper_limit = hsvC[0][0][0] + 10, 255, 255

    lower_limit = np.array(lower_limit, dtype=np.uint8)
    upper_limit = np.array(upper_limit, dtype=np.uint8)
    return lower_limit, upper_limit


red = [255, 0, 0]
blue = [0, 0, 255]

hsv_color_r = cv.cvtColor(np.uint8([[red]]), cv.COLOR_BGR2HSV) 
hsv_color_b = cv.cvtColor(np.uint8([[blue]]), cv.COLOR_BGR2HSV)

lowerlimit_b, upperlimit_b = get_color_limit(color=blue)
lowerlimit_r, upperlimit_r = get_color_limit(color=red)
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    hsvimage = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    if lowerlimit_b[0] <= hsv_color_b[0][0][0] <= upperlimit_b[0] and lowerlimit_b[1] <= hsv_color_b[0][0][1] <= upperlimit_b[1] and lowerlimit_b[2]<= hsv_color_b[0][0][2] <= upperlimit_b[2]:
        #print("b")
        mask_b = cv.inRange(hsvimage, lowerlimit_b, upperlimit_b)
        mask_box_b = Image.fromarray(mask_b)
        bbox_b = mask_box_b.getbbox()
        if bbox_b is not None:
            x1, y1, x2, y2 = bbox_b
            frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 265, 0), 2)
    elif lowerlimit_r[0] <= hsv_color_r[0][0][0] <= upperlimit_r[0] and lowerlimit_r[1] <= hsv_color_r[0][0][1] <= upperlimit_r[1] and lowerlimit_r[2] <= hsv_color_r[0][0][2]<= upperlimit_r[2]:
        #print("r")
        mask_r = cv.inRange(hsvimage, lowerlimit_r, upperlimit_r)
        mask_box_r = Image.fromarray(mask_r)
        bbox_r = mask_box_r.getbbox()
        if bbox_r is not None:
            x1, y1, x2, y2 = bbox_r
            frame = cv.rectangle(frame, (x1, y1), (x2, y2), (0, 265, 0), 2)
    cv.imshow("frame_my", frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
