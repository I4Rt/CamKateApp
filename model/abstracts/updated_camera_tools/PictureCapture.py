from config import *
from multiprocessing import Process, Event

class PictureCapture:
    '''
        SHIT SHIT SHIT SHIT SHIT SHIT SHIT SHIT SHIT\n
        
        При создании инифиализирует поток подключения к камере\n
        Пока поток жив отдает картинки, иначе не отдает ничего\n
        Mожно инкапсулировано начать или остановить поток чтения 
        изображений используя функцию "start" или "stop" 
        соответственно
    '''
    def __init__(self, camRoute) -> None:
        self.__bufferDict = MANAGER.dict()
        self.pictureGetterStream = PictureCapture.__PictureGetterStream(camRoute, self.__bufferDict)
        
    def getImage(self):
        if self.pictureGetterStream.isAlive():
            try:
                return True, self.__bufferDict['image'] # BOOLshit
            except: # handle key fucking error
                pass
        return False, None
    
    def stop(self):
        self.pictureGetterStream.stop()
        
    def start(self):
        self.pictureGetterStream.start()
        
    def isActive(self):
        return self.pictureGetterStream.isAlive()
          
    class __PictureGetterStream:
        '''
            HOLE HOLE HOLE HOLE HOLE HOLE HOLE HOLE HOLE\n
            
            Инкапсулирует функцию сбора видеоизображения\n
            Дает возможность прерывать сбор данных с камер
        '''
        def __init__(self, cam_route, buferLink):
            self.stopEvent = Event()
            self.captureProcess = Process(target = self.task, args=(cam_route, buferLink))
            
        def task(self, cam_route, buferLink):
            stream = cv2.VideoCapture(cam_route)
            if stream.isOpened():
                while not self.stopEvent.is_set():
                    res, buferLink['image'] = stream.read() # BOOLshit
                    
        def isAlive(self):
            return self.captureProcess.is_alive()
        
        def start(self):
            self.captureProcess.start()
        
        def stop(self):
            self.stopEvent.set()
