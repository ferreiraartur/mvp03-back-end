from pydantic import BaseModel
from typing import Optional, List
from models.promotion import Promotion


class PromotionSchema(BaseModel):
    """ Define como um novo course vai ser inserido e representado
    """
    
    name: str = "Natal10"
    discount: int = "10"


class FindPromotionBySchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da Promoção.
    """
    termo: str = "Natal10"


class FindPromotionByIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apen com base no ID da Promoção.
    """
    id: int = "1"


class PromotionListSchema(BaseModel):
    """ Define como uma listagem de courses será retornada.
    """
    promotions:List[PromotionSchema]


def apresenta_promotions(promotions: List[Promotion]):
    """ Retorna uma representação da promotion seguindo o schema definido em ListagemPromotionSchema.
    """
    result = []
    for promotion in promotions:
        result.append({
            "id": promotion.id,
            "name": promotion.name,
            "discount": promotion.discount,
        })
    
    return {"promotions": result}


def apresenta_promotion(promotion: Promotion):
    """ Retorna uma representação da promotion seguindo o schema definido em
        PromotionViewSchema.
    """
    return {
        "id": promotion.id,
        "name": promotion.name,
        "discount": promotion.discount,
        
    }
