from config import *
from web_contollers.api_tools.wraplers import *
from model.abstracts.updated_camera_tools.CameraPictureGetter import *
from model.data.Camera import Camera
from model.data.CamSector import CamSector
from model.data.Box import Box
from model.data.Measurement import Measurement
from model.data.BasePoint import BasePoint
from tools.FileUtil import FileUtil
from tools.CameraSettings import CameraSettings
import json
from flask import request, send_file

import io
import csv
import zipfile
from datetime import timedelta

@cross_origin
@app.route('/getCameraPicture', methods=['POST']) 
@exception_processing
def getCameraPicture():
    rawCamSecId = request.json['cam_sec_id']
    try:
        camSecId = int(rawCamSecId)
    except:
        return {request.path: False, 'data': {'description': 'Bad cam_id type', 'code': 1}}
    cs = CamSector.getByID(camSecId)
    if cs:
        cam = cs.getCamera()
        if cam:
            MAX_CONNECTIONS_RETRYS = 20
            res = 2 # start await value
            break_counter = 0

            while res == 2 and break_counter < MAX_CONNECTIONS_RETRYS:
                print('getPicture')
                res, pic, info = CameraPictureGetter.getPicture(cam)
                sleep(1)
                break_counter += 1
                # here can be added check for case res is 1 but img is None
            print(3, res, type(pic))

            if res == 1 and pic is not None:
                # pic = cv2.imread('D:/GitHub/AnglesCamera/ready_20340101/image.png')
                correct_pic = CameraSettings.get_correct_img(pic, cam.camera_matrix, cam.coefs)
                # correct_pic = CameraSettings.removeErrorAngle(pic)

                return {request.path: True, 'data': {'b64img': FileUtil.convertImageToBytes(correct_pic), 'code': 0}}
            elif res == 2:
                return {request.path: False, 'data': {'description': 'Too long await time', 'code': 3}}
            elif res == 3:
                return {request.path: False, 'data': {'description': 'Camera is not avaliable', 'code': 4}}
            elif res == 4:
                return {request.path: False, 'data': {'description': 'No answer from camera, try later', 'code': 5}}
            elif res == 1:
                return {request.path: False, 'data': {'description': 'Image did not apear yet', 'code': 8}} # connection created but image did not apear
            else:
                return {request.path: False, 'data': {'description': f'Bad camera connection with inside code {res}', 'code': 6}}
            
        return {request.path: False, 'data': {'description': 'Bad DB link error: cs has no camera', 'code': 7}}
            
    return {request.path: False, 'data': {'description': 'CameraSector with such ID do not exist', 'code': 2}}

@cross_origin
@app.route('/delCameraSector', methods=['GET']) 
@exception_processing
def delCamera():
    camSectorId = request.args['cam_sector_id']
    cs = CamSector.getByID(camSectorId)
    if cs:
        cs.delete()
    return {request.path: True}

@cross_origin
@app.route('/delBox', methods=['GET']) 
@exception_processing
def delBox():
    boxId = request.args['id']
    Box.deleteByID(boxId)
    return {request.path: True}
    

@cross_origin
@app.route('/setCameraSector', methods=['POST']) 
@exception_processing
def setCameraSector():
    
    name = request.json['name']
    route = request.json['route']
    matrix = request.json['matrix']
    coefs = request.json['coefs']

    print(matrix)
    
    # matrix check
    # try:
    #     json.loads(matrix)
    # except:
    #     return {request.path: False, 'data': {'description': 'Bad matrix format', 'code': 1}}
    # # coefs check
    # try:
    #     json.loads(coefs)
    # except:
    #     return {request.path: False, 'data': {'description': 'Bad coefs format', 'code': 2}}

    if 'cam_sec_id' in request.json:
        camSec = CamSector.getByID(request.json['cam_sec_id'])
        if camSec:
            try:
                camSec.name = name
                camSec.save()
            except Exception as e:
                return {request.path: False, 'data': {'description': 'Name not unique', 'code': 6, 'adder_info': str(e)}}
            camera = camSec.getCamera()
            
            if camera:
                try:
                    camera.route = route
                    camera.coefs = coefs
                    camera.camera_matrix = matrix
                    camera.save()
                except:
                    return {request.path: False, 'data': {'description': 'Bad DB link error: cs has no camera', 'code': 7}}
            else:
                camSec.delete()
                return {request.path: False, 'data': {'description': 'Bad DB link error: cs has no camera', 'code': 8}}
        else:
            return {request.path: False, 'data': {'description': 'No such camera ID', 'code': 5}}
    else:
        try:
            camSec = CamSector(name)
            camSec.save()
        except Exception as e:
            return {request.path: False, 'data': {'description': 'Name not unique', 'exception': str(e), 'code': 3}}
        
        try:
            camera = Camera(route, matrix, coefs)
            camera.save()
        except:
            camSec.delete()
            return {request.path: False, 'data': {'description': 'Route not unique', 'code': 4}}
        
        try:
            camera.setCamSector(camSec)
        except:
            camSec.delete()
            {request.path: False, 'data': {'description': 'Unmatched error', 'code': 5}}
    
    return {request.path: True, 'data': {'cam_sec_id': camSec.id, 'camera': camera.getInfo(), 'code': 0}}

