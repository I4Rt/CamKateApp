from config import *
from model.data.BaseData import *

class Box(BaseData):
    __tablename__ = 'box'
    
    
    name = Column(String, nullable=False)
    x1 = Column(Double, nullable=False) # in percents
    y1 = Column(Double, nullable=False) # in percents
    x2 = Column(Double, nullable=False) # in percents
    y2 = Column(Double, nullable=False) # in percents
    cam_sector_id = Column(Integer, ForeignKey('cam_sector.id', ondelete="CASCADE"), nullable=False)
    
    __table_args__ = (UniqueConstraint('cam_sector_id', 'name'), )
    
    def __init__(self, name, x1, y1, x2, y2, id=None):
        super().__init__(id)
        
        self.name = name
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        
    def setCamSector(self, cs:"CamSector"):
        if cs.id:
            self.cam_sector_id = cs.id
            self.save()
            return True
        return False
    
    def setCamSectorById(self, cs_id:"CamSector"):
        self.cam_sector_id = cs_id
        self.save()
        return True
    
    def getInfo(self):
        return [self.name, self.x1, self.y1, self.x2, self.y2, self.id]
        