# utils/pdf_utils.py

import re
from typing import List
from PyPDF2 import PdfReader, PdfWriter

def extrair_nome_cliente(texto: str) -> str:
    """
    Extrai o nome do cliente de um texto de fatura usando regex.
    Se não encontrar, gera um identificador genérico.
    """
    match = re.search(r"Cliente\.\:\s*\d+\s*-\s*(.+)", texto)
    if match:
        return match.group(1).strip().replace("/", "-")
    # Fallback: hash simples para evitar colisões
    return f"CLIENTE_{abs(hash(texto)) % 1000000}"

def mesclar_pdfs(caminhos: List[str], caminho_saida: str) -> None:
    """
    Recebe uma lista de caminhos de arquivos PDF e cria um único PDF de saída
    com todas as páginas na ordem em que aparecem na lista.
    """
    writer = PdfWriter()
    for pdf_path in caminhos:
        reader = PdfReader(pdf_path)
        for pagina in reader.pages:
            writer.add_page(pagina)
    # Grava o PDF resultante
    with open(caminho_saida, "wb") as f:
        writer.write(f)
