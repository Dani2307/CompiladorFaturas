# build.spec
# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

block_cipher = None

# Caminho absoluto para a raiz do projeto (onde está o build.spec)
project_root = os.path.abspath(os.getcwd())

a = Analysis(
    ['main.py'],                     # seu entry point
    pathex=[project_root],           # onde procurar o main.py
    binaries=[
        # Poppler executáveis e DLLs
        ('vendor/poppler/bin/pdftoppm.exe', 'vendor/poppler/bin'),
        ('vendor/poppler/bin/pdftocairo.exe', 'vendor/poppler/bin'),
        ('vendor/poppler/bin/*.dll',   'vendor/poppler/bin'),
        # Tesseract executável e DLLs
        ('vendor/tesseract/tesseract.exe', 'vendor/tesseract'),
        ('vendor/tesseract/*.dll',       'vendor/tesseract'),
    ],
    datas=[
        # Logo
        ('resources/logo.png', 'resources'),
        # Manual de Ajuda PDF
        ('resources/Manual_Ajuda.pdf', 'resources'),
        # Arquivos de idiomas do Tesseract
        ('vendor/tesseract/tessdata/*.traineddata', 'vendor/tesseract/tessdata'),
        # Icone da aplicação
        ('resources/icon.ico', 'resources'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],                    # não adiciona binários extras aqui
    exclude_binaries=True,
    name='CompiladorFaturas',
    icon=os.path.join('resources', 'icon.ico'),  # ícone do executável
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,         # janela GUI sem console
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='CompiladorFaturas'
)