@cross_origin
@app.route('/setBox', methods=['POST']) 
@exception_processing
def setBox():
    
    x1 = request.json['x1']
    y1 = request.json['y1']
    x2 = request.json['x2']
    y2 = request.json['y2']
    boxName = request.json['box_name']
    
    if 'box_id' in request.json:
        box_id = request.json['box_id']
        box = Box.getByID(box_id)
        box.x1 = x1
        box.x2 = x2
        box.y1 = y1
        box.y2 = y2
        box.name = boxName
        
        try:
            box.save()
        except:
            return {request.path: False, 'data': {'description': 'Name is not unique', 'code': 2}}
    else:
        camSecId = request.json['cam_sec_id']
        camSec = CamSector.getByID(camSecId)
        if camSec:
            box = Box(boxName, x1, y1, x2, y2)
            
            try:
                box.setCamSectorById(camSec.id)
            except Exception as e:
                return {request.path: False, 'data': {'description': 'Name is not unique', 'code': 2}}
            
        else: 
            return {request.path: False, 'data': {'description': 'Unmatched error', 'code': 1}}
        
    return {request.path: True, 'data': {'box': box.getInfo(), 'code': 0}}

@cross_origin
@app.route('/setBasePoint', methods=['POST']) 
@exception_processing
def setBasePoint():
    
    x1 = request.json['x1']
    y1 = request.json['y1']
    x2 = request.json['x2']
    y2 = request.json['y2']
    
    cam_sec_id = request.json['cam_sec_id']
        
    basePoint = BasePoint.getByCameraSectorId(cam_sec_id)
    print(basePoint)
    if basePoint:
        basePoint.x1 = x1
        basePoint.x2 = x2
        basePoint.y1 = y1
        basePoint.y2 = y2
    else:
        camSec = CamSector.getByID(cam_sec_id)
        if camSec:
            basePoint = BasePoint(cam_sec_id, x1, y1, x2, y2)
        else: 
            return {request.path: False, 'data': {'description': 'No such camera sector id', 'code': 1}}
        
    basePoint.save()
    
    return {request.path: True, 'data': {'basePoint': basePoint.getInfo(), 'code': 0}}

@cross_origin
@app.route('/delBasePoint', methods=['GET']) 
@exception_processing
def delBasePoint():
    basePointId = request.args['id']
    BasePoint.deleteByID(basePointId)
    return {request.path: True}

@app.route('/get_csv', methods=['GET', 'POST'])
@cross_origin()
@exception_processing
def test_download():
    json_data = request.json
    outer_id = json_data['cam_sec_id']
    
    begin_time = None
    end_time = None
    if 'begin_time' in json_data:
        begin_time = json_data['begin_time']
    if 'end_time' in json_data:
        end_time = json_data['end_time']
    
    print(outer_id, type(outer_id))
    try:
        data = Measurement.getMeasurements(outer_id, begin_time, end_time)
        print(data)
    except Exception as e:
        print(e)
    data_len = len(data)
    print(data_len)
    if data_len == 0:
        return {"status": False, "description":
                "Нет данных по эксперименту за выбранный промежуток времени \n или номер эксперимента указан неверно" }
    print('next')
    proxy = io.StringIO()
    writer = csv.writer(proxy)
    zip_buffer = io.BytesIO()
    mem = io.BytesIO()
    start_date = data[0][2]
    limit_len = 1000000 if (data_len > 1000000) else data_len
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, row in enumerate(data):
            writer.writerow(row)
            if i % limit_len == 0 and i > 0:
                save_file(row, start_date, mem, proxy, zip_file)
                proxy = io.StringIO()
                writer = csv.writer(proxy)
                mem = io.BytesIO()

                try:
                    start_date = data[i+1][2]
                    print('try start_date', start_date)
                    
                except Exception as e:
                    print('row', row)
                    start_date = row[2]
                    print(e)

        print('\nfinal')
        print('start_date', start_date)
        print(row)
        save_file(row, start_date, mem, proxy, zip_file)
    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name='files.zip',
        mimetype='application/zip'
    )

def save_file(row, start_date, mem, proxy, zip_file):
    end_date = row[2]
    filename = f'file{start_date.day if len(str(start_date.day)) == 2 else "0"+str(start_date.day)}' + \
        f'{start_date.month if len(str(start_date.month)) == 2 else "0"+str(start_date.month)}_' + \
        f'{end_date.day if len(str(end_date.day)) == 2 else "0"+str(end_date.day)}' + \
        f'{end_date.month if len(str(end_date.month)) == 2 else "0"+str(end_date.month)}.csv'
    
    mem.write(proxy.getvalue().encode())
    zip_file.writestr(f'{filename}', mem.getvalue())

    proxy.close()
    mem.close()
    