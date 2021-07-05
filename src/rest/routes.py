
from fastapi import APIRouter
from src.rest.dto.produto_dto import Produtodto


from src.domain.produtoDB import ProdutoDB
from src.core.controle import Controle, TipoEnum


router = APIRouter()
ProdutoDB().criarTabela()

@router.get("/product",
            tags=["Listar Produtos..."],
            status_code=200)
def Listar_catálogo():
    lista = Controle().fluxo(TipoEnum.listar)
    return (lista)


@router.post("/product",
             tags=[" Cadastrando Produtos..."],
             status_code=200)
def Cadastrar_GiftCard(dto: Produtodto = None):
    obj = dto.getCommand()
    response = Controle().fluxo(TipoEnum.salvar, None, obj)
    return (response)


@router.delete("/product/{item_id}",
               tags=[" Deletando Produtos..."],
               status_code=200)
def Deletar_GiftCard(item_id: str):
    response = Controle().fluxo(TipoEnum.deletar, int(item_id))
    return (response)


@router.put("/product/{item_id}",
            tags=["Atualizando Produtos..."],
            status_code=200)
def Atualizar_GiftCard(item_id: str, dto: Produtodto):
    obj = dto.getCommand()
    response = Controle().fluxo(TipoEnum.atualizar, item_id, obj)
    return (response)


@router.post("/product/{item_id}/confirm",
             tags=["Obtendo PIN..."],
             status_code=200)
def Obter_PIN(item_id: str):
    response = Controle().fluxo(TipoEnum.gerarGift, int(item_id))
    return (response)


@router.get("/productPIN",
            tags=["Listar PIN..."],
            status_code=200)
def Listar_catálogo():
    lista = Controle().fluxo(TipoEnum.listaPIN)
    return (lista)


@router.post("/productPIN/{pin}/activate",
             tags=["Ativar PIN..."],
             status_code=200)
def Ativar_PIN(pin: str):
    lista = Controle().fluxo(TipoEnum.activate, pin)
    return (lista)
