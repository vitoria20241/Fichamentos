# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:18:48 2026

@author: Vitoria
"""

import streamlit as st
from utils.banco import (listar_fichamentos, editar_anotacoes, 
                         buscar_fichamento_por_id, listar_tipos)
from utils.fichamento import remover_fichamento


col1, col2 = st.columns([3, 1]) 
with col1:
    pesquisa = st.text_input(
        "Pesquisar",
        placeholder="Título, autor ou anotação..."
    )
with col2:
    tipos = ["Todos"] + listar_tipos()
    tipo = st.selectbox(
        "Tipo", 
        tipos
    ) 
    

# Busca
fichamentos = listar_fichamentos(
    texto=pesquisa,
    tipo=tipo
)

st.markdown("---") 
st.write(f"📚 {len(fichamentos)} fichamento(s) encontrado(s)") 

@st.dialog("Editar anotações")
def dialog_editar(id_fichamento):

    ficha = buscar_fichamento_por_id(id_fichamento)

    novas_anotacoes = st.text_area(
        "Anotações",
        value=ficha["anotacoes"],
        height=300
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
                "Cancelar", 
                type = "secondary", 
                use_container_width=True):
            st.rerun()
            
    with col2:
        if st.button(
                "Salvar", 
                type = "primary", 
                use_container_width=True
                ):

            editar_anotacoes(
                id_fichamento,
                novas_anotacoes
            )

            st.success("Anotações atualizadas!")

            st.rerun()
            

for ficha in fichamentos:

    with st.expander(ficha["titulo"]):

        st.write("**Autor(es):**", ficha["autores"])
        st.write("**Tipo de documento:**", ficha["tipo"])
        
        st.write("**Anotações:**")
        st.markdown(ficha["anotacoes"])

        st.write("**Arquivo:**") 
        st.write(ficha["caminho"])  

        col1, col2, col3 = st.columns(3)

        # Botão editar
        with col1:
            if st.button(
                "Editar anotações",
                key=f"editar_{ficha['id']}"
            ):
                dialog_editar(ficha["id"])
       

        # Botão excluir
        with col2:
            if st.button(
                "Excluir fichamento",
                key=f"excluir_{ficha['id']}"
            ):
                st.session_state[
                    f"confirmar_exclusao_{ficha['id']}"
                ] = True

        # Confirmação da exclusão
        if st.session_state.get(
            f"confirmar_exclusao_{ficha['id']}",
            False
        ):

            st.warning(
                f"Tem certeza que deseja excluir '{ficha['titulo']}'?"
            )

            col1, col2, col3, col4 = st.columns(4) 

            with col2:
                if st.button(
                    "Cancelar",
                    type='secondary',
                    key=f"cancelar_{ficha['id']}"
                ):

                    del st.session_state[
                        f"confirmar_exclusao_{ficha['id']}"
                    ]

                    st.rerun()
                    
            with col3:
                if st.button(
                    "Sim, excluir",
                    type='primary',
                    key=f"confirmar_{ficha['id']}"
                ):

                    remover_fichamento(ficha["id"])

                    del st.session_state[
                        f"confirmar_exclusao_{ficha['id']}"
                    ]

                    st.success("Fichamento excluído!")

                    st.rerun() 