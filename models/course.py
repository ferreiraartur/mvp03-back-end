from sqlalchemy import Column, String, Integer, DateTime, Float, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union
from models import Base
from sqlalchemy import LargeBinary

class Course(Base):

    __tablename__ = 'course_catalog'

    id = Column("pk_course", Integer, primary_key=True)
    title = Column(String(200))
    price = Column(Float)
    content = Column(String(200))
    imageURL = Column(String(200))
    #category = Column(String(200))
    filename = Column(String(120), nullable=False)
    filepath = Column(String(120), nullable=False)
    image_data = Column(LargeBinary, nullable=False)
    #category_id = Column(Integer, ForeignKey('category_catalog.pk_category'), nullable=False)

    data_insercao = Column(DateTime, default=datetime.now())

    def __init__ (self,  title, price, content, imageURL, category, filename, filepath, image_data,
                  data_insercao:Union[DateTime, None] = None):
        """
            Cria um Curso

            Arguments:
                title: título.
                price: preço
                content: content
                imageURL: imageURL
                category: category
                filename: filename
                data_insercao: data_insercao
        
        """
        self.title = title
        self.price = price
        self.content = content
        self.imageURL = imageURL
        self.category = category
        self.filename = filename
        self.filepath = filepath
        self.image_data = image_data
        data_insercao = data_insercao

        if data_insercao:
            self.data_insercao = data_insercao
    
    def to_dict(self):
        """
        Retorna a representação em dicionário do Objeto Curso.
        """
        return{
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "content": self.content,
            "imageURL": self.imageURL,
            "category": self.category,
            "filename": self.filename,
            "filepath": self.filepath,
            "image_data": self.image_data,
            "data_insercao": self.data_insercao
        }
    
    def __repr__(self):
        """
        Retorna uma representação do Curso em forma de texto.
        """
        return f"Curso(id={self.id}, name='{self.title}', )"