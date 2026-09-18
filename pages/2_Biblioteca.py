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
    remover_pdf,
    TituloDuplicadoError,
)

from utils.auth import exigir_login

from utils.storage import (
    gerar_url_pdf,
    excluir_pdf,
    enviar_pdf,
)


# ==================================================
# CONFIGURAÇÕES
# ==================================================

TIPOS_DOCUMENTO = [
    "Artigo",
    "TCC",
    "Dissertação",
    "Livro",
    "Outro",
]


# ==================================================
# AUTENTICAÇÃO
# ==================================================

usuario = exigir_login()


# ==================================================
# CABEÇALHO
# ==================================================

st.markdown("#### Biblioteca")


# ==================================================
# CARREGAR FICHAMENTOS
# ==================================================

try:
    fichamentos = listar_fichamentos(usuario.id)

except Exception as e:
    st.error("Não foi possível carregar sua biblioteca.")
    st.exception(e)
    st.stop()


# ==================================================
# BIBLIOTECA VAZIA
# ==================================================

if not fichamentos:
    st.info("Você ainda não possui nenhum fichamento.")
    st.stop()


# ==================================================
# BUSCA E FILTROS
# ==================================================

col_busca, col_tipo = st.columns([5, 1])

with col_busca:
    busca = st.text_input(
        "🔎 Buscar fichamento",
        placeholder="Digite autor, título ou anotação...",
    )

