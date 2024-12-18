from model.abstracts.StopableThread import *
from time import sleep
from model.data.CamSector import *
from web_contollers.api.main_rest_controller import *
from model.abstracts.updated_camera_tools.CameraPictureGetter import *
from tools import FullAnalize

class DefectsThread(StopableThread):

    def __init__(self):
        super().__init__(target=DefectsThread.startThread)

    # def startThread(self):
    #     defectThread = StopableThread(target=self.getBoxesFromCam)
    #     # return defectThread

    #     # defectThread.start()
    #     # sleep(5)
    #     # defectThread.stop()
    #     # defectThread.join()
    @staticmethod
    def startThread():
        print('getBoxesFromCam')
        while True:
            print('run')
            FullAnalize.run()
            print('sleep')
            sleep(5)
        
        # camSecs = CamSector.getAll()
        # for camSec in camSecs:
        #     cam = camSec.getCamera()
        #     camSecBoxes = camSec.getBoxes()
        #     res, pic, info = CameraPictureGetter.getPicture(cam)

        #     print(camSecBoxes.x1, camSecBoxes.y1, camSecBoxes.x2, camSecBoxes.y2)
        # sleep(10)