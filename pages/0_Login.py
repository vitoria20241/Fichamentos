# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 21:11:29 2026

@author: Vitoria
"""

import streamlit as st
from pathlib import Path
import base64

from utils.auth import login
from config import MANDALA1


# ==================================================
# TELA DE LOGIN
# ==================================================

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# FORMULÁRIO
# ==================================================

col1, col2, col3 = st.columns(3)

with col2:

    with st.form("login_form"):

        email = st.text_input("E-mail")

        senha = st.text_input(
            "Senha",
            type="password",
        )

        col1, col2, col3 = st.columns([1, 0.7, 1])

        with col2:
            entrar = st.form_submit_button(
                "Entrar",
                type="primary",
                use_container_width=True,
            )


# ==================================================
# MANDALA
# ==================================================

@st.cache_data
def carregar_mandala(caminho):
    with open(caminho, "rb") as f:
        return base64.b64encode(f.read()).decode()


mandala = Path(MANDALA1)

if mandala.exists():

    img = carregar_mandala(str(mandala))

    st.markdown(
        f"""
        <img src="data:image/png;base64,{img}"
        style="
            position: fixed;
            bottom: -110px;
            left: 50%;
            transform: translateX(-50%);
            width: min(2000px, 100vw);
            opacity: 0.17;
            z-index: 0;
            pointer-events: none;
        ">
        """,
        unsafe_allow_html=True,
    ) 


# ==================================================
# AUTENTICAÇÃO
# ==================================================

if entrar:
    col1, col2, col3 = st.columns(3) 
    with col2:

        if not email or not senha:
    
            st.error("Informe o e-mail e a senha.")
    
        else:
    
            try:
                resposta = login(email, senha)
    
                if resposta.session:
                    st.rerun()
    
                else:
                    st.error(
                        "Não foi possível iniciar a sessão."
                    )
    
            except Exception:
                st.error("E-mail ou senha incorretos.") 