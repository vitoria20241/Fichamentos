# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 19:27:04 2026

@author: Vitoria
"""
import streamlit as st
from utils.estilo import titulo
from utils.banco import buscar_fichamentos_recentes 
from pathlib import Path
import base64
from config import MANDALA

st.sidebar.markdown("---")
st.sidebar.write("""
                 🎓 24/11/2026 - Entrega do TCC  
                 🎓 31/03/2027 - Colação, 15h 
                 """) 

titulo("Biblioteca de pesquisa",
       "Leituras, referências e fichamentos do TCC.") 

st.divider() 

st.markdown("#### Últimas leituras") 

fichamentos = buscar_fichamentos_recentes(3)

if not fichamentos:
    st.caption("Seus fichamentos aparecerão aqui.")
else:
    col1, col2 = st.columns([5, 1])
    with col1:
        for titulo_leitura, autores, tipo, anotacoes, caminho in fichamentos:
            with st.expander(titulo_leitura):
                st.write("**Autor(es):**", autores)
                st.write("**Tipo de documento:**", tipo)
                
                st.write("**Anotações:**")
                st.markdown(anotacoes)
        
                st.write("**Arquivo:**") 
                st.write(caminho)  


st.markdown("> *Todas as vitórias ocultam uma abdicação.*  \n— Simone de Beauvoir") 


@st.cache_data
def carregar_mandala(caminho):
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode()

mandala = Path(MANDALA)

if mandala.exists():
    img = carregar_mandala(str(mandala))

    st.markdown(
        f"""
        <img src="data:image/png;base64,{img}"
        style="
            position: fixed;
            bottom: -95px;
            right: -20px;
            width: 350px;
            opacity: 0.16;
            z-index: 0;
            pointer-events: none;
        ">
        """,
        unsafe_allow_html=True
    ) 