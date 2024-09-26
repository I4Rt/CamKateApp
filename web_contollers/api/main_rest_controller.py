from config import *
from web_contollers.api_tools.wraplers import *
from model.abstracts.updated_camera_tools.CameraPictureGetter import *
from model.data.Camera import Camera
from tools.FileUtil import FileUtil

@cross_origin
@app.route('/addCamera', methods=['POST']) 
@exception_processing
def addCamera():
    return {request.path: True}


@cross_origin
@app.route('/getCameraPicture', methods=['POST']) 
@exception_processing
def getCameraPicture():
    try:
        camId = int(request.json['cam_id'])
    except:
        return {request.path: False, 'data': {'answer': 'Bad cam_id type', 'code': 1}}
    camera = Camera.getByID(camId)
    if camera:
        MAX_CONNECTIONS_RETRYS = 10
        res = -1
        break_counter = 0
        while res <= 2 and break_counter < MAX_CONNECTIONS_RETRYS:
            res, pic, info = CameraPictureGetter.getPicture(camera)
            sleep(1)
            break_counter += 1
        if res == 1:
            return {request.path: True, 'data': {'b64img': FileUtil.convertImageToBytes(pic), 'code': 0}}
        elif res == 2:
            return {request.path: False, 'data': {'answer': 'Too long await time', 'code': 3}}
        elif res == 3:
            return {request.path: False, 'data': {'answer': 'Camera is not avaliable', 'code': 4}}
        elif res == 4:
            return {request.path: False, 'data': {'answer': 'No answer from camera, try later', 'code': 5}}
        else:
            return {request.path: False, 'data': {'answer': f'Bad camera connection with inside code {res}', 'code': 6}}
            
    return {request.path: False, 'data': {'answer': 'Camera with such ID do not exist', 'code': 2}}