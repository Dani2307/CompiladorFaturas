# config.py


import os
import sys

# quando empacotado pelo PyInstaller, ele extrai tudo em _MEIPASS;
# caso contrário, usamos a pasta do próprio script
base_path = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))

# caminhos das ferramentas, relativos a base_path
POPPLER_PATH = os.path.join(base_path, "vendor","vendor", "poppler", "bin")
TESSERACT_CMD = os.path.join(base_path, "vendor", "vendor", "tesseract", "tesseract.exe")

# DPI padrão para OCR
OCR_DPI = 150

# cutoff de similaridade
SIMILARITY_CUTOFF = 0.6

# extensões de imagem válidas para ZIPs
VALID_IMAGE_EXTS = (".jpg", ".jpeg", ".png")