# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 20:39:56 2026

@author: Vitoria
"""

import streamlit as st

from services.fichamentos import (
    listar_fichamentos,
    excluir_fichamento,
    atualizar_fichamento,
    TituloDuplicadoError 
)
from utils.auth import exigir_login
from utils.storage import (
    gerar_url_pdf,
    excluir_pdf,
    enviar_pdf
)


usuario = exigir_login()


# --------------------------------------------------
# CABEÇALHO
# --------------------------------------------------

st.markdown("#### Biblioteca")


# --------------------------------------------------
# BUSCAR FICHAMENTOS
# --------------------------------------------------

try:
    fichamentos = listar_fichamentos(usuario.id)

except Exception as e:
    st.error("Não foi possível carregar sua biblioteca.")
    st.exception(e)
    st.stop()


if not fichamentos:
    st.info("Você ainda não possui nenhum fichamento.")
    st.stop() 


# --------------------------------------------------
# BUSCA E FILTRO
# --------------------------------------------------

col_busca, col_tipo = st.columns([5, 1])

with col_busca:

    busca = st.text_input(
        "🔎 Buscar fichamento",
        placeholder="Digite autor, título ou anotação...",
    )


with col_tipo:

    filtro_tipo = st.selectbox(
        "Tipo",
        [
            "Todos",
            "Artigo",
            "TCC",
            "Dissertação",
            "Livro",
            "Outro",
        ],
    )


campo_busca = st.radio(
    "Pesquisar em:",
    [
        "Todos",
        "Título",
        "Autores",
        "Anotações",
    ],
    horizontal=True,
)


# --------------------------------------------------
# FILTRAR FICHAMENTOS
# --------------------------------------------------

fichamentos_filtrados = []

for fichamento in fichamentos:

    # ----------------------------------------------
    # FILTRO POR TIPO
    # ----------------------------------------------

    if filtro_tipo != "Todos":

        if fichamento.get("tipo") != filtro_tipo:
            continue


    # ----------------------------------------------
    # FILTRO POR TEXTO
    # ----------------------------------------------

    if busca.strip():

        termos = busca.lower().split()


        # Define onde pesquisar

        if campo_busca == "Título":

            texto = fichamento.get("titulo") or ""

        elif campo_busca == "Autores":

            texto = fichamento.get("autores") or ""

        elif campo_busca == "Anotações":

            texto = fichamento.get("anotacoes") or ""

        else:

            texto = " ".join([
                fichamento.get("titulo") or "",
                fichamento.get("autores") or "",
                fichamento.get("anotacoes") or "",
            ])


        texto = texto.lower()


        # Todos os termos precisam aparecer

        if not all(termo in texto for termo in termos):
            continue


    # ----------------------------------------------
    # FICHAMENTO APROVADO PELOS FILTROS
    # ----------------------------------------------

    fichamentos_filtrados.append(fichamento)  


# --------------------------------------------------
# RESULTADO DA BUSCA
# --------------------------------------------------

st.write(
    f"**{len(fichamentos_filtrados)} fichamento(s) encontrado(s)**"
)

st.divider()


# --------------------------------------------------
# DIALOGO DE EDICAO
# --------------------------------------------------

@st.dialog("Editar fichamento")
def editar_dialog(fichamento):

    titulo = st.text_input(
        "Título",
        value=fichamento["titulo"],
    )

    autores = st.text_input(
        "Autor(es)",
        value=fichamento["autores"],
    )

    tipos = [
        "Artigo",
        "TCC",
        "Dissertação",
        "Livro",
        "Outro",
    ]

    tipo_atual = fichamento.get("tipo")

    if tipo_atual in tipos:
        indice_tipo = tipos.index(tipo_atual)
    else:
        indice_tipo = 0

    tipo = st.selectbox(
        "Tipo de documento",
        tipos,
        index=indice_tipo,
    )

    anotacoes = st.text_area(
        "Anotações",
        value=fichamento.get("anotacoes") or "",
        height=200,
    )

    st.divider()

    st.write("**PDF atual**")

    st.code(
        fichamento["caminho"],
        language=None,
    )

    novo_pdf = st.file_uploader(
        "Substituir PDF (opcional)",
        type=["pdf"],
        key=f"novo_pdf_{fichamento['id']}",
    )

    st.divider()

    if st.button(
        "Salvar alterações",
        type="primary",
        use_container_width=True,
    ):

        if not titulo.strip():
            st.error("Informe o título.")
            return

        if not autores.strip():
            st.error("Informe o(s) autor(es).")
            return

        caminho_novo = None

        try:

            if novo_pdf is not None:

                caminho_novo = enviar_pdf(
                    usuario_id=usuario.id,
                    arquivo_bytes=novo_pdf.getvalue(),
                    nome_arquivo=novo_pdf.name,
                )

            atualizar_fichamento(
                usuario_id=usuario.id,
                fichamento_id=fichamento["id"],
                titulo=titulo.strip(),
                autores=autores.strip(),
                tipo=tipo,
                anotacoes=anotacoes.strip() or None,
                caminho=caminho_novo,
            )

            if caminho_novo is not None:

                excluir_pdf(
                    fichamento["caminho"]
                )

            st.success(
                "Fichamento atualizado com sucesso!"
            )

            st.rerun()

        except TituloDuplicadoError as e:

            if caminho_novo is not None:
                try:
                    excluir_pdf(caminho_novo)
                except Exception:
                    pass

            st.warning(str(e))

        except Exception as e:

            if caminho_novo is not None:
                try:
                    excluir_pdf(caminho_novo)
                except Exception:
                    pass

            st.error(
                "Não foi possível atualizar o fichamento."
            )

            st.exception(e)


# --------------------------------------------------
# LISTAGEM
# --------------------------------------------------

for fichamento in fichamentos_filtrados:

    st.markdown(f"#### {fichamento['titulo']}")

    st.write(
        f"**Autor(es):** {fichamento['autores']}"
    )

    if fichamento.get("tipo"):
        st.write(
            f"**Tipo:** {fichamento['tipo']}"
        )

    if fichamento.get("anotacoes"):
        st.write(
            f"**Anotações:** {fichamento['anotacoes']}"
        )

    col_pdf, col_editar, col_excluir = st.columns([1, 1, 1])

    with col_pdf:

        try:
            url_pdf = gerar_url_pdf(
                fichamento["caminho"]
            )

            st.link_button(
                "📄 Abrir PDF",
                url_pdf,
            )

        except Exception:
            st.error(
                "Não foi possível gerar o link do PDF."
            )

    with col_editar:

        if st.button(
            "✏️ Editar",
            key=f"editar_{fichamento['id']}",
        ):
            editar_dialog(fichamento)

    with col_excluir:

        with st.popover("🗑️ Excluir"):

            st.write(
                "Tem certeza que deseja excluir "
                "este fichamento?"
            )

            if st.button(
                "Sim, excluir",
                key=f"excluir_{fichamento['id']}",
                type="primary",
            ):

                try:

                    excluir_pdf(
                        fichamento["caminho"]
                    )

                    excluir_fichamento(
                        usuario_id=usuario.id,
                        fichamento_id=fichamento["id"],
                    )

                    st.success(
                        "Fichamento excluído."
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Não foi possível excluir "
                        "o fichamento."
                    )

                    st.exception(e)

    st.divider() 
