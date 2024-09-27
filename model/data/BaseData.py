from config import *
from typing import List
from model.abstracts.Jsonifyer import *
from sqlalchemy import or_, and_
from datetime import datetime

from model.abstracts.DBSessionMaker import *

class BaseData(Jsonifyer, Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    
    def __init__(self, id = None):
        Jsonifyer.__init__(self)
        self.id = id
             
    def __save(self):
        with DBSessionMaker.getSession() as ses:
            ses.add(self)
            ses.commit()
            return self.id
        
    def save(self):
        self:self.__class__ = self.getByID(self.__save())
        
    @classmethod 
    def getAll(cls) -> List["BaseData"]:
        with DBSessionMaker.getSession() as ses:
            value = ses.query(cls).all()
            return value

    @classmethod
    def getLast(cls) -> "BaseData":
        with DBSessionMaker.getSession() as ses:
            # print('\ngetLast')
            # print(datetime.now())
            value = ses.query(cls).order_by(cls.id.desc()).first()
            # print(datetime.now())
            return value
        
    @classmethod 
    def getByID(cls, searchId:int) -> "BaseData":
        with DBSessionMaker.getSession() as ses:
            # print('\ngetByID')
            # print(datetime.now())
            value = ses.query(cls).filter_by(id=searchId).first()
            # print(datetime.now())
            return value

    def delete(self):
        with DBSessionMaker.getSession() as ses:
            ses.delete(self)
            ses.commit()
            
    @classmethod
    def deleteAll(cls):
        with DBSessionMaker.getSession() as ses:
            res = ses.query(cls).delete()
            ses.commit()
            print(f'deleted {res}')
            
    @classmethod
    def deleteByID(cls, targetId):
        with DBSessionMaker.getSession() as ses:
            res = ses.query(cls).filter_by(id=targetId).delete()
            ses.commit()
            print(f'deleted {res}')
              
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.getParamsList()}>"
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.getParamsList()}"
    
    
    
        
    