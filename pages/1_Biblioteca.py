# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 16:18:48 2026

@author: Vitoria
"""

import streamlit as st
from utils.banco import listar_fichamentos
from utils.fichamento import remover_fichamento
from utils.estilo import titulo


st.sidebar.image("assets\\logo.png", width=250) 
st.sidebar.markdown("---")

titulo("Fichamentos",
       "Consulte e edite seus fichamentos.") 


fichamentos = listar_fichamentos()


for ficha in fichamentos:

    with st.expander(ficha["titulo"]):

        st.write("**Autores:**", ficha["autores"])
        st.write("**Tipo de documento:**", ficha["tipo"])

        st.write("**Anotações:**")
        st.text(ficha["anotacoes"]) 

        st.write("**PDF:**", ficha["caminho"])


        # Botão inicial de excluir
        if st.button(
            "Excluir",
            key=f"excluir_{ficha['id']}"
        ):
            st.session_state[f"confirmar_exclusao_{ficha['id']}"] = True


        # Área de confirmação
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


