# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 20:58:08 2026

@author: Vitoria
"""

from utils.supabase import supabase


class TituloDuplicadoError(Exception):
    pass


def criar_fichamento(
    usuario_id: str,
    titulo: str,
    autores: str,
    tipo: str | None,
    anotacoes: str | None,
    caminho: str | None,
):
    try:
        resposta = (
            supabase
            .table("fichamentos")
            .insert({
                "usuario_id": usuario_id,
                "titulo": titulo,
                "autores": autores,
                "tipo": tipo,
                "anotacoes": anotacoes,
                "caminho": caminho,
            })
            .execute()
        )

        return resposta.data

    except Exception as e:

        if "duplicate key" in str(e).lower():
            raise TituloDuplicadoError(
                "Você já possui um fichamento com esse título."
            ) from e

        raise


def listar_fichamentos(usuario_id: str):
    resposta = (
        supabase
        .table("fichamentos")
        .select("*")
        .eq("usuario_id", usuario_id)
        .order("criado_em", desc=True)
        .execute()
    )

    return resposta.data


def atualizar_fichamento(
    usuario_id: str,
    fichamento_id: int,
    titulo: str,
    autores: str,
    tipo: str | None,
    anotacoes: str | None,
    caminho: str | None = None,
):
    dados = {
        "titulo": titulo,
        "autores": autores,
        "tipo": tipo,
        "anotacoes": anotacoes,
    }

    if caminho is not None:
        dados["caminho"] = caminho

    try:
        resposta = (
            supabase
            .table("fichamentos")
            .update(dados)
            .eq("id", fichamento_id)
            .eq("usuario_id", usuario_id)
            .execute()
        )

        return resposta.data

    except Exception as e:

        if "duplicate key" in str(e).lower():
            raise TituloDuplicadoError(
                "Você já possui outro fichamento com esse título."
            ) from e

        raise


def remover_pdf(
    usuario_id: str,
    fichamento_id: int,
):
    resposta = (
        supabase
        .table("fichamentos")
        .update({"caminho": None})
        .eq("id", fichamento_id)
        .eq("usuario_id", usuario_id)
        .execute()
    )

    return resposta.data


def excluir_fichamento(
    usuario_id: str,
    fichamento_id: int,
):
    resposta = (
        supabase
        .table("fichamentos")
        .delete()
        .eq("id", fichamento_id)
        .eq("usuario_id", usuario_id)
        .execute()
    )

    return resposta.data


def listar_ultimos_fichamentos(
    usuario_id: str,
    limite: int = 3,
):
    resposta = (
        supabase
        .table("fichamentos")
        .select("*")
        .eq("usuario_id", usuario_id)
        .order("atualizado_em", desc=True)
        .limit(limite)
        .execute()
    )

    return resposta.data
