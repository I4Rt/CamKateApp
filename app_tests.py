from model.abstracts.CameraApi import *
from model.abstracts.TestsDB import *
from model.abstracts.CameraHolder import *
from model.abstracts.updated_camera_tools.CameraPictureGetter import *
from model.abstracts.updated_camera_tools.PictureCapture import *
from model.abstracts.updated_camera_tools.VideoCaptureHolder import *
from tools.testing import *
import numpy as np

from matplotlib import pyplot as plt

def testCamApi(route=0):

    cam_api = CameraApi(route)
    
    assert_values(cam_api.connect(), True, 'Тест подключения')
    assert_values(cam_api.connect(), True, 'Тест повторного подключения')
    
    res = cam_api.getFrame()
    assert_values(res[0], True, 'Тест чтения фрейма')
    assert_values(type(res[1]), np.ndarray, 'Тест значения фрейма')
    
    assert_values(cam_api.disconnect(), True, 'Тест разрыва подключения')
    assert_values(cam_api.disconnect(), True, 'Тест повторного разрыва подключения')

def testDBRequests():
    tests_db = TestsDB()

    tests_db.delete_box()
    tests_db.delete_camera()
    tests_db.delete_camera_sec()

    assert_values(tests_db.save_camera_sec(), True, 'Тест сохранения экземпляра сектора')
    assert_values(tests_db.save_box(), True, 'Тест сохранения бокса')
    assert_values(tests_db.save_camera(), True, 'Тест сохранения экземпляра камеры')
    

    assert_values(tests_db.set_camera_sec_to_box(), True, 'Тест привязки сектора к боксу')
    assert_values(tests_db.set_camera_sec_to_camera(), True, 'Тест привязки сектора к камере')

    assert_values(tests_db.get_all_boxes(), True, 'Тест получения всех боксов')
    assert_values(tests_db.get_all_cameras(), True, 'Тест получения всех камер')
    assert_values(tests_db.get_all_camera_sectors(), True, 'Тест получения всех секторов')
    
    assert_values(tests_db.get_by_id_box(), True, 'Тест получения бокса по id')
    assert_values(tests_db.get_by_id_camera(), True, 'Тест получения камеры по id')
    assert_values(tests_db.get_by_id_camera_sec(), True, 'Тест получения сектора по id')

    assert_values(tests_db.delete_box(), True, 'Тест удаления бокса')
    assert_values(tests_db.delete_camera(), True, 'Тест удаления камеры')
    assert_values(tests_db.delete_camera_sec(), True, 'Тест удаления сектора')    

def camHolderTest():
    CameraHolder.getInstance().addCameras(Camera.getAll())
    lastCam = Camera.getLast()
    res1 = assert_values(CameraHolder.getInstance().checkCamera(lastCam), True, 'Проверка наличия камеры')
    if res1:
        CameraHolder.getInstance().delCamera(lastCam)
        res2 = assert_values(CameraHolder.getInstance().checkCamera(lastCam), False, 'Проверка удаления камеры')
    
    res = CameraHolder.getInstance().getCameraFrame(lastCam)
    assert_values(res[0], False, 'Проверка взятия картинки с ошибкой')
    
    i = 1
    while i < 11:
        print(f'Цикл {i}')
        CameraHolder.getInstance().addCameras(Camera.getAll())
        res = CameraHolder.getInstance().refreshCameraConnection(lastCam)
        assert_values(res, True, 'Проверка подключения к стриму')
        
        res = CameraHolder.getInstance().getCameraFrame(lastCam)
        assert_values(res[0], True, 'Проверка взятия картинки')
        
        CameraHolder.getInstance().delCamera(lastCam)
        res = assert_values(CameraHolder.getInstance().checkCamera(lastCam), False, 'Проверка удаления камеры')
        i += 1
    

def testCamerasUpdated(route = 0):
    camera = Camera.getLast()   
    for i in range(6):
        res, pic, info = CameraPictureGetter.getPicture(camera)
        print(res, pic, info )
        sleep(3)
    sleep(10)
    VideoCaptureHolder.getInstance().stopDemon()
    # plt.imshow(pic)
    


if __name__ == '__main__':
    MANAGER = Manager()
    PictureCapture.setManager(MANAGER)
    # print("Тесты подключения к камере")
    # testCamApi(0)
    
    # print('\nТесты запросов к БД')
    # testDBRequests()
    
    # print('\nТесты подключений к камерам')
    # camHolderTest()
    testCamerasUpdated()

    

