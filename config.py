# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 20:02:12 2026

@author: Vitoria
"""

import os

# pasta raiz do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# pastas
IMAGENS_DIR = os.path.join(BASE_DIR, "assets")

# arquivos
LOGO = os.path.join(
    IMAGENS_DIR,
    "logo.png"
)

MANDALA1 = os.path.join(
    IMAGENS_DIR,
    "mandala1.png" 
) 

MANDALA2 = os.path.join(
    IMAGENS_DIR,
    "mandala2.png" 
) 

ICONE = os.path.join(
    IMAGENS_DIR,
    "icone.ico"
) 