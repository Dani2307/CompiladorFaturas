# processor.py

import os
import shutil
import tempfile
from concurrent.futures import ProcessPoolExecutor
from typing import Dict, List

import difflib
import pytesseract
from PyPDF2 import PdfReader, PdfWriter

from config import SIMILARITY_CUTOFF, TESSERACT_CMD
from utils.pdf_utils import extrair_nome_cliente
from utils.ocr_utils import carregar_imagem_boleto, extrair_nome_pagador
from utils.zip_utils import extrair_arquivos_zip

# Configura o Tesseract
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def processar_pdfs(
    fat_path: str,
    bol_path: str,
    zip_folder: str,
    saida_folder: str,
    progress_callback=None,
    status_callback=None
) -> bool:
    """
    1) Lê PDFs de fatura e boleto.
    2) Extrai ZIPs e agrupa documentos por cliente.
    3) Converte páginas de boleto em imagens (paralelo) e faz OCR.
    4) Para cada página: identifica cliente, pagador e mescla fatura, boleto e ZIPs.
    5) Grava PDFs finais em saida_folder.
    """

    # Prepara diretório de saída
    os.makedirs(saida_folder, exist_ok=True)

    # 1) Leitura dos PDFs
    f_reader = PdfReader(fat_path)
    b_reader = PdfReader(bol_path)
    total = min(len(f_reader.pages), len(b_reader.pages))

    # 2) Extrai arquivos ZIP
    tmp_dir = tempfile.mkdtemp()
    docs_zip: Dict[str, List[str]] = extrair_arquivos_zip(zip_folder, tmp_dir)

    # 3) Converte páginas do boleto em imagens (em paralelo)
    # novo: usa a função top-level, passamos dois iteráveis
    with ProcessPoolExecutor() as executor:
        boleto_imgs = list(executor.map(
            carregar_imagem_boleto,  # função picklável
            [bol_path] * total,  # primeiro argumento: pdf_path
            range(total)  # segundo argumento: page_index
        ))

    # 4) Loop de mesclagem
    for idx in range(total):
        # a) Páginas brutas
        f_page = f_reader.pages[idx]
        b_page = b_reader.pages[idx]

        # b) Extrai nome do cliente (da fatura)
        texto_fat = f_page.extract_text() or ""
        cliente = extrair_nome_cliente(texto_fat)

        # c) OCR no boleto + extração de pagador
        try:
            texto_bol = pytesseract.image_to_string(boleto_imgs[idx], lang='por')
            pagador = extrair_nome_pagador(texto_bol)
        except Exception as e:
            # Fallback: usa o nome do cliente como pagador
            pagador = cliente

        # d) Cria writer e adiciona páginas
        writer = PdfWriter()
        writer.add_page(f_page)
        writer.add_page(b_page)

        # e) Anexa documentos do ZIP para esse cliente
        match = difflib.get_close_matches(cliente, docs_zip.keys(), n=1, cutoff=SIMILARITY_CUTOFF)
        if match:
            for doc in docs_zip[match[0]]:
                rdr = PdfReader(doc)
                for p in rdr.pages:
                    writer.add_page(p)

        # f) Grava PDF final
        out_path = os.path.join(saida_folder, f"{cliente}.pdf")
        with open(out_path, "wb") as f_out:
            writer.write(f_out)

        # g) Callbacks para GUI
        if progress_callback:
            progress_callback(idx + 1, total)
        if status_callback:
            status_callback(f"Cliente: {cliente} | Pagador: {pagador}")

    # 5) Limpa temporários
    shutil.rmtree(tmp_dir)
    return True
