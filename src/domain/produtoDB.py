#from pydantic import BaseModel
from dataclasses import dataclass
from pydantic import Field
from typing import List
from enum import Enum
import sqlite3
from datetime import datetime
import uuid
from requests.models import Response
import json
from fastapi import status


class ProdutoDB():
    response=Response()

    def criarTabela(self):
        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE if not exists produto (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor TEXT NOT NULL);
        """)

        cursor.execute("""
        CREATE TABLE if not exists produtoGift (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor TEXT NOT NULL,
                pin TEXT NOT NULL,
                status TEXT NOT NULL);
        """)
        conn.close()

    def geraProdutoGift(self, itens):

        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()
        valor = str(uuid.uuid4())

        cursor.execute("""
        SELECT * FROM produto
        WHERE id=?;
        """, (itens.get('item_id'),))
        list = cursor.fetchall()

        if list:
            data = list[0]
            result = cursor.execute(f"""
            INSERT INTO produtoGift (nome,valor,pin,status)
            VALUES ("{data[1]}","{data[2]}","{valor}","ATIVO")
            """)

            mensagem = {
                'idTransacao': result.lastrowid,
                'dataOperacao': str(datetime.now()),
                'statusOperacao': 'PIN gerado com Sucesso !!!',
                'valor': data[2],
                'PIN': valor
            }
            self.response.status_code = status.HTTP_200_OK
        else:
            mensagem = {'MensagemErro': 'Codigo do produto inexistente!!!'}
            self.response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        conn.commit()
        conn.close()

        self.response._content = bytes(json.dumps(mensagem), 'utf-8')
        return self.response

    def salvarProduto(self, itens):

        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()
        p = itens.get('obj')

        cursor.execute("""
        SELECT * FROM produto
        WHERE valor=?;
        """, (p.valor,))
        teste = cursor.fetchall()

        if not teste:
            result = cursor.execute(f"""
            INSERT INTO produto (nome,valor)
            VALUES ("{p.nome}","{p.valor}")
            """)

            mensagem = {
                'codigoProduto': result.lastrowid,
                'dataOperacao': str(datetime.now()),
                'statusOperacao': 'Cadastrado com Sucesso !!!'
            }   
            self.response.status_code = status.HTTP_200_OK

        else:
            mensagem = {
                'dataOperacao': str(datetime.now()),
                'statusOperacao': 'Produto com esse valor ja cadastrado !!!'
            }
            self.response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        conn.commit()
        conn.close()
        
        self.response._content = bytes(json.dumps(mensagem), 'utf-8')
        return self.response

    def deletar(self, itens):

        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()

        request = cursor.execute("""
        DELETE FROM produto WHERE id = ?
        """, (itens.get('item_id'),))

        if request.rowcount:
            mensagem = {
                'dataOperacao': str(datetime.now()),
                'statusOperacao': 'Excluido com Sucesso !!!'
            }
            self.response.status_code = status.HTTP_200_OK
        else:
            mensagem = {
                'dataOperacao': str(datetime.now()),
                'statusOperacao': 'Produto Não encontrado !!!'
            }
            self.response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        conn.commit()
        conn.close()

        self.response._content = bytes(json.dumps(mensagem), 'utf-8')
        return self.response

    def atualizar(self, itens):

        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()

        data = itens.get('obj')

        cursor.execute("""
        SELECT * FROM produto
        WHERE valor=?;
        """, (data.valor,))
        teste = cursor.fetchall()

        if True:
            request = cursor.execute("""
                    UPDATE produto
                    SET nome = ?,
                    valor = ?
                    WHERE id = ?
                    """, (data.nome, data.valor, itens.get('item_id'),))

            if request.rowcount:
                mensagem = {
                    'dataOperacao': str(datetime.now()),
                    'statusOperacao': 'Atualizado com Sucesso !!!'
                }
                self.response.status_code = status.HTTP_200_OK
            else:
                mensagem = {
                    'dataOperacao': str(datetime.now()),
                    'statusOperacao': 'Produto Não encontrado !!!'
                }
                self.response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        else:
            mensagem = {
                'dataOperacao': str(datetime.now()),
                'statusOperacao': 'Produto com esse valor ja cadastrado !!!'
            }
            self.response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        conn.commit()
        conn.close()

        self.response._content = bytes(json.dumps(mensagem), 'utf-8')
        return self.response

    def pegarProduto(self, itens):
        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM produto;
        """)

        produtos = []
        for linha in cursor.fetchall():
            produtos.append({'id':linha[0], 'nome':linha[1], 'valor':linha[2]})
            id = linha[0]
        conn.close()

        self.response.status_code = status.HTTP_200_OK
        self.response._content = bytes(json.dumps(produtos), 'utf-8')
        return self.response


    def listaProdutoPIN(self, itens):
        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM produtoGift;
        """)

        produtos = []
        for linha in cursor.fetchall():
            produtos.append({'nome': linha[1],
                            'valor': linha[2],
                             'PIN': linha[3],
                             'status': linha[4]
                             })
        conn.close()
        self.response.status_code = status.HTTP_200_OK
        self.response._content = bytes(json.dumps(produtos), 'utf-8')
        return self.response
        

    def ativarProdutoGift(self, itens):

        conn = sqlite3.connect('produtos.db')
        cursor = conn.cursor()
        pin = itens.get('item_id')

        cursor.execute("""
        SELECT * FROM produtoGift
        WHERE pin=?;
        """, (pin,))
        list = cursor.fetchall()

        if 'RESGATADO' in list[0]:
            mensagem = {
                'dataOperacao': str(datetime.now()),
                'statusOperacao': 'PIN Já resgatado anteriormente !!!'
            }
            self.response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        elif list:
            cursor.execute("""
            UPDATE produtoGift
            SET status = ?
            WHERE pin = ?
            """, ('RESGATADO', pin,))

            mensagem = {
                'dataOperacao': str(datetime.now()),
                'statusOperacao': 'PIN resgatado com Sucesso !!!'
            }
            self.response.status_code = status.HTTP_200_OK
        else:
            mensagem = {
                'dataOperacao': str(datetime.now()),
                'statusOperacao': 'PIN nao encontrado !!!'
            }
            self.response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

        conn.commit()
        conn.close()

        self.response._content = bytes(json.dumps(mensagem), 'utf-8')
        return self.response


@dataclass
class Produto():

    nome: str
    valor: str
    cnpj: int= Field(None)
    id: int= Field(None)
