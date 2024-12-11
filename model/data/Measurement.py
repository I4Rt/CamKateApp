from config import *
from model.data.BaseData import *

class Measurement(BaseData):
    __tablename__ = 'measurement'
    
    
    type = Column(String, nullable=False)
    value = Column(Double, nullable=False)
    datetime = Column(DateTime(timezone=False), nullable=False)

    box_id = Column(Integer, ForeignKey('box.id', ondelete="CASCADE"), nullable=False)
    
    def __init__(self, type_, val, box_id, id=None):
        super().__init__(id)
        
        self.type = type_
        self.value = val
        self.box_id = box_id
        self.datetime = datetime.now()
        