with col_tipo:
    filtro_tipo = st.selectbox(
        "Tipo",
        ["Todos"] + TIPOS_DOCUMENTO,
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


# ==================================================
# FILTRAR
# ==================================================

termos_busca = busca.strip().lower().split()

fichamentos_filtrados = []


for fichamento in fichamentos:

    # ----------------------------------------------
    # FILTRO POR TIPO
    # ----------------------------------------------

    if filtro_tipo != "Todos":
        if fichamento.get("tipo") != filtro_tipo:
            continue

    # ----------------------------------------------
    # BUSCA
    # ----------------------------------------------

    if termos_busca:

        titulo = fichamento.get("titulo") or ""
        autores = fichamento.get("autores") or ""
        anotacoes = fichamento.get("anotacoes") or ""

        if campo_busca == "Título":
            texto = titulo

        elif campo_busca == "Autores":
            texto = autores

        elif campo_busca == "Anotações":
            texto = anotacoes

        else:
            texto = " ".join(
                [
                    titulo,
                    autores,
                    anotacoes,
                ]
            )

        texto = texto.lower()

        if not all(
            termo in texto
            for termo in termos_busca
        ):
            continue

    fichamentos_filtrados.append(fichamento)


# ==================================================
# RESULTADO
# ==================================================

st.write(
    f"**{len(fichamentos_filtrados)} fichamento(s) encontrado(s)**"
)

st.divider()


# ==================================================
# DIÁLOGO DE EDIÇÃO
# ==================================================

@st.dialog("Editar fichamento")
def editar_dialog(fichamento):

    fichamento_id = fichamento["id"]

    titulo = st.text_input(
        "Título",
        value=fichamento.get("titulo") or "",
        key=f"titulo_edicao_{fichamento_id}",
    )

    autores = st.text_input(
        "Autor(es)",
        value=fichamento.get("autores") or "",
        key=f"autores_edicao_{fichamento_id}",
    )

    tipo_atual = fichamento.get("tipo")

    if tipo_atual in TIPOS_DOCUMENTO:
        indice_tipo = TIPOS_DOCUMENTO.index(tipo_atual)
    else:
        indice_tipo = 0

    tipo = st.selectbox(
        "Tipo de documento",
        TIPOS_DOCUMENTO,
        index=indice_tipo,
        key=f"tipo_edicao_{fichamento_id}",
    )

    anotacoes = st.text_area(
        "Anotações",
        value=fichamento.get("anotacoes") or "",
        height=200,
        key=f"anotacoes_edicao_{fichamento_id}",
    )

    st.divider()

    # ==================================================
    # PDF
    # ==================================================

    caminho_atual = fichamento.get("caminho")

    st.write("**PDF**")

    if caminho_atual:

        try:
            url_pdf = gerar_url_pdf(caminho_atual)

            st.link_button(
                "📄 Abrir PDF atual",
                url_pdf,
                use_container_width=False,
            )

        except Exception:
            st.warning(
                "Não foi possível gerar o link do PDF atual."
            )

        excluir_pdf_marcado = st.checkbox(
            "Excluir PDF atual",
            key=f"excluir_pdf_{fichamento_id}",
        )

    else:

        st.info("Nenhum PDF anexado.")

        excluir_pdf_marcado = False

    novo_pdf = st.file_uploader(
        "Substituir PDF",
        type=["pdf"],
        key=f"novo_pdf_{fichamento_id}",
        help="Selecione um arquivo somente se quiser substituir o PDF atual.",
    )

    if novo_pdf is not None:
        st.caption(
            "O novo PDF substituirá o PDF atual ao salvar."
        )

    # Se selecionou um novo PDF, a exclusão manual
    # deixa de fazer sentido.
    if novo_pdf is not None and excluir_pdf_marcado:
        st.info(
            "O novo PDF selecionado terá prioridade sobre a exclusão do PDF atual."
        )

    st.divider()

    # ==================================================
    # SALVAR
    # ==================================================

    if st.button(
        "Salvar alterações",
        type="primary",
        use_container_width=True,
        key=f"salvar_edicao_{fichamento_id}",
    ):

        # ----------------------------------------------
        # VALIDAÇÕES
        # ----------------------------------------------

        titulo = titulo.strip()
        autores = autores.strip()
        anotacoes = anotacoes.strip()

        if not titulo:
            st.error("Informe o título.")
            return

        if not autores:
            st.error("Informe o(s) autor(es).")
            return

        caminho_novo = None

        try:

            # ==================================================
            # 1. SUBSTITUIR PDF
            # ==================================================

            if novo_pdf is not None:

                caminho_novo = enviar_pdf(
                    usuario_id=usuario.id,
                    arquivo_bytes=novo_pdf.getvalue(),
                    nome_arquivo=novo_pdf.name,
                )

                try:

                    atualizar_fichamento(
                        usuario_id=usuario.id,
                        fichamento_id=fichamento_id,
                        titulo=titulo,
                        autores=autores,
                        tipo=tipo,
                        anotacoes=anotacoes or None,
                        caminho=caminho_novo,
                    )

                except Exception:

                    # O novo arquivo já foi enviado,
                    # mas o banco não foi atualizado.
                    # Remove o novo arquivo para
                    # evitar arquivo órfão.

                    try:
                        excluir_pdf(caminho_novo)
                    except Exception:
                        pass

                    caminho_novo = None

                    raise

                # O banco agora aponta para o novo PDF.
                # Só então removemos o antigo.

                if caminho_atual:
                    try:
                        excluir_pdf(caminho_atual)
                    except Exception as e:
                        st.warning(
                            "O fichamento foi atualizado, "
                            "mas não foi possível remover "
                            "o PDF anterior do Storage."
                        )
                        st.exception(e)

            # ==================================================
            # 2. REMOVER PDF
            # ==================================================

            elif excluir_pdf_marcado and caminho_atual:

                remover_pdf(
                    usuario_id=usuario.id,
                    fichamento_id=fichamento_id,
                )

                atualizar_fichamento(
                    usuario_id=usuario.id,
                    fichamento_id=fichamento_id,
                    titulo=titulo,
                    autores=autores,
                    tipo=tipo,
                    anotacoes=anotacoes or None,
                )

            # ==================================================
            # 3. MANTER PDF
            # ==================================================

            else:

                atualizar_fichamento(
                    usuario_id=usuario.id,
                    fichamento_id=fichamento_id,
                    titulo=titulo,
                    autores=autores,
                    tipo=tipo,
                    anotacoes=anotacoes or None,
                )

            st.success(
                "Fichamento atualizado com sucesso!"
            )

            st.rerun()

        except TituloDuplicadoError as e:

            st.warning(str(e))

        except Exception as e:

            st.error(
                "Não foi possível atualizar o fichamento."
            )

            st.exception(e)


# ==================================================
# LISTAGEM
# ==================================================

if not fichamentos_filtrados:

    st.info(
        "Nenhum fichamento corresponde aos filtros selecionados."
    )

else:

    for fichamento in fichamentos_filtrados:

        fichamento_id = fichamento["id"]

        titulo = fichamento.get("titulo") or "Sem título"
        autores = fichamento.get("autores") or "Não informado"
        tipo = fichamento.get("tipo")
        anotacoes = fichamento.get("anotacoes")
        caminho_pdf = fichamento.get("caminho")

        # ==================================================
        # INFORMAÇÕES
        # ==================================================

        st.markdown(f"#### {titulo}")

        st.write(
            f"**Autor(es):** {autores}"
        )

        if tipo:
            st.write(
                f"**Tipo:** {tipo}"
            )

        if anotacoes:
            st.write(
                f"**Anotações:** {anotacoes}"
            )

        # ==================================================
        # AÇÕES
        # ==================================================

        if caminho_pdf:
            col_pdf, col_editar, col_excluir = st.columns(3)
        else:
            col_editar, col_excluir = st.columns(2)

        # ==================================================
        # ABRIR PDF
        # ==================================================

        if caminho_pdf:

            with col_pdf:

                try:

                    url_pdf = gerar_url_pdf(
                        caminho_pdf
                    )

                    st.link_button(
                        "📄 Abrir PDF",
                        url_pdf,
                        use_container_width=True,
                    )

                except Exception:

                    st.error(
                        "Não foi possível gerar o link do PDF."
                    )

        # ==================================================
        # EDITAR
        # ==================================================

        with col_editar:

            if st.button(
                "✏️ Editar",
                key=f"editar_{fichamento_id}",
                use_container_width=True,
            ):

                editar_dialog(fichamento)

        # ==================================================
        # EXCLUIR FICHAMENTO
        # ==================================================

        with col_excluir:

            with st.popover(
                "🗑️ Excluir",
                use_container_width=True,
            ):

                st.write(
                    "Tem certeza que deseja excluir este fichamento?"
                )

                if caminho_pdf:
                    st.caption(
                        "O PDF associado também será removido."
                    )

                if st.button(
                    "Sim, excluir",
                    key=f"excluir_{fichamento_id}",
                    type="primary",
                    use_container_width=True,
                ):

                    try:

                        # ----------------------------------
                        # REMOVE PDF PRIMEIRO
                        # ----------------------------------

                        if caminho_pdf:

                            excluir_pdf(
                                caminho_pdf
                            )

                        # ----------------------------------
                        # REMOVE FICHAMENTO
                        # ----------------------------------

                        excluir_fichamento(
                            usuario_id=usuario.id,
                            fichamento_id=fichamento_id,
                        )

                        st.success(
                            "Fichamento excluído."
                        )

                        st.rerun()

                    except Exception as e:

                        st.error(
                            "Não foi possível excluir o fichamento."
                        )

                        st.exception(e)

        st.divider() 
