from config import *
from model.data.BaseData import *

class Measurement(BaseData):
    __tablename__ = 'measurement'
    
    
    type = Column(String, nullable=False)
    value = Column(Double)
    datetime = Column(DateTime(timezone=False), nullable=False)

    box_id = Column(Integer, ForeignKey('box.id', ondelete="CASCADE"), nullable=False)
    
    def __init__(self, type_, val, box_id, id=None):
        super().__init__(id)
        
        self.type = type_
        self.value = val
        self.box_id = box_id
        self.datetime = datetime.now()

    @classmethod
    def getMeasurements(cls, camSecId, beginTime = None, end_time = None):
        with DBSessionMaker.getSession() as ses:
            sqlQuery = f'''
                    SELECT m.type, m.value, m.datetime, m.box_id 
                    FROM public.measurement m 
                    JOIN public.box b ON b.id = m.box_id 
                    where b.cam_sector_id={camSecId}
                '''
            if beginTime:
                sqlQuery += f' and m.datetime > \'{beginTime}\' '
                if end_time:
                    sqlQuery += f'and m.datetime < \'{end_time}\' '
            elif end_time:
                sqlQuery += f'and m.datetime < \'{end_time}\' '
            sqlQuery += 'order by m.datetime;'

            res = ses.execute(text(sqlQuery))
            ses.commit()
            return list(map( lambda row: row[:], res))
        