from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from models import Base


class Cupom(Base):

    __tablename__ = 'cupom_catalog'

    id = Column("pk_cupom", Integer, primary_key=True)
    name = Column(String(200))   
    discount = Column(Integer)
    valid = Column(Boolean, default=True)


    def __init__(self, name, discount, valid):
     """
        Cria um cupom
        Arguments:
            name: name
            discount: discount
            valid: valid
            
     """
     self.name = name
     self.discount = discount
     self.valid = valid

     def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Cupom.
        """
        return{
            "id": self.id,
            "name": self.name,
            "discount": self.discount,
            "valid": self.valid,
            
            
        }
    
    def __repr__(self):
        """
        Retorna uma representação da promoção em forma de texto.
        """
        return f"Cupom(id={self.id}, name='{self.name}', valid='{self.valid}',)"

