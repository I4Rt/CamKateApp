from config import *
from model.data.BaseData import *

class BasePoint(BaseData):
    '''
        Хранение информации о репере для отсчета до простенков касет
    '''

    __tablename__ = 'base_point'
    
    
    x1 = Column(Double, nullable=False) # in percents
    y1 = Column(Double, nullable=False) # in percents
    x2 = Column(Double, nullable=False) # in percents
    y2 = Column(Double, nullable=False) # in percents
    
    cam_sector_id = mapped_column(ForeignKey("cam_sector.id"), nullable=False, unique=True)
    cam_sector = relationship("CamSector", back_populates="basePoint")
    
    
    def __init__(self, cam_sector_id, x1, y1, x2, y2, id=None):
        super().__init__(id)
        
        self.cam_sector_id = cam_sector_id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    @classmethod 
    def getByCameraSectorId(cls, searchId:int) -> "BasePoint":
        with DBSessionMaker.getSession() as ses:
            value = ses.query(cls).filter_by(id=searchId).first()
            return value
    
    def getInfo(self):
        return [self.x1, self.y1, self.x2, self.y2, self.cam_sector_id, self.id]
        