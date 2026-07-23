# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:18:48 2026

@author: Vitoria
"""

import streamlit as st
from utils.banco import (listar_fichamentos, editar_anotacoes, 
                         buscar_fichamento_por_id)
from utils.fichamento import remover_fichamento
from utils.pdf import link_pdf 
from utils.estilo import titulo


st.sidebar.image("assets\\logo.png", width=250) 
st.sidebar.markdown("---")

titulo("Fichamentos",
       "Consulte e edite seus fichamentos.") 


fichamentos = listar_fichamentos()

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
        if st.button("Salvar", use_container_width=True):

            editar_anotacoes(
                id_fichamento,
                novas_anotacoes
            )

            st.success("Anotações atualizadas!")

            st.rerun()

    with col2:
        if st.button("Cancelar", use_container_width=True):
            st.rerun()

for ficha in fichamentos:

    with st.expander(ficha["titulo"]):

        st.write("**Autor(es):**", ficha["autores"])
        st.write("**Tipo de documento:**", ficha["tipo"])

        st.write("**Anotações:**")
        st.text(ficha["anotacoes"])

        st.write("**Arquivo:**") 
        st.write(link_pdf(ficha["caminho"])) 

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

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "Sim, excluir",
                    key=f"confirmar_{ficha['id']}"
                ):

                    remover_fichamento(ficha["id"])

                    del st.session_state[
                        f"confirmar_exclusao_{ficha['id']}"
                    ]

                    st.success("Fichamento excluído!")

                    st.rerun()

            with col2:
                if st.button(
                    "Cancelar",
                    key=f"cancelar_{ficha['id']}"
                ):

                    del st.session_state[
                        f"confirmar_exclusao_{ficha['id']}"
                    ]

                    st.rerun()
                    
