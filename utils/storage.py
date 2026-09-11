# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 19:42:55 2026

@author: Vitoria
"""

import uuid
from pathlib import Path

from utils.supabase import supabase


BUCKET = "fichamentos"


def validar_pdf(nome_arquivo: str) -> None:
    extensao = Path(nome_arquivo).suffix.lower()

    if extensao != ".pdf":
        raise ValueError("Apenas arquivos PDF são permitidos.")


def gerar_caminho(
    usuario_id: str,
    nome_arquivo: str,
) -> str:

    validar_pdf(nome_arquivo)

    nome_unico = f"{uuid.uuid4()}.pdf"

    return f"{usuario_id}/{nome_unico}"


def enviar_pdf(
    usuario_id: str,
    arquivo_bytes: bytes,
    nome_arquivo: str,
) -> str:

    caminho = gerar_caminho(
        usuario_id,
        nome_arquivo,
    )

    supabase.storage.from_(BUCKET).upload(
        caminho,
        arquivo_bytes,
        {
            "content-type": "application/pdf",
        },
    )

    return caminho


def gerar_url_pdf(
    caminho: str,
    validade: int = 3600,
) -> str:

    resposta = (
        supabase
        .storage
        .from_(BUCKET)
        .create_signed_url(
            caminho,
            validade,
        )
    )

    return resposta["signedURL"]


def excluir_pdf(caminho: str):

    return (
        supabase
        .storage
        .from_(BUCKET)
        .remove([caminho])
    )
