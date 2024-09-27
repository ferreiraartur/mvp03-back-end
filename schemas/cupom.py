from pydantic import BaseModel
from typing import Optional, List
from models.cupom import Cupom


class CupomSchema(BaseModel):
    """ Define como um novo course vai ser inserido e representado
    """
    
    name: str = "Natal10"
    discount: int = "10"
    valid: bool = "true"
    


class FindCupomBySchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Cupom.
    """
    code: str = "Natal10"


class FindCupomByIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apen com base no ID do Cupom.
    """
    id: int = "1"


class CupomListSchema(BaseModel):
    """ Define como uma listagem de cupons será retornada.
    """
    promotions:List[CupomSchema]


class CupomDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int


def apresenta_cupons(cupons: List[Cupom]):
    """ Retorna uma representação do cupom seguindo o schema definido em ListagemCupomSchema.
    """
    result = []
    for cupom in cupons:
        result.append({
            "id": cupom.id,
            "name": cupom.name,
            "discount": cupom.discount,
            "valid": cupom.valid,
        })
    
    return {"cupons": result}


def apresenta_cupom(cupom: Cupom):
    """ Retorna uma representação da promotion seguindo o schema definido em
        PromotionViewSchema.
    """
    return {
        "id": cupom.id,
        "name": cupom.name,
        "discount": cupom.discount,
        "valid": cupom.valid,
        
    }
