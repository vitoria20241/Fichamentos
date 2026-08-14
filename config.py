# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 17:10:25 2026

@author: Vitoria
"""

import os

# pasta raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# pastas
DADOS_DIR = os.path.join(BASE_DIR, "dados")
IMAGENS_DIR = os.path.join(BASE_DIR, "assets")
PDFS_DIR = os.path.join(BASE_DIR, "pdfs")

# arquivos
BANCO = os.path.join(
    DADOS_DIR,
    "fichamentos.db"
)

LOGO = os.path.join(
    IMAGENS_DIR,
    "logo.png"
)

MANDALA = os.path.join(
    IMAGENS_DIR,
    "mandala.png"
) 

ICONE = os.path.join(
    IMAGENS_DIR,
    "icone.ico"
) 