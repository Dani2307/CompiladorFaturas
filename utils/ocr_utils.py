# utils/ocr_utils.py

import re
from typing import List
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from config import POPPLER_PATH, TESSERACT_CMD, OCR_DPI

# Aponta o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def carregar_imagem_boleto(pdf_path: str, page_index: int) -> Image.Image:
    """
    Converte a página `page_index` do PDF em imagem PIL, usando o DPI de OCR.
    """
    imagens: List[Image.Image] = convert_from_path(
        pdf_path,
        dpi=OCR_DPI,
        poppler_path=POPPLER_PATH,
        first_page=page_index + 1,
        last_page=page_index + 1
    )
    return imagens[0]

def limpar_nome_pagador(texto: str) -> str:
    """
    Remove termos desnecessários e caracteres inválidos para nome de arquivo.
    """
    nome = texto.strip().replace('\n', ' ').replace('\r', ' ')
    nome = re.sub(r'(?i)Nosso Número\s*', '', nome)
    nome = re.sub(r'\s*-\s*.*$', '', nome)
    nome = re.sub(r'[\\/:*?"<>|]', '', nome)
    nome = re.sub(r'\s+', ' ', nome)
    return nome.strip()

def extrair_nome_pagador(texto: str) -> str:
    """
    Tenta extrair via regex a linha que começa com 'Pagador:'.
    Se não encontrar, busca algumas linhas abaixo.
    Retorna 'DESCONHECIDO' como fallback.
    """
    # 1) Tentar regex direta
    match = re.search(r"Pagador[:\s]+([A-Z0-9\s\.\-ÇÃÕÊÁÉÍÓÚÂÔ]+)", texto, re.IGNORECASE)
    if match:
        return limpar_nome_pagador(match.group(1))

    # 2) Heurística por proximidade de linha
    linhas = texto.splitlines()
    for i, linha in enumerate(linhas):
        if "Pagador" in linha:
            for j in range(1, 4):
                if i + j < len(linhas):
                    cand = linhas[i + j].strip()
                    if cand and not re.search(
                        r"Nosso Número|Agência|CNPJ|CPF|Vencimento", cand, re.IGNORECASE
                    ):
                        return limpar_nome_pagador(cand)

    return "DESCONHECIDO"
