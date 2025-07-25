# utils/zip_utils.py

import os
import zipfile
from collections import defaultdict
from PIL import Image
from config import VALID_IMAGE_EXTS


def imagem_para_pdf(caminho_img: str, caminho_pdf_saida: str) -> None:
    """
    Converte uma imagem (jpg/png) em PDF.
    """
    img = Image.open(caminho_img)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save(caminho_pdf_saida, "PDF")


def extrair_arquivos_zip(pasta_zip: str, pasta_destino: str) -> dict:
    """
    Descompacta todos os ZIPs em pasta_destino, converte imagens em PDF
    e agrupa os arquivos resultantes por nome de cliente.

    A chave do dicionário é o nome do cliente (tudo após o primeiro '_'
    no nome do arquivo original) e o valor é lista de caminhos de PDF.
    """
    arquivos_por_cliente = defaultdict(list)

    # 1) Descompacta todos os ZIPs
    for nome_zip in os.listdir(pasta_zip):
        if nome_zip.lower().endswith(".zip"):
            caminho_zip = os.path.join(pasta_zip, nome_zip)
            with zipfile.ZipFile(caminho_zip, 'r') as z:
                z.extractall(pasta_destino)

    # 2) Percorre os arquivos extraídos
    for raiz, _, arquivos in os.walk(pasta_destino):
        for nome in arquivos:
            caminho = os.path.join(raiz, nome)
            nome_base, ext = os.path.splitext(nome)
            # Cliente é o texto após o primeiro '_'
            partes = nome_base.split("_", 1)
            cliente = (partes[1] if len(partes) > 1 else partes[0]).strip()
            cliente = cliente.replace("/", "-")

            # Se for imagem, converte em PDF
            if ext.lower() in VALID_IMAGE_EXTS:
                pdf_convertido = caminho + ".pdf"
                imagem_para_pdf(caminho, pdf_convertido)
                arquivos_por_cliente[cliente].append(pdf_convertido)

            # Se for PDF, adiciona direto
            elif ext.lower() == ".pdf":
                arquivos_por_cliente[cliente].append(caminho)

    return arquivos_por_cliente
