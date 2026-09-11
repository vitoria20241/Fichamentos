# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 20:40:22 2026

@author: Vitoria
"""

import streamlit as st

from services.fichamentos import (
    criar_fichamento,
    TituloDuplicadoError,
)

from utils.auth import exigir_login
from utils.storage import (
    enviar_pdf,
    excluir_pdf,
) 


usuario = exigir_login() 


# --------------------------------------------------
# CABEÇALHO
# --------------------------------------------------

st.markdown("### Novo Fichamento")


st.write(
    """
    Cadastre um arquivo e registre suas anotações 
    para consulta futura.
    """
)


st.divider()


# --------------------------------------------------
# FORMULÁRIO
# --------------------------------------------------

col_formulario, col_vazia = st.columns([4, 1])

with col_formulario:

    titulo = st.text_input("Título")

    autores = st.text_input("Autor(es)")

    tipo = st.selectbox(
        "Tipo de documento",
        [
            "Artigo",
            "TCC",
            "Dissertação",
            "Livro",
            "Outro",
        ],
    )

    anotacoes = st.text_area(
        "Anotações",
        height=200,
    )

    arquivo_pdf = st.file_uploader(
        "Selecione o PDF",
        type=["pdf"],
    )

    # --------------------------------------------------
    # SALVAR
    # --------------------------------------------------

    if st.button(
        "Salvar",
        type="primary",
        use_container_width=False,
    ):

        if not titulo.strip():

            st.error("Informe o título.")

        elif not autores.strip():

            st.error("Informe o(s) autor(es).")

        elif arquivo_pdf is None:

            st.error("Selecione um arquivo PDF.")

        else:

            caminho = None

            try:

                # ------------------------------------------
                # Envia PDF
                # ------------------------------------------

                caminho = enviar_pdf(
                    usuario_id=usuario.id,
                    arquivo_bytes=arquivo_pdf.getvalue(),
                    nome_arquivo=arquivo_pdf.name,
                )

                # ------------------------------------------
                # Salva fichamento
                # ------------------------------------------

                criar_fichamento(
                    usuario_id=usuario.id,
                    titulo=titulo.strip(),
                    autores=autores.strip(),
                    tipo=tipo,
                    anotacoes=anotacoes.strip() or None,
                    caminho=caminho,
                )

                # ------------------------------------------
                # Confirmação
                # ------------------------------------------

                st.success(
                    "Fichamento salvo com sucesso!"
                )

            except TituloDuplicadoError as e:

                if caminho is not None:

                    try:
                        excluir_pdf(caminho)
                    except Exception:
                        pass

                st.warning(str(e))

            except Exception as e:

                if caminho is not None:

                    try:
                        excluir_pdf(caminho)
                    except Exception:
                        pass

                st.error(
                    "Não foi possível salvar o fichamento."
                )

                st.exception(e) 