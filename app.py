import streamlit as st

from utils.auth import (
    logout,
    restaurar_sessao,
)
from config import ICONE, LOGO


st.set_page_config(
    page_title="Fichamentos",
    page_icon=ICONE,
    layout="wide",
)


# ==================================================
# SESSION STATE
# ==================================================

if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "refresh_token" not in st.session_state:
    st.session_state["refresh_token"] = None


# ==================================================
# RESTAURA SESSÃO
# ==================================================

if (
    st.session_state["usuario"] is not None
    and st.session_state["access_token"]
    and st.session_state["refresh_token"]
):
    restaurar_sessao()


# ==================================================
# NAVEGAÇÃO
# ==================================================

if st.session_state["usuario"] is None:

    # ----------------------------------------------
    # USUÁRIO NÃO AUTENTICADO
    # ----------------------------------------------

    paginas = {
        "": [
            st.Page(
                "pages/0_Login.py",
                title="Login",
            ),
        ]
    }

else:

    # ----------------------------------------------
    # USUÁRIO AUTENTICADO
    # ----------------------------------------------

    with st.sidebar:
        st.image(LOGO, width=200)
        st.divider()

        col1, col2, col3 = st.columns(3)

        with col2:
            if st.button(
                "Sair",
                use_container_width=True,
            ):
                logout()
                st.rerun()

    paginas = {
        "": [
            st.Page(
                "pages/1_Inicio.py",
                title="Início",
                icon="🏠",
            ),
            st.Page(
                "pages/2_Biblioteca.py",
                title="Biblioteca",
                icon="📚",
            ),
            st.Page(
                "pages/3_Cadastro.py",
                title="Cadastro",
                icon="📝",
            ),
        ]
    }


pg = st.navigation(paginas)

pg.run() 