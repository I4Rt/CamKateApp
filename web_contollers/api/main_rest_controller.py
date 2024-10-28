from config import *
from web_contollers.api_tools.wraplers import *
from model.abstracts.updated_camera_tools.CameraPictureGetter import *
from model.data.Camera import Camera
from model.data.CamSector import CamSector
from model.data.Box import Box
from tools.FileUtil import FileUtil
import json

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
            MAX_CONNECTIONS_RETRYS = 10
            res = 2 # start await value
            break_counter = 0
            while res == 2 and break_counter < MAX_CONNECTIONS_RETRYS:
                res, pic, info = CameraPictureGetter.getPicture(cam)
                sleep(1)
                break_counter += 1
            if res == 1:
                return {request.path: True, 'data': {'b64img': FileUtil.convertImageToBytes(pic), 'code': 0}}
            elif res == 2:
                return {request.path: False, 'data': {'description': 'Too long await time', 'code': 3}}
            elif res == 3:
                return {request.path: False, 'data': {'description': 'Camera is not avaliable', 'code': 4}}
            elif res == 4:
                return {request.path: False, 'data': {'description': 'No answer from camera, try later', 'code': 5}}
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
    boxId = request.args['box_id']
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
            print(camera)
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
            print(e)
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
                print(e)
                return {request.path: False, 'data': {'description': 'Name is not unique', 'code': 2}}
            
        else: 
            return {request.path: False, 'data': {'description': 'Unmatched error', 'code': 1}}
        
    return {request.path: True, 'data': {'box': box.getInfo(), 'code': 0}}

