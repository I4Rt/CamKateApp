from config import *
from model.data.BaseData import *


class Camera(BaseData):
    __tablename__ = 'camera'
    
    route = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    correction_coefs = Column(String, nullable=False,  unique=False)
    
    cam_sector_id = mapped_column(ForeignKey("cam_sector.id"), nullable=True)
    cam_sector = relationship("CamSector", back_populates="child")
    
    def __init__(self, route, name, correction_coefs, id=None):
        super().__init__(id)
        self.route = route
        self.name = name
        self.correction_coefs = correction_coefs
        
    def setCamSector(self, cs:"CamSector"):
        if cs.id:
            self.cam_sector_id = cs.id
            self.save()
            return True
        return False