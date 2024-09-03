from config import *
from model.data.BaseData import *
from model.data.Box import *
from model.data.Camera import *

class CamSector(BaseData):
    __tablename__ = 'cam_sector'
    name = Column(String, nullable=False, unique=True)
    camera = relationship("Camera", uselist=False, back_populates="parent")
    boxes = relationship('Box', cascade="all,delete", backref='target', lazy='select')
    
    def __init__(self, name, id=None):
        super().__init__(id)
        self.name = name
        
        
        
    