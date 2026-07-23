# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:07:30 2026

@author: Vitoria
"""

import os

PASTA_PDFS = "pdfs"

def salvar_pdf(upload):
    caminho = os.path.join(PASTA_PDFS, upload.name)

    with open(caminho, "wb") as f:
        f.write(upload.getbuffer())

    return caminho 


def excluir_pdf(caminho): 
    if caminho and os.path.exists(caminho):
        os.remove(caminho) 
        

def link_pdf(caminho_pdf):
    pasta = "C:/Users/Vitoria/Documents/GitHub/Fichamentos/"
    caminho_pdf = caminho_pdf.replace("\\", "/") 
    return pasta + caminho_pdf 
