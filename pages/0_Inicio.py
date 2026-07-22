# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 19:27:04 2026

@author: Vitoria
"""
import streamlit as st
from utils.estilo import titulo

st.sidebar.image("assets\\logo.png", width=250) 
st.sidebar.markdown("---")

titulo("Bem vinda!",
       """
       Organize suas leituras, registre fichamentos e acompanhe o 
       desenvolvimento da sua pesquisa. """) 

st.markdown("---") 
st.markdown("> *Todas as vitórias ocultam uma abdicação.*  \n— Simone de Beauvoir") 
 