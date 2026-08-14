# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 15:02:22 2026

@author: Vitoria
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))

python_venv = os.path.join(
    BASE_DIR,
    "venv",
    "Scripts",
    "python.exe"
)

app = os.path.join(BASE_DIR, "app.py")

subprocess.Popen([
    python_venv,
    "-m",
    "streamlit",
    "run",
    app
]) 


# Depois para gerar o arquivo executável pelo powershell: 
# pyinstaller --onedir --windowed --icon=icone.ico --name Fichamentos launcher.py 