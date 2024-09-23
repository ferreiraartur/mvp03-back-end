from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from models import Base
from sqlalchemy import LargeBinary

class Category(Base):

    __tablename__= 'category_catalog'
    
    id = Column("pk_category", Integer, primary_key=True)
    name = Column(String(200))   
    description = Column(String(200))
    image_category = Column(LargeBinary, nullable=False)
    

    def __init__(self, name, description, image_category):
     """
        Cria uma Categoria
        Arguments:
            name: name
            description: description
            image_category: image_category
            
     """
     self.name = name
     self.description = description
     self.image_category = image_category

     def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Categoria.
        """
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image_category": self.image_category,
            
        }
    
    def __repr__(self):
        """
        Retorna uma representação da categoria em forma de texto.
        """
        return f"Category(id={self.id}, name='{self.name}', )"
        
    
    
    

