# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 18:58:45 2026

@author: Vitoria
"""

import streamlit as st


def titulo(texto, subtitulo=None):
    st.markdown(
        f"""
        <h1 style="
            font-size:2.0rem;
            margin-bottom:0.2rem;
            color:#2B2B2B;
            font-weight:700;
        ">
            {texto}
        </h1>
        """,
        unsafe_allow_html=True
    )

    if subtitulo:
        st.markdown(
            f"""
            <p style="
                color:#666666;
                font-size:1.0rem;
                margin-top:0;
                margin-bottom:2rem;
            ">
                {subtitulo}
            </p>
            """,
            unsafe_allow_html=True
        )