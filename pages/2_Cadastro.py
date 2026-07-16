# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 15:49:06 2026

@author: Vitoria
"""

import streamlit as st 
from utils.fichamento import criar_fichamento
from utils.estilo import titulo


st.sidebar.image("assets\\logo.png", width=250) 
st.sidebar.markdown("---")

titulo("Novo Fichamento", 
       "Cadastre um arquivo e registre suas anotações para consulta futura.") 


titulo = st.text_input("Título")

autores = st.text_input("Autor(es)")

tipo = st.selectbox(
    "Tipo de documento",
    [
        "Artigo",
        "TCC",
        "Dissertação",
        "Livro",
        "Outro"
    ]
) 

anotacoes = st.text_area(
    "Anotações",
    height=200
)

arquivo_pdf = st.file_uploader(
    "Selecione o PDF",
    type=["pdf"]
)


if st.button("Salvar"):
    try:
        criar_fichamento(
            titulo,
            autores,
            tipo,
            anotacoes,
            arquivo_pdf
        )

        st.success("Fichamento salvo!")

    except ValueError as e:
        st.error(str(e)) 