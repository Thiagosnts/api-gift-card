from datetime import datetime
from pydantic import BaseModel, Field 
from src.domain.produtoDB import Produto
from typing import List,Optional
import uuid

class Produtodto(BaseModel):
    cnpj:Optional[int]=Field(None, alias="cnpj",gt=1,le=99999999999999)
    nome:str=Field(..., alias="nome", min_length=1)
    valor: float=Field(..., alias="valor", ge=00.1)

    def getCommand(self):
        return Produto(
            cnpj=int(self.cnpj),
            nome=self.nome,
            valor=str(self.valor)
        )

