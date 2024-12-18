from model.abstracts.updated_camera_tools.PictureCaptureInfoSpace import *
from model.abstracts.StopableThread import StopableThread

class VideoCaptureHolder:
    __instance:"VideoCaptureHolder" = None
    __KILL_INTERVAL = 0.5
    __KILL_TIMEOUT = 10
    
    def __init__(self) -> None:
        self.__connections:dict["Any", PictureCaptureInfoSpace] = {}
        self.__demon = StopableThread(target = self.__killThreadTask, looped=True, loop_interval=self.__KILL_INTERVAL)
        self.__demon.start()
        print('started')
        
    @classmethod
    def init(cls):
        cls.getInstance()
        
    
    def stopDemon(self):
        self.__demon.stop()
        self.__demon.join()
    
    @classmethod
    def getInstance(cls) -> "VideoCaptureHolder":
        if cls.__instance == None:
            cls.__instance = VideoCaptureHolder()
        return cls.__instance
    
    def addConnection(self, identifyer, route): 
        '''
            returns: \n
            1 # новое подключение добавлено\n
            2 # подключение обновлено\n
            3 # подключение не обновлено, его срок жизни заканчился\n
            4 # еблан (ты) пытается запихнуть не тот route под существующим identifyer
        '''            
        # TODO: по этим ебучим таймерам лучше сделать 
        #       интервалы неактивности, когда подключение 
        #       уже просто тупо ожидает удаления 
        # TODO: добавить проверку на существование route 
        #       в списке под другим identifyer    
        if not (identifyer in list(self.__connections.keys())):
            self.__connections[identifyer] = PictureCaptureInfoSpace(route)
            self.__connections[identifyer].startCaptureing()
            return 1 # новое подключение добавлено
        elif self.__connections[identifyer].getRoute() == route:
            if self.__connections[identifyer].captureIsActive():
                self.__connections[identifyer].updateTime()
                return 2 # подключение обновлено
            return 3 # подключение не обновлено, поток завершен
        return 4 # еблан (ты) пытается запихнуть не тот route под существующим identifyer
    
    def getPicture(self, identifier):
        if identifier in self.__connections.keys():
            res, pic = self.__connections[identifier].getPicture()
            if res:
                return 1, pic # нормальный ответ
            if self.__connections[identifier].captureIsActive():
                return 2, None # картинка не пришла
            return 3, None # подключение недоступно
        return 4, None # по данному identifyer нчего нет
    
    
    # TODO: переписать в класс
    
    def __killThreadTask(self):
        # print(self.__connections)
        del_list = []
        for con_key in self.__connections:
            # print(con_key, (datetime.now() - self.__connections[con_key].getStartTime()).total_seconds(), self.__KILL_TIMEOUT)
            if (datetime.now() - self.__connections[con_key].getStartTime()).total_seconds() > self.__KILL_TIMEOUT:
                i = 0
                while self.__connections[con_key].stopCapturing():
                    i += 1
                    if i > 9:
                        break
                del_list.append(con_key)
                
        for key in del_list:
            self.__connections.pop(key)
                
                