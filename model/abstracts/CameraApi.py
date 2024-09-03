
import cv2
from config import *

class CameraApi:
    def __init__(self, route) -> None:
        
        self.route = route
        self.stream = None
        
        self.isConnected = False
        self.streamError = False
        
    
    def connect(self, force=False):
        try:
            if force or not self.isConnected:
                self.stream = cv2.VideoCapture(self.route)
                self.error = False
                self.isConnected = True
            return True
        except Exception as e:
            logger.info(f'Error: connecting to the camera | {e}')
            self.isConnected = False
            self.error = True
        return False
        
    def disconnect(self):
        try:
            if self.stream:
                self.stream.release()
                if self.stream.isOpened():
                    raise Exception('Stream not closed')
                self.stream = None
            self.isConnected = False
            self.error = False
            return True
        except Exception as e:
            logger.info(f'Error: releasing the camera connection | {e}')
            self.error = True
        return False
            
    def getFrame(self):
        try:
            if self.isConnected and self.stream and not self.error:
                if self.stream.isOpened():
                    res, frame =  self.stream.read()
                    return res, frame
                logger.info(f'Error: frame acquisition | mismatch of states {self.stream} {self.stream.isOpened()} {self.isConnected}')
                self.error = True
        except Exception as e:
            logger.info(f'Error: getting a frame | {e}')
            self.error = True
        return False, None