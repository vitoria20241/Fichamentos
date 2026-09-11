import streamlit as st

from utils.supabase import supabase


def login(email, senha):
    resposta = supabase.auth.sign_in_with_password({
        "email": email,
        "password": senha,
    })

    if resposta.session:
        st.session_state["usuario"] = resposta.user
        st.session_state["access_token"] = resposta.session.access_token
        st.session_state["refresh_token"] = resposta.session.refresh_token

    return resposta


def restaurar_sessao():
    access_token = st.session_state.get("access_token")
    refresh_token = st.session_state.get("refresh_token")

    if not access_token or not refresh_token:
        return False

    try:
        resposta = supabase.auth.set_session(
            access_token,
            refresh_token,
        )

        if not resposta.session or not resposta.user:
            raise Exception("Sessão inválida.")

        st.session_state["usuario"] = resposta.user
        st.session_state["access_token"] = resposta.session.access_token
        st.session_state["refresh_token"] = resposta.session.refresh_token

        return True

    except Exception:
        st.session_state["usuario"] = None
        st.session_state["access_token"] = None
        st.session_state["refresh_token"] = None

        return False


def logout():
    try:
        supabase.auth.sign_out()
    finally:
        st.session_state["usuario"] = None
        st.session_state["access_token"] = None
        st.session_state["refresh_token"] = None


def exigir_login():

    if st.session_state.get("usuario") is None:

        restaurar_sessao()

    if st.session_state.get("usuario") is None:

        col1, col2, col3 = st.columns(3)

        with col2:

            st.warning(
                "Você precisa estar logado para acessar esta página."
            )

            st.stop()

    return st.session_state["usuario"]
