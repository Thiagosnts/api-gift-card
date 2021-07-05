from pydantic import BaseModel,Field
from typing import Optional, List

    
class ResponseProduto(BaseModel):
  
    valor: Optional[str]=Field(None, alias="valor")
    nome:Optional[str]=Field(None, alias="nome")



