from model.data.Camera import *

class CameraHolder:
    __instance = None
    def __init__(self) -> None:
        self.cameras:List[Camera] = []
        
    @classmethod
    def getInstance(cls) -> "CameraHolder":
        if cls.__instance is None:
            cls.__instance = CameraHolder()
        return cls.__instance
         
    def addCameras(self, cameraList:Camera):
        for cam in cameraList:
            if cam not in self.cameras:
                self.cameras.append(cam)
                
    def checkCamera(self, camera:Camera):
        return camera in self.cameras
    
    def refreshCameraConnection(self, camera:Camera):
        if self.checkCamera(camera):
            cam_ind = self.cameras.index(camera)
            con_res = self.cameras[cam_ind].connect()
            
            if con_res:
                return True
            self.cameras[cam_ind].disconnect()
            cameraInstance = self.cameras.pop(cam_ind)
            del cameraInstance
        return False
            
    def delCamera(self, cam: Camera):
        if cam in self.cameras:
            cameraInstance = self.cameras.pop(self.cameras.index(cam))
            cameraInstance.disconnect()
            del cameraInstance
        return True
            
    def getCameraFrame(self, cam: Camera):
        if cam in self.cameras:
            res, frame = self.cameras[self.cameras.index(cam)].getFrame()
            return res, frame
        return False, None