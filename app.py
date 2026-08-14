# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:47:16 2026

@author: Vitoria
"""

import streamlit as st 
from utils.banco import criar_tabelas
from config import (LOGO, ICONE)


criar_tabelas() 

st.set_page_config(
    page_title="Fichamentos", 
    page_icon=ICONE,  
    layout="wide"
    ) 

st.sidebar.image(LOGO, width=200) 

pg = st.navigation([
    st.Page("pages/0_Inicio.py", title="⌂ Início"),
    st.Page("pages/1_Biblioteca.py", title="◫ Biblioteca"),
    st.Page("pages/2_Cadastro.py", title="✎ Cadastro"),
])

pg.run()

