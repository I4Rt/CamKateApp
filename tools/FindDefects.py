import tkinter as tk
from tkinter import Label, Scale, Frame, Button, Entry
import cv2
from PIL import Image, ImageTk, ImageFilter
import matplotlib.pyplot as plt
import os
from functools import partial
import numpy as np
from pathlib import Path

class FindDefects():

    def img_analize(edges, img, defects):
        rho = 1  # distance resolution in pixels of the Hough grid
        theta = np.pi / 500  # angular resolution in radians of the Hough grid
        threshold = 15  # minimum number of votes (intersections in Hough grid cell)
        min_line_length = 30  # minimum number of pixels making up a line
        max_line_gap = 20  # maximum gap in pixels between connectable line segments
        line_image = np.copy(img) * 0  # creating a blank to draw lines on
        img_for_check_lines = np.copy(line_image)

        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print('gray_img',gray_img)
        img_for_check_lines = cv2.cvtColor(img_for_check_lines, cv2.COLOR_BGR2GRAY)
        print('img_for_check_lines', img_for_check_lines.shape)

        # Run Hough on edge detected image
        # Output "lines" is an array containing endpoints of detected line segments
        lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
        lx = []
        rx = []
        list_hw = []
        lines_list = []
        lines_lr = [[],[]]
        # lines_r = []
        image_center = line_image.shape[1]/2
        len_btw_lines = 10
        for line in lines: 
            for x1,y1,x2,y2 in line:
                if abs(x1 - x2) < 5:
                    list_hw.append([x1-x2, y1-y2])
                    lines_list.append([[x1,y1],[x2,y2]])
                    if x1 < image_center:
                        lines_lr[0].append([[x1,y1],[x2,y2]])
                        lx.append(x1)
                        lx.append(x2)
                    if x1 > image_center:
                        lines_lr[1].append([[x1,y1],[x2,y2]])
                        rx.append(x1)
                        rx.append(x2)
        try:
            detect_defect_l = []
            detect_defect_r = []
            mean_l = np.median(np.array(lx))
            mean_r = np.median(np.array(rx))


            limit = line_image.shape[1] / 12
            # print('limit', limit)

            for index_side, lines_side in enumerate(lines_lr):
                for index_line, line in enumerate(lines_side):
                    if index_line > 0:
                        if abs(line[0][0] - lines_lr[index_side][index_line-1][1][0]) < len_btw_lines:  # рисуем линию если текущая координата x меньше чем установленное значение
                            # TODO: исправить условие рисования линий
                            # print('draw line index')
                            
                            cv2.line(img_for_check_lines,line[0],line[1],1,1)
                            line_points = np.column_stack(np.where(img_for_check_lines == 1))
                            line_values = [gray_img[x, y] for x, y in line_points]
                            print('line_points_l', np.mean(line_values), len(line_values)) # среднее значение всех точек исходного изображения, которые совпадают координатами с линией
                            img_for_check_lines = img_for_check_lines * 0

                            if np.mean(line_values) > 200:
                                print('line_points_l_true', np.mean(line_values), len(line_values))
                                cv2.line(line_image,line[0],line[1],(0,255,0),1) #BGR
                        else:
                            lines_side.remove(line)
                            continue
                    else:
                        mean_val = int(np.array([line[0][0], line[1][0]]).mean())
                        if abs(mean_val - mean_l) < limit or abs(mean_val - mean_r) < limit:
                            # print('draw line limit')
                            cv2.line(img_for_check_lines,line[0],line[1],1,1)
                            line_points = np.column_stack(np.where(img_for_check_lines == 1))
                            line_values = [gray_img[x, y] for x, y in line_points]
                            print('line_points_r', np.mean(line_values), len(line_values)) # среднее значение всех точек исходного изображения, которые совпадают координатами с линией
                            img_for_check_lines = img_for_check_lines * 0

                            if np.mean(line_values) > 200:
                                print('line_points_r_true', np.mean(line_values), len(line_values))
                                cv2.line(line_image,line[0],line[1],(0,255,0),1) #BGR

                    detect_defect_l.append(line[0][0]) if index_side == 0 else detect_defect_r.append(line[0][0])
                    detect_defect_l.append(line[1][0]) if index_side == 0 else detect_defect_r.append(line[1][0])
            # plt.imshow(line_image)
            # print('среднее lx: ', mean_l, 'среднее rx: ', mean_r)
            # print('detect x: ', detect_defect_l, detect_defect_r)
            left_defect = abs(min(detect_defect_l) - max(detect_defect_l))
            right_defect = abs(min(detect_defect_r) - max(detect_defect_r))
            defects[0], defects[1] = left_defect*1.8, right_defect*1.8
            print(defects)
            # print(str(x), f'левое искревление = {left_defect}({left_defect*1.8} см), правое искревление = {right_defect}({right_defect*1.8} см)')
        except Exception as e:
            print(e)

        print('lines', lines)

        edges_3d = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        lines_edges = cv2.addWeighted(img, 0.7, line_image, 1, 0)
        final_img = cv2.cvtColor(lines_edges, cv2.COLOR_BGR2RGB)
        
        # axes[n//3, n%3].set_title(str(x))
        return final_img, defects

    def PIL_tranform(x, cor_light=None):
        path = 'ready_20340101/one_file/copy1_blue.jpg'
        img = Image.open(x)
        print('pil_trans', img.mode)
        if (img.mode == 'RGBA'):
            red, green, blue, alpha = img.split()
        else:
            red, green, blue = img.split()
        if cor_light is None:
            light = np.array(blue).mean() 
            cor_light = light if light < 100 else light + 15 if light < 125 else light + 25
        else: cor_light = cor_light.get()
        # cor_light = light
        blue_th = blue.point(lambda x: 255 if x < cor_light else 0)
        
        # blue_th = dilate(1, blue_th)
        # blue_th = erode(2, blue_th)
        # blue_th = dilate(1, blue_th)
        # blue_th.show()
        blue_th.save(path)
        return path

    def get_image(images, label, light=None, use_PIL=True, *args):
        global index
        global normal_img

        filename = images[index % len(images)]
        print('get_img_filename', filename, light, ' index ', index)
        
        path = PIL_tranform(filename, light) if use_PIL else filename
        
        # normal_img = cv2.imread(str(x))
        
        normal_img = cv2.imread(path)
        # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # if img_rechange: 
        tk_image = image_to_imageTk(normal_img)
        label.config(image=tk_image)
        label.image = tk_image
        return normal_img


    def transform_image(img, values):

        low_threshold = values[0].get()
        high_threshold = values[1].get()
        # print('values', low_threshold, high_threshold)
        edges = cv2.Canny(img, low_threshold, high_threshold)

        return edges

    def print_slider_value(slider, values, defects, labels, mode):
        global normal_img
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # another variant
        edges = transform_image(normal_img, values)
        img_analized, defects = img_analize(edges, normal_img, defects)

        if mode == 'full_analize':
            tk_image = image_to_imageTk(img_analized)

            labels[1].config(text=defects[0])
            labels[2].config(text=defects[1])
        elif mode == 'edges_only':
            tk_image = image_to_imageTk(edges)

        labels[0].config(image=tk_image)
        labels[0].image = tk_image

        # print(values[0].get(), values[1].get())

    def image_to_imageTk(img):
        tk_image = Image.fromarray(img)
        tk_image = ImageTk.PhotoImage(tk_image)
        return tk_image

    def erode(cycles, image):
        if type(image) == np.ndarray: image = Image.fromarray(image)
        # del white pixels
        for _ in range(cycles):
            image = image.filter(ImageFilter.MinFilter(3))
        return image

    def dilate(cycles, image):
        if type(image) == np.ndarray: image = Image.fromarray(image)
        # del black pixels
        for _ in range(cycles):
            image = image.filter(ImageFilter.MaxFilter(3))
        return image

    def next_image(label, images):
        global index
        global normal_img
        index += 1
        print('next_image', str(images[index % len(images)]))
        normal_img = get_image(images, label=label)
        # tk_image = image_to_imageTk(normal_img)
        # label.config(image=tk_image)
        # label.image = tk_image

    def change_img(label, func):
        global normal_img
        
        method = globals()[func]
        normal_img = np.asarray(method(1, normal_img))

        tk_image = image_to_imageTk(normal_img)
        label.config(image=tk_image)
        label.image = tk_image
