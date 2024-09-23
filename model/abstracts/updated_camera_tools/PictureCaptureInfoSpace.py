from datetime import datetime
from model.abstracts.updated_camera_tools.PictureCapture import *

class PictureCaptureInfoSpace:
    
    def __init__(self, route) -> None:
        self.route = route
        self.picCapture = PictureCapture(route)
        self.startTime = None
    
    def getRoute(self):
        return self.route
        
    def getPicture(self):
        return self.picCapture.getImage()
    
    def captureIsActive(self) -> bool:
        return self.picCapture.isActive()
    
    def startCaptureing(self) -> bool:
        if self.startTime == None:
            self.startTime = datetime.now()
            if not self.picCapture.isActive():
                self.picCapture.start()
                return True
        return False
    
    def stopCapturing(self) -> bool:
        self.picCapture.stop()
        return not self.picCapture.isActive()
    
    def getStartTime(self) -> datetime | None:
        return self.startTime
    
    def updateTime(self):
        self.startTime = datetime.now()