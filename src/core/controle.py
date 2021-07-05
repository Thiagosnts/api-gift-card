from starlette import responses
from src.domain.produtoDB import ProdutoDB
from enum import Enum
from src.rest.errors import launch_http_exception
from fastapi import status



class TipoEnum(Enum):
    listar = 'listar'
    salvar = 'salvar'
    atualizar = 'atualizar'
    deletar = 'deletar'
    gerarGift = 'gerarGift'
    listaPIN = 'listaPIN'
    activate = 'activate'

class Controle():


    def fluxo(self,tipo=None,item_id=None,obj=None):

        itens={'item_id':item_id,'obj':obj}


        action={

            TipoEnum.listar: ProdutoDB().pegarProduto,

            TipoEnum.salvar:ProdutoDB().salvarProduto,

            TipoEnum.atualizar:ProdutoDB().atualizar,

            TipoEnum.deletar:ProdutoDB().deletar,

            TipoEnum.gerarGift:ProdutoDB().geraProdutoGift,

            TipoEnum.listaPIN:ProdutoDB().listaProdutoPIN,

            TipoEnum.activate:ProdutoDB().ativarProdutoGift
        }
        response=action[tipo](itens)

        return self.verificar_erro(response)

    def verificar_erro(self,response):
        if response.ok:
            return response.json()
        else:
            launch_http_exception(response.status_code, response.json(),"Ocorreu um erro !!!")

  
            
       



