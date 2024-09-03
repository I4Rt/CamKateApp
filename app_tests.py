from model.abstracts.CameraApi import *
from tools.testing import *
import numpy as np

def testCamApi():
    route = 0
    cam_api = CameraApi(route)
    
    assert_values(cam_api.connect(), True, 'Тест подключения')
    assert_values(cam_api.connect(), True, 'Тест повторного подключения')
    
    res = cam_api.getFrame()
    assert_values(res[0], True, 'Тест чтения фрейма')
    assert_values(type(res[1]), np.ndarray, 'Тест значения фрейма')
    
    assert_values(cam_api.disconnect(), True, 'Тест разрыва подключения')
    assert_values(cam_api.disconnect(), True, 'Тест повторного разрыва подключения')
    
if __name__ == '__main__':
    testCamApi()