# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 14:52:46 2026

@author: Vitoria
"""

import sqlite3
from config import BANCO


def conectar():
    return sqlite3.connect(BANCO) 

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fichamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT UNIQUE NOT NULL,
            autores TEXT NOT NULL,
            tipo TEXT,
            anotacoes TEXT,
            caminho TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close() 

  
def salvar_fichamento(titulo, autores, tipo, anotacoes, caminho):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO fichamentos 
        (titulo, autores, tipo, anotacoes, caminho)
        VALUES (?, ?, ?, ?, ?)
    """, (titulo, autores, tipo, anotacoes, caminho))

    conn.commit()
    conn.close()
    

def titulo_existe(titulo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM fichamentos WHERE titulo = ? LIMIT 1",
        (titulo,)
    )

    existe = cursor.fetchone() is not None

    conn.close()

    return existe 


def listar_fichamentos(texto="", tipo="Todos"):
    conn = conectar()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    sql = """
         SELECT id, titulo, autores, tipo, anotacoes, caminho
         FROM fichamentos
         WHERE 1=1
     """

    parametros = []

    if texto:
        sql += """
            AND (
                titulo LIKE ?
                OR autores LIKE ?
                OR anotacoes LIKE ?
            )
        """
        pesquisa = f"%{texto}%"
        parametros.extend([pesquisa, pesquisa, pesquisa])

    if tipo != "Todos":
        sql += " AND tipo = ?"
        parametros.append(tipo)

    sql += " ORDER BY titulo"

    cursor.execute(sql, parametros)
    resultados = cursor.fetchall()
    conn.close()
    return [dict(ficha) for ficha in resultados] 


def buscar_fichamento_por_id(id_fichamento):
    conn = conectar()
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM fichamentos
        WHERE id = ?
        """,
        (id_fichamento,)
    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:
        return dict(resultado)

    return None 


def excluir_fichamento(id_fichamento):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM fichamentos
        WHERE id = ?
        """,
        (id_fichamento,)
    )

    conn.commit()
    conn.close() 


def editar_anotacoes(id_fichamento, anotacoes):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE fichamentos
        SET anotacoes = ?
        WHERE id = ?
    """, (anotacoes, id_fichamento))

    conn.commit()
    conn.close() 
    

def listar_tipos():
    conn = conectar() 
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT tipo
        FROM fichamentos
        ORDER BY tipo
    """)

    tipos = [linha[0] for linha in cursor.fetchall()]

    conn.close()

    return tipos