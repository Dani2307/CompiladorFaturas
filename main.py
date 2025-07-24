# main.py

import multiprocessing

if __name__ == "__main__":
    # Necessário no Windows + PyInstaller
    multiprocessing.freeze_support()

    # Só aqui importamos e rodamos a GUI
    from gui import run_app
    run_app()
