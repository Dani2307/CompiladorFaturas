# Combina Arquivos – Contabitec

Uma aplicação desktop em Python que combina automaticamente:

* **Faturas** (PDF)
* **Boletos** (OCR via Tesseract)
* **Documentos ZIP** (PDF ou imagem)

Gerando um **PDF final por cliente** na sequência:

```
Fatura → Boleto → Documentos do ZIP
```

---

## 📁 Estrutura do Projeto

```
combina_arquivos/  
├── README.md            # Documentação do projeto (você está aqui)  
├── config.py           # Configurações (paths relativos, DPI, cutoff)  
├── main.py             # Entry point (multiprocessing + GUI)  
├── gui.py              # Interface gráfica Tkinter  
├── processor.py        # Lógica de processamento (fatura, OCR, ZIP)  
├── requirements.txt    # Dependências pip  
├── vendor/             # Bibliotecas portáteis  
│   ├── poppler/        # Poppler executáveis e DLLs  
│   │   └── bin/        # pdftoppm.exe, pdftocairo.exe, *.dll  
│   └── tesseract/      # Tesseract OCR (exe, DLLs, tessdata/)  
├── resources/          # Recursos estáticos (logo.png)  
└── utils/              # Módulos utilitários  
    ├── __init__.py     # Pacote Python  
    ├── pdf_utils.py    # Leitura e mesclagem de PDFs  
    ├── ocr_utils.py    # OCR e extração de nome do pagador  
    └── zip_utils.py    # Extração de ZIPs e conversão de imagens
```

---

## 🚀 Pré-requisitos

* **Python 3.8+**
* **Poppler** portátil (incluído em `vendor/poppler/bin`)

  * Ferramentas: `pdftoppm.exe`, `pdftocairo.exe`, etc.
* **Tesseract OCR** portátil (incluído em `vendor/tesseract`)

  * Executável `tesseract.exe`, DLLs e pasta `tessdata/por.traineddata`

> *No Windows, `tkinter` já vem com Python. No Linux, instale `python3-tk`.*

---

## 💻 Instalação e Execução

1. Clone ou copie este diretório e entre nele:

   ```bash
   git clone <repo_url> combina_arquivos
   cd combina_arquivos
   ```
2. Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
3. Instale as dependências Python:

   ```bash
   pip install -r requirements.txt
   ```
4. Ajuste (se desejar) os parâmetros em `config.py`:

   ```python
   # Paths serão resolvidos automaticamente via sys._MEIPASS em build.
   OCR_DPI = 200               # Resolução para OCR
   SIMILARITY_CUTOFF = 0.6     # Similaridade de nomes ZIP
   ```
5. Execute a aplicação:

   ```bash
   python main.py
   ```

   * Selecione: PDF de Faturas, PDF de Boletos, Pasta de ZIPs e Pasta de Saída.
   * Acompanhe a barra de progresso e receba os PDFs finais.

---

## 📦 Empacotamento com PyInstaller

Para gerar um executável standalone (`.exe`) que inclua Poppler, Tesseract e seus módulos:

1. Instale o PyInstaller no seu venv:

   ```bash
   pip install pyinstaller
   ```
2. Na raiz do projeto, crie (ou ajuste) `build.spec` com conteúdo como:

   ```python
   # -*- mode: python -*-
   import os
   block_cipher = None

   project_root = os.path.abspath(os.path.dirname(__file__))

   a = Analysis(
       ['main.py'],
       pathex=[project_root],
       binaries=[
           ('vendor/poppler/bin/*.exe', 'vendor/poppler/bin'),
           ('vendor/poppler/bin/*.dll', 'vendor/poppler/bin'),
           ('vendor/tesseract/tesseract.exe', 'vendor/tesseract'),
           ('vendor/tesseract/*.dll', 'vendor/tesseract'),
       ],
       datas=[
           ('resources/logo.png', 'resources'),
           ('vendor/tesseract/tessdata/*.traineddata', 'vendor/tesseract/tessdata'),
       ],
       hiddenimports=[],
       hookspath=[],
       runtime_hooks=[],
       cipher=block_cipher
   )
   pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
   exe = EXE(
       pyz,
       a.scripts,
       exclude_binaries=True,
       name='CompiladorFaturas',
       console=False,
       strip=False,
       upx=True,
   )
   coll = COLLECT(
       exe,
       a.binaries,
       a.datas,
       strip=False,
       upx=True,
       name='CompiladorFaturas'
   )
   ```
3. Execute:

   ```bash
   pyinstaller build.spec
   ```
4. O executável e todas as dependências (Poppler, Tesseract, libs Python) estarão em `dist/CompiladorFaturas/`.

---

## 🧪 Testes

Rode testes unitários em `tests/` com:

```bash
pytest
```

---

## 🤝 Contribuição

1. Fork no GitHub
2. Branch: `git checkout -b feature/minha-melhoria`
3. Commit: `git commit -m "Descrição da melhoria"`
4. PR: `git push origin feature/minha-melhoria`

---

## 📄 Licença

MIT © Contabitec
