from pydantic import BaseModel, Base64Bytes
from typing import Optional, List
from models.category import Category


class CategorySchema(BaseModel):
    """ Define como uma nova categoria vai ser inserida
    """
    
    name: str = "Docker Certified Associate"
    description: str = "Automação, CI/CD, containers orquestração, infraestrutura como código e monitoramento."
    file: Base64Bytes = "Image"
    #image_category: str = "teste image"


class CategoryViewSchema(BaseModel):
    """ Define como uma categoria será retornado: categoria
    """
    id: int = 1
    name: str = ""

class CategoriesListSchema(BaseModel):
    """ Define como uma listagem de categorias será retornada.
    """
    categories:List[CategoryViewSchema]


class CategoryDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int


class FindCategoryByIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apen com base no ID da categoria.
    """
    id: int = "1"


def apresenta_categorias(categories: List[Category]):
    """ Retorna uma representação da categoria seguindo o schema definido em ListagemCategoriasSchema.
    """
    result = []
    for category in categories:
        result.append({
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "image_category": category.image_category,
        })
    
    return {"categories": result}


def apresenta_categoria(category: Category):
    """ Retorna uma representação do course seguindo o schema definido em
        Category
    """
    return {
        "id": category.id,
        "name": category.name,
        "description": category.description
        
    }