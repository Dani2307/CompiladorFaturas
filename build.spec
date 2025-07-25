import os
import glob
from PyInstaller.utils.hooks import collect_submodules
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

block_cipher = None

project_root = os.path.abspath(os.getcwd())

# Listando DLLs do Poppler
poppler_dlls = [
    (dll, 'vendor/vendor/poppler/bin') for dll in glob.glob(os.path.join(project_root, 'vendor', 'vendor', 'poppler', 'bin', '*.dll'))
]
# Listando DLLs do Tesseract
tesseract_dlls = [
    (dll, 'vendor/vendor/tesseract') for dll in glob.glob(os.path.join(project_root, 'vendor', 'vendor', 'tesseract', '*.dll'))
]
# Listando arquivos traineddata do Tesseract
tessdata_files = [
    (td, 'vendor/vendor/tesseract/tessdata') for td in glob.glob(os.path.join(project_root, 'vendor', 'vendor', 'tesseract', 'tessdata', '*.traineddata'))
]

a = Analysis(
    ['main.py'],
    pathex=[project_root],
    binaries=[
        (os.path.join(project_root, 'vendor', 'vendor', 'poppler', 'bin', 'pdftoppm.exe'), 'vendor/vendor/poppler/bin'),
        (os.path.join(project_root, 'vendor', 'vendor', 'poppler', 'bin', 'pdftocairo.exe'), 'vendor/vendor/poppler/bin'),
        (os.path.join(project_root, 'vendor', 'vendor', 'tesseract', 'tesseract.exe'), 'vendor/vendor/tesseract'),
    ] + poppler_dlls + tesseract_dlls,
    datas=[
        (os.path.join(project_root, 'vendor', 'vendor', 'poppler', 'bin'), 'vendor/vendor/poppler/bin'),
        (os.path.join(project_root, 'vendor', 'vendor', 'tesseract'), 'vendor/vendor/tesseract'),
    ] + tessdata_files,

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
    [],
    exclude_binaries=True,
    name='CompiladorFaturas',
    icon=None,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='CompiladorFaturas'
)