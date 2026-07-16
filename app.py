# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:47:16 2026

@author: Vitoria
"""

import streamlit as st 
from utils.banco import criar_tabelas

criar_tabelas() 

st.set_page_config(page_icon="\U0001F50E", 
                   layout="wide") 

pg = st.navigation([
    st.Page("pages/0_Inicio.py", title="Início"),
    st.Page("pages/1_Biblioteca.py", title="Biblioteca"),
    st.Page("pages/2_Cadastro.py", title="Cadastro"),
])

pg.run()

