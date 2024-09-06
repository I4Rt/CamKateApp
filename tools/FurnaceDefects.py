from tools.FindDefects import *

import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

class FurnaceDefects(FindDefects):

    @classmethod
    def detect(cls, img_path, check_img=False, save_img=False):
        image = Image.open(img_path)

        bw_image = image.convert("L")
        thresholded_image = bw_image.point(lambda p: 1 if p < 70 else 255)
        thresholded_image.save('test.jpg')

        grey_image = cv2.imread('test.jpg', cv2.IMREAD_GRAYSCALE)
        os.remove('test.jpg')
        _, binary = cv2.threshold(grey_image, 1, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        square_con = []
        for contour in contours:
            square_con.append(contour) if len(contour) > 200 else None

        data = square_con[0]
        image2 = cv2.cvtColor(grey_image, cv2.COLOR_GRAY2BGR)
        for data in square_con:
            FindDefects.find_defect_at_counter(data, image2)
            print('\n')

        if check_img:
            plt.imshow(image2)
            plt.show()
        if save_img:
            cv2.imwrite('detected_img.jpg', image2)

    @classmethod
    def find_defect_at_counter(cls, counter, image):
        first_values = [item[0][0] for item in counter]
        second_values = [item[0][1] for item in counter]
        lx = min(first_values)
        rx = max(first_values)
        ty = min(second_values)
        by = max(second_values)
        start_l = [lx, ty]
        start_r = [rx, ty]
        defect_l = [lx, ty]
        defect_r = [rx, ty]

        print('x', lx)

        cv2.circle(image, defect_l, radius=2, color=(0, 255, 0), thickness=-1)
        cv2.circle(image, defect_r, radius=2, color=(0, 255, 0), thickness=-1)

        for i in range(ty, by):
            color = list(set(image[i, lx]))[0]
            if color > 30:
                for j in range(10):
                    check_color = list(set(image[i, lx+j]))[0]
                    if check_color < 10:
                        defect_l = [lx+j, i]
                        image2 = cv2.circle(image, defect_l, radius=1, color=(255, 0, 0), thickness=-1)
                        lx = lx + j
                        break

        for i in range(ty, by):
            color = list(set(image[i, rx]))[0]
            if color > 40:
                for j in range(10):
                    check_color = list(set(image[i, rx-j]))[0]
                    if check_color < 10:
                        defect_r = [rx-j, i]
                        cv2.circle(image, defect_r, radius=1, color=(255, 0, 0), thickness=-1)
                        rx = rx - j
                        break

        cv2.circle(image2, defect_l, radius=1, color=(0, 0, 255), thickness=-1)
        cv2.line(image2, defect_l, (start_l[0], defect_l[1]), color=(255, 123, 245))
        print(f'defect_l is {abs(defect_l[0] - start_l[0])} pixels')

        cv2.circle(image2, defect_r, radius=1, color=(0, 0, 255), thickness=-1)
        cv2.line(image2, defect_r, (start_r[0], defect_r[1]), color=(255, 123, 245))
        print(f'defect_r is {abs(defect_r[0] - start_r[0])} pixels')
        

