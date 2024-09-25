from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from models import Base


class Promotion(Base):

    __tablename__ = 'promotion_catalog'

    id = Column("pk_promotion", Integer, primary_key=True)
    name = Column(String(200))   
    discount = Column(Integer)


    def __init__(self, name, discount):
     """
        Cria uma Promoção
        Arguments:
            name: name
            discount: discount
            
     """
     self.name = name
     self.discount = discount

     def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Categoria.
        """
        return{
            "id": self.id,
            "name": self.name,
            "discount": self.discount,
            
            
        }
    
    def __repr__(self):
        """
        Retorna uma representação da promoção em forma de texto.
        """
        return f"Promotion(id={self.id}, name='{self.name}', )"

