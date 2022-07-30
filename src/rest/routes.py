
from datetime import time
from fastapi import APIRouter
from src.rest.dto.produto_dto import Produtodto
from datetime import datetime
import time
from src.domain.produtoDB import ProdutoDB
from src.core.controle import Controle, TipoEnum
from threading import Thread
import time

router = APIRouter()
ProdutoDB().criarTabela()

@router.get("/product",
            tags=["Listar Produtos..."],
            status_code=200)
def Listar_catálogo():
    lista = Controle().fluxo(tipo=TipoEnum.listar)
    return (lista)


@router.post("/product",
             tags=[" Cadastrando Produtos..."],
             status_code=200)
def Cadastrar_GiftCard(dto: Produtodto = None):
    obj = dto.getCommand()
    response = Controle().fluxo(tipo=TipoEnum.salvar, obj=obj)
    return (response)


@router.delete("/product/{item_id}",
               tags=[" Deletando Produtos..."],
               status_code=200)
def Deletar_GiftCard(item_id: str):
    response = Controle().fluxo(tipo=TipoEnum.deletar, item_id=int(item_id))
    return (response)


@router.put("/product/{item_id}",
            tags=["Atualizando Produtos..."],
            status_code=200)
def Atualizar_GiftCard(item_id: str, dto: Produtodto):
    obj = dto.getCommand()
    response = Controle().fluxo(tipo=TipoEnum.atualizar, item_id=int(item_id), obj=obj)
    return (response)


@router.post("/product/{item_id}/confirm",
             tags=["Obtendo PIN..."],
             status_code=200)
def Obter_PIN(item_id: str):
    response = Controle().fluxo(tipo=TipoEnum.gerarGift, item_id=int(item_id))
    return (response)


@router.get("/productPIN",
            tags=["Listar PIN..."],
            status_code=200)
def Listar_catálogo():
    lista = Controle().fluxo(tipo=TipoEnum.listaPIN)
    return (lista)


@router.post("/productPIN/{pin}/activate",
             tags=["Ativar PIN..."],
             status_code=200)
def Ativar_PIN(pin: str):
    lista = Controle().fluxo(TipoEnum.activate, item_id=pin)
    return (lista)


# @router.get("/assincrono",
#              tags=["Ativar PIN..."],
#              status_code=200)
# def assincrono():

#     obj1 = Thread(target=segundo_plano,args=[1.1,"Ed"])
#     # obj2 = Thread(target=func2,args=[1.2,"Paulo"])

#     obj1.start()
#     # obj2.start()

#     return "Tudo certo3"

# def segundo_plano(velocidade,nome):
#         time.sleep(0.7)
#         print("Pedido Autorizado !!!"+str(datetime.now()))
