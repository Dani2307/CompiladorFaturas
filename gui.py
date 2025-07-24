import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Frame, Label, Button, Progressbar
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk

from processor import processar_pdfs

def run_app():
    root = tk.Tk()
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
    root.title("Compilador de Arquivos de Faturamento – Grupo 44")
    root.geometry("600x350")
    root.resizable(False, False)

    # Tema moderno
    style = ThemedStyle(root)
    style.set_theme("arc")
    # Estilo personalizado para o botão Iniciar
    style.configure('Start.TButton', background='#76AB93', foreground='#76AB93', font=('Helvetica', 12, 'bold'))

    # ─── Layout em Frames ───
    top = Frame(root, padding=10)
    top.grid(row=0, column=0, sticky="ew")
    top.grid_columnconfigure(0, weight=1)

    middle = Frame(root, padding=10)
    middle.grid(row=1, column=0, sticky="nsew")
    bottom = Frame(root, padding=10)
    bottom.grid(row=2, column=0, sticky="ew")

    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # ─── Topo: logo + slogan centralizados ───
    logo_path = os.path.join(os.path.dirname(__file__), "resources", "logo.png")
    if os.path.exists(logo_path):
        img = Image.open(logo_path).resize((350, 80), Image.LANCZOS)
        logo = ImageTk.PhotoImage(img)
        Label(top, image=logo).grid(row=0, column=0, pady=(0,10))
        top.logo = logo

    Label(top,
          text="Conte com a Contabitec para simplificar!",
          font=("Helvetica", 14, "bold")
    ).grid(row=1, column=0)

    # ─── Meio: apenas Iniciar Processamento com cor personalizada ───
    start_btn = Button(
        middle,
        text="Iniciar Processamento",
        padding=(20,10),
        style='Start.TButton'
    )
    middle.grid_columnconfigure(0, weight=1)
    start_btn.grid(row=0, column=0, pady=40)

    # ─── Barras e Status ───
    prog = Progressbar(bottom, orient="horizontal", length=580, mode="determinate")
    prog.grid(row=0, column=0, columnspan=3, pady=(0,10))
    status = Label(bottom, text="Aguardando ação...", font=("Helvetica", 10))
    status.grid(row=1, column=0, columnspan=3)

    # ─── Rodapé: Ajuda e Sair alinhados à direita ───
    bottom.grid_columnconfigure(0, weight=1)
    ajuda_btn = Button(bottom, text="Ajuda")
    sair_btn  = Button(bottom, text="Sair")
    ajuda_btn.grid(row=2, column=1, sticky="e", padx=(0,5))
    sair_btn.grid(row=2, column=2, sticky="e")

    # ─── Callbacks ───
    arquivos = {"fat":None, "bol":None, "zip":None, "out":None}

    def task():
        start_btn.state(["disabled"])
        def on_progress(done, total):
            prog["maximum"] = total; prog["value"] = done
        def on_status(txt):
            status.config(text=txt)
        ok = processar_pdfs(
            arquivos["fat"], arquivos["bol"],
            arquivos["zip"], arquivos["out"],
            on_progress, on_status
        )
        if ok:
            messagebox.showinfo("Sucesso", f"Arquivos prontos em:\n{arquivos['out']}")
        start_btn.state(["!disabled"])

    def iniciar():
        arquivos["fat"] = filedialog.askopenfilename(
            title="PDF de Faturas", filetypes=[("PDF","*.pdf")]
        )
        arquivos["bol"] = filedialog.askopenfilename(
            title="PDF de Boletos", filetypes=[("PDF","*.pdf")]
        )
        arquivos["zip"] = filedialog.askdirectory(title="Pasta de ZIPs")
        arquivos["out"] = filedialog.askdirectory(title="Pasta de Saída")
        if None in arquivos.values() or "" in arquivos.values():
            messagebox.showwarning("Aviso", "Selecione todos os itens antes de continuar!")
            return
        threading.Thread(target=task, daemon=True).start()

    start_btn.config(command=iniciar)
    sair_btn.config(command=root.quit)
    ajuda_btn.config(command=lambda: os.startfile(
        os.path.join(os.path.dirname(__file__), "resources", "Manual_Ajuda.pdf")
    ))

    root.mainloop()

if __name__ == "__main__":
    run_app()
