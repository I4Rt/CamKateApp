import tkinter as tk
from tkinter import Label, Scale, Frame, Button, Entry
import cv2
from PIL import Image, ImageTk, ImageFilter
import matplotlib.pyplot as plt
import os
from functools import partial
import numpy as np
from pathlib import Path
import math
from model.data.CamSector import *
from model.abstracts.updated_camera_tools.CameraPictureGetter import *
from datetime import datetime
from tools.CameraSettings import *

def workWithLines(edges, img):
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 30  # minimum number of pixels making up a line
    max_line_gap = 20  # maximum gap in pixels between connectable line segments

    line_image = np.copy(img) * 0
    if img.ndim == 2:
        line_image = cv2.cvtColor(line_image, cv2.COLOR_GRAY2BGR) # return to bgr


    lx = []
    rx = []
    list_hw = []
    lines_list = []
    lines_lr = [[],[]]
    image_center = line_image.shape[1]/2

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
    try:
        for line in lines: 
            for x1,y1,x2,y2 in line:
                if abs(x1 - x2) < 10:
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
    except Exception as e:
        print('workWithLines', e)
        return None, None, None, line_image
    return lines_lr, lx, rx, line_image

def img_analize(edges, img):
    defects = [[], []]
    
    len_btw_lines = 10
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    lines_lr, lx, rx, line_image = workWithLines(edges, img)
    if lines_lr is None:
        return None, None, None

    mean_l = np.median(np.array(lx))
    mean_r = np.median(np.array(rx))
    detect_defect_l = []
    detect_defect_r = []

    limit = line_image.shape[1] / 12

    try:
        for index_side, lines_side in enumerate(lines_lr): # смотрим список всех линий, левые -> правые
            for index_line, line in enumerate(lines_side): 
                if index_line > 0: # если НЕ первая линия
                    if abs(line[0][0] - lines_lr[index_side][index_line-1][1][0]) < len_btw_lines: # расстояние между линиями меньше заданного
                        cv2.line(line_image,line[0],line[1],(0,255,0),1) #BGR
                    else:
                        lines_side.remove(line)
                        
                else:
                    mean_val = int(np.array([line[0][0], line[1][0]]).mean())
                    if abs(mean_val - mean_l) < limit or abs(mean_val - mean_r) < limit: # адекватно ли расположена первая линия
                        cv2.line(line_image,line[0],line[1],(0,255,0),1) #BGR
                    else:
                        lines_side.remove(line)
                        
                detect_defect_l.append(line[0][0]) if index_side == 0 else detect_defect_r.append(line[0][0]) # возможно баг, в расчетах нет учитывания корректности линии
                detect_defect_l.append(line[1][0]) if index_side == 0 else detect_defect_r.append(line[1][0])
        left_defect = abs(min(detect_defect_l) - max(detect_defect_l))
        right_defect = abs(min(detect_defect_r) - max(detect_defect_r))
        defects[0], defects[1] = format(left_defect*1.8, '.1f') , format(right_defect*1.8, '.1f')
        # print(f'левое искревление = {left_defect}({left_defect*1.8} см), правое искревление = {right_defect}({right_defect*1.8} см)')

        edges_3d = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        lines_edges = cv2.addWeighted(img, 0.7, line_image, 1, 0)
        final_img = cv2.cvtColor(lines_edges, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print('img_analize', e)
        return None, None, None
    
    return final_img, defects, rx

def PIL_tranform(img, cor_light=None):
    if (img.mode == 'RGBA'):
        red, green, blue, alpha = img.split()
    else:
        red, green, blue = img.split()
    if cor_light is None:
        light = np.array(blue).mean() 
        cor_light = light if light < 100 else light + 15 if light < 125 else light + 25
    blue_th = blue.point(lambda x: 255 if x < cor_light else 0)
    blue_th = dilate(1, blue_th)
    blue_th = erode(2, blue_th)
    blue_th = dilate(1, blue_th)
    
    # blue_th.show()
    # blue_th.save(path)
    return blue_th

def transform_image(img):
    low_threshold = 50
    high_threshold = 150
    edges = cv2.Canny(img, low_threshold, high_threshold)

    return edges

def analize(img):
    # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # another variant
    img = np.array(img)
    if img.ndim == 3:
        print('reformat')
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    edges = transform_image(img)
    img_analized, defects, rx = img_analize(edges, img)
    max_rx = None
    if rx is not None:
        max_rx = max(rx)

    return img_analized, defects, max_rx

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

def calc_move_val(dist, cur_pos, padding):
    return int(round(padding*cur_pos/dist, 0))

def remove_distortion(img, deg_angle):
    # deg_angle = 4.5
    angle = deg_angle/180 * math.pi

    img_h, img_w, img_dep = img.shape
    img_center = img_h // 2
    img_h, img_w, img_center

    padding_value = int(round(img_center * math.tan(angle), 0))
    img_with_padding = np.zeros((img_h, img_w+padding_value*2, img_dep), dtype = np.uint8)

    for i in range(img_with_padding.shape[0]):
        pad = calc_move_val(img_center, i, padding_value)
        img_with_padding[i,pad:img_w+pad,:] = img[i]
    
    return img_with_padding

def getImg(cam):
    MAX_CONNECTIONS_RETRYS = 10
    res = 2 # start await value
    break_counter = 0
    while res == 2 and break_counter < MAX_CONNECTIONS_RETRYS:
        res, pic, info = CameraPictureGetter.getPicture(cam)
        sleep(1)
        break_counter += 1
    if res == 1 and pic is not None:
        correct_pic = CameraSettings.get_correct_img(pic, cam.camera_matrix, cam.coefs)
        print('break_counter', break_counter)
        return res, correct_pic
    else:
        return res, None

def analize_manhole(img):
    img = np.array(img)
    if img.ndim == 3:
        print('reformat')
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    edges = transform_image(img)
    lines_lr, lx, rx, line_image = workWithLines(edges, img)
    if lines_lr is None:
        return None
    # plt.imshow(img)
    # plt.show()
    print('lines_lr', lines_lr)

    min_lx = min(lx)

    return min_lx
    
def getPrepareImg(prepare_object, img):
    w, h = img.size

    x1 = int(prepare_object.x1/100 * w)
    y1 = int(prepare_object.y1/100 * h)
    x2 = int(prepare_object.x2/100 * w)
    y2 = int(prepare_object.y2/100 * h)

    crop_img = img.crop(box=(x1, y1, x2, y2))
    crop_img = crop_img.rotate(90, expand=True) # top -> left, bottom -> right
    
    return crop_img, [x1, y1, x2, y2]

def run():
    camSecs = CamSector.getAll()
    for camSec in camSecs:
        cam = camSec.getCamera()
        camSecBoxes = camSec.getBoxes()
        camSecBasePoint = camSec.getBasePoint()
        res, img = getImg(cam)
        print('got img')
        if type(img) == np.ndarray:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
        if img is None:
            print("can't get image")
            continue
        # res = 1
        # img = Image.open('D:/GitHub/CamKateApp/resources/static/img/cor_rotate.png')
        # plt.imshow(img)
        # plt.show()

        if res == 1:
            crop_img, coords = getPrepareImg(camSecBasePoint, img) # basePoint
            crop_img = PIL_tranform(crop_img, cor_light=115)
            min_lx_base_point = analize_manhole(crop_img)
            
            if min_lx_base_point is not None:
                min_lx_base_point = min_lx_base_point + coords[1] # coords of object + coords of crop img (top border)
                print('min_lx_base_point on image', min_lx_base_point) 
            
            for box in camSecBoxes:
                crop_img, coords = getPrepareImg(box, img)
                crop_img = PIL_tranform(crop_img)
                
                
                final_img, defects, max_rx_box = analize(crop_img)
                if defects is None:
                    print('box not found', datetime.now())
                    # box.addMeasurement('top_defect', None)
                    # box.addMeasurement('bottom_defect', None)
                    # box.addMeasurement('distance to base point', None)
                    continue
                final_img = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
                final_img = Image.fromarray(final_img)
                final_img = final_img.rotate(-90, expand=True)

                max_rx_box = coords[1] + max_rx_box  # coords of crop img (top border) + coords of object
                if min_lx_base_point is not None:
                    distance = (min_lx_base_point - max_rx_box) * 1.8
                else:
                    distance = None
                # print('max_rx_box on image', max_rx_box)
                
                # plt.imshow(final_img)
                # plt.show()

                box.addMeasurement('top_defect', defects[0])
                box.addMeasurement('bottom_defect', defects[1])
                box.addMeasurement('distance to base point', distance)
                print(f'\nИскревление верхней стенки = {defects[0]} см\nИскревление нижней стенки = {defects[1]} см\nРасстояние от люка = {distance} см')

    print('finish')
    # sleep(10)
