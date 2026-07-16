# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 15:38:13 2026

@author: Vitoria
"""

from .pdf import salvar_pdf, excluir_pdf 
from .banco import (salvar_fichamento, titulo_existe, 
                    buscar_fichamento_por_id, excluir_fichamento) 


def criar_fichamento(
    titulo,
    autores,
    tipo,
    anotacoes,
    arquivo_pdf
):
    
    if titulo_existe(titulo):
        raise ValueError("Já existe um fichamento com esse título.")

    caminho = salvar_pdf(arquivo_pdf)

    salvar_fichamento(
        titulo,
        autores,
        tipo,
        anotacoes,
        caminho
    ) 


def remover_fichamento(id_fichamento):
    ficha = buscar_fichamento_por_id(id_fichamento)
    if ficha is None:
        raise ValueError("Fichamento não encontrado.")

    caminho = ficha["caminho"]
    excluir_fichamento(id_fichamento)
    excluir_pdf(caminho) 

