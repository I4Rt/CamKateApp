from config import *
from model.data.BaseData import *
from model.abstracts.CameraApi import *

class Camera(BaseData): #, CameraApi):
    __tablename__ = 'camera'
    
    route = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    camera_matrix = Column(String, nullable=False,  unique=False)
    coefs = Column(String, nullable=False,  unique=False)

    
    cam_sector_id = mapped_column(ForeignKey("cam_sector.id"), nullable=True)
    cam_sector = relationship("CamSector", back_populates="camera")
    

    def __init__(self, route, name, camera_matrix, coefs, id=None):
        BaseData.__init__(self, id)
        # CameraApi.__init__(self, route)
        self.route = route
        self.name = name
        self.camera_matrix = camera_matrix
        self.coefs = coefs
        
    def setCamSector(self, cs:"CamSector"):
        if cs.id:
            self.cam_sector_id = cs.id
            self.save()
            return True
        return False
    
    def getCorrectValues(self):
        cm = self.camera_matrix.strip('{}')
        coefs = self.coefs.strip('{}')
        cm = [list(map(float, group.split(','))) for group in cm.split('},{')]
        coefs = [float(i) for i in coefs.split(',')]
        return cm, coefs
    
    def getInfo(self):
        return [self.route, self.camera_matrix, self.coefs]
    
    def __eq__(self, other:"Camera"):
        if type(other) == Camera:
            return self.id == other.id 
        return False

