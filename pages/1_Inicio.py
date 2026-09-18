# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 20:39:01 2026

@author: Vitoria
"""

import streamlit as st
from pathlib import Path
import base64

from utils.auth import exigir_login
from utils.storage import gerar_url_pdf
from config import MANDALA2
from services.fichamentos import listar_ultimos_fichamentos


# ==================================================
# AUTENTICAÇÃO
# ==================================================

usuario = exigir_login()


# ==================================================
# CABEÇALHO
# ==================================================

st.markdown("#### ⌕ Biblioteca de pesquisa")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        "*Leituras, referências e fichamentos do TCC.*"
    )

    st.markdown(
        "Formatação de referências: "
        "[FastFormat](https://app.fastformat.co/references/)"
    )


with col2:

    st.markdown(
        """
        **Datas importantes:**  
        🎓 24/11/2026 - Entrega do TCC  
        🎓 02/12/2026 - Defesa, 09h às 10h30min  
        🎓 ~~31/03/2027 - Colação, 15h~~  
        """
    )


st.divider()


# ==================================================
# ÚLTIMAS LEITURAS
# ==================================================

st.markdown("#### ◴ Últimas leituras")

ultimos_fichamentos = listar_ultimos_fichamentos(
    usuario_id=usuario.id,
    limite=3,
)


colunas = st.columns(3)


for coluna, fichamento in zip(
    colunas,
    ultimos_fichamentos,
):

    with coluna:

        st.markdown(
            f"**{fichamento['titulo']}**"
        )

        st.write(
            f"**Autor(es):** {fichamento['autores']}"
        )

        if fichamento.get("tipo"):

            st.write(
                f"**Tipo:** {fichamento['tipo']}"
            )


        # ------------------------------------------
        # PDF
        # ------------------------------------------

        caminho_pdf = fichamento.get("caminho")

        if caminho_pdf:

            try:

                url_pdf = gerar_url_pdf(
                    caminho_pdf
                )

                st.link_button(
                    "📄 Abrir PDF",
                    url_pdf,
                    use_container_width=False,
                )

            except Exception:

                st.error(
                    "Não foi possível gerar o link do PDF."
                )


# ==================================================
# MANDALA
# ==================================================

@st.cache_data
def carregar_mandala(caminho):

    with open(caminho, "rb") as f:

        return base64.b64encode(
            f.read()
        ).decode()


mandala = Path(MANDALA2)


if mandala.exists():

    img = carregar_mandala(
        str(mandala)
    )

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
        unsafe_allow_html=True,
    ) 
