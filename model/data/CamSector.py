from config import *
from model.data.BaseData import *
from model.data.Box import *
from model.data.Camera import *

class CamSector(BaseData):
    __tablename__ = 'cam_sector'
    name = Column(String, nullable=False, unique=True)
    camera = relationship("Camera", uselist=False, back_populates="cam_sector")
    boxes = relationship('Box', cascade="all,delete", backref='cam_sector', lazy='select')
    
    def __init__(self, name, id=None):
        super().__init__(id)
        self.name = name
        
    def getBoxes(self) -> List[Box]:
        with DBSessionMaker.getSession() as ses:
            return ses.query(Box).filter_by(cam_sector_id=self.id).all()
        
    def getCamera(self):
        with DBSessionMaker.getSession() as ses:
            return ses.query(Camera).filter_by(cam_sector_id=self.id).first()
        
    def delete(self):
        with DBSessionMaker.getSession() as ses:
            ses.query(Camera).filter_by(cam_sector_id=self.id).delete()
            ses.delete(self)
            ses.commit()
            
    
            