# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 19:27:04 2026

@author: Vitoria
"""
import streamlit as st
from utils.estilo import titulo
from pathlib import Path

st.sidebar.image("assets\\logo.png", width=200) 
st.sidebar.markdown("---")
st.sidebar.write("🎓 Colação 31/03/2027 às 15h") 

titulo("Bem vinda!",
       """
       Organize suas leituras, registre fichamentos e acompanhe o 
       desenvolvimento da sua pesquisa. """) 

st.markdown("---") 
st.markdown("> *Todas as vitórias ocultam uma abdicação.*  \n— Simone de Beauvoir") 

mandala = Path("assets/mandala.png")
if mandala.exists():
    st.markdown(
        f"""
        <img src="data:image/png;base64,{__import__('base64').b64encode(open(mandala, 'rb').read()).decode()}"
        style="
            position: fixed;
            bottom: 20px;
            right: 30px;
            width: 350px;
            opacity: 0.30;
            z-index: 0;
        ">
        """,
        unsafe_allow_html=True
    ) 