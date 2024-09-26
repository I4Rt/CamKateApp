# from config import *
from multiprocessing import Process, Event, Manager
import cv2
from time import sleep
class PictureCapture:
    
    '''
        SHIT SHIT SHIT SHIT SHIT SHIT SHIT SHIT SHIT\n
        
        При создании инифиализирует поток подключения к камере\n
        Пока поток жив отдает картинки, иначе не отдает ничего\n
        Mожно инкапсулировано начать или остановить поток чтения 
        изображений используя функцию "start" или "stop" 
        соответственно
    '''
    __MANAGER = None
    
    def __init__(self, camRoute:str) -> None:
        self.__bufferDict = PictureCapture.__MANAGER.dict()
        self.stopEvent = Event()
        
        self.captureProcess = Process(target = self.task, args=(int(camRoute) if camRoute.isdigit() else camRoute, self.__bufferDict))

    def task(self, cam_route, buferLink):
        stream = cv2.VideoCapture(cam_route)
        # buferLink['info'] = stream.isOpened()
        if stream.isOpened():
            while not self.stopEvent.is_set():
                try:
                    res, buferLink['image'] = stream.read() # BOOLshit
                    # buferLink['imgGet'] = res
                except:
                    break
                
    
    @classmethod
    def setManager(cls, manager):
        cls.__MANAGER = manager
        
    def getImage(self):
        if self.isActive():
            try:
                return True, self.__bufferDict['image'] # BOOLshit
            except: # handle key fucking error
                pass
        return False, None
    
    def stop(self):
        self.stopEvent.set()
        
    def start(self):
        self.captureProcess.start()
        
    def isActive(self):
        return self.captureProcess.is_alive()
    
if __name__ == "__main__":
    MANAGER = Manager()
    PictureCapture.setManager(MANAGER)
    ps = PictureCapture("0")
    ps.start()
    for i in range(10):
        sleep(1)
        print(ps.getImage())
    ps.stop()
    sleep(1)