import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from filtro_xml import carregar_filtro, mover_arquivos
from visuais import configurar_tema, carregar_icone, animar_fade_in_label

class XMLFilterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Extrator de Dados XML")
        self.geometry("720x720")
        self.minsize(600, 400)

        configurar_tema()

        self.pasta_origem = ctk.StringVar()
        self.pasta_destino = ctk.StringVar()
        self.arquivo_filtro = ctk.StringVar()
        self.tipo_filtro = ctk.StringVar(value="nNF")

        self.loading = False

        self.icone_pasta = carregar_icone("icones/pasta.png")  # Ícone para pastas
        self.icone_arquivo = carregar_icone("icones/arquivo.png")  # Ícone para selecionar arquivo
        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 20, 'pady': 10}

        ctk.CTkLabel(self, text="Pasta dos XMLs:").pack(anchor="w", **padding)
        frame_origem = ctk.CTkFrame(self)
        frame_origem.pack(fill="x", **padding)
        ctk.CTkEntry(frame_origem, textvariable=self.pasta_origem).pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkButton(frame_origem, text="Selecionar", image=self.icone_pasta,
                      compound="left", command=self.selecionar_pasta_origem, width=120).pack(side="right")

        ctk.CTkLabel(self, text="Pasta destino para XMLs filtrados:").pack(anchor="w", **padding)
        frame_destino = ctk.CTkFrame(self)
        frame_destino.pack(fill="x", **padding)
        ctk.CTkEntry(frame_destino, textvariable=self.pasta_destino).pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkButton(frame_destino, text="Selecionar", image=self.icone_pasta,
                      compound="left", command=self.selecionar_pasta_destino, width=120).pack(side="right")

        ctk.CTkLabel(self, text="Escolha o tipo de filtro:").pack(anchor="w", **padding)
        frame_filtros = ctk.CTkFrame(self)
        frame_filtros.pack(anchor="w", **padding)
        filtros = [("Número da Nota", "nNF"),
                   ("CNPJ do Destinatário", "CNPJ"),
                   ("Nome do Destinatário", "xNome")]
        for text, val in filtros:
            ctk.CTkRadioButton(frame_filtros, text=text, variable=self.tipo_filtro, value=val).pack(side="left", padx=10)

        ctk.CTkLabel(self, text="Arquivo de filtro (.txt) - um valor por linha:").pack(anchor="w", **padding)
        frame_arquivo = ctk.CTkFrame(self)
        frame_arquivo.pack(fill="x", **padding)
        ctk.CTkEntry(frame_arquivo, textvariable=self.arquivo_filtro).pack(side="left", fill="x", expand=True, padx=(0,10))
        ctk.CTkButton(frame_arquivo, text="Selecionar arquivo", image=self.icone_arquivo,
                      compound="left", command=self.selecionar_arquivo_filtro, width=140).pack(side="right")

        ctk.CTkLabel(self, text="Ou digite os valores para filtro (um por linha):").pack(anchor="w", **padding)
        self.text_manual = ctk.CTkTextbox(self, height=120)
        self.text_manual.pack(fill="both", padx=20, pady=(0,10), expand=False)

        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.pack(pady=(0,10))
        self.btn_executar = ctk.CTkButton(frame_botoes, text="Executar Filtro", command=self.executar_filtro, width=140)
        self.btn_executar.pack(side="left", padx=10)
        self.btn_limpar = ctk.CTkButton(frame_botoes, text="Limpar Filtros", command=self.limpar_filtros, width=140)
        self.btn_limpar.pack(side="left", padx=10)

        self.label_resultado = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.label_resultado.pack(pady=(10, 20))

    def selecionar_pasta_origem(self):
        path = filedialog.askdirectory()
        if path:
            self.pasta_origem.set(path)

    def selecionar_pasta_destino(self):
        path = filedialog.askdirectory()
        if path:
            self.pasta_destino.set(path)

    def selecionar_arquivo_filtro(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.arquivo_filtro.set(path)

    def limpar_filtros(self):
        self.arquivo_filtro.set("")
        self.text_manual.delete("1.0", ctk.END)
        self.label_resultado.configure(text="")

    def executar_filtro(self):
        pasta_origem = self.pasta_origem.get().strip()
        pasta_destino = self.pasta_destino.get().strip()
        tipo_filtro = self.tipo_filtro.get()

        if not pasta_origem:
            messagebox.showerror("Erro", "Pasta de origem inválida ou não selecionada.")
            return
        if not pasta_destino:
            messagebox.showerror("Erro", "Pasta destino inválida ou não selecionada.")
            return

        valores_filtro = carregar_filtro(self.arquivo_filtro.get(), self.text_manual.get("1.0", ctk.END).splitlines())
        if not valores_filtro:
            messagebox.showwarning("Aviso", "Nenhum valor para filtro foi informado.")
            return

        self.btn_executar.configure(state="disabled")
        self.btn_limpar.configure(state="disabled")

        threading.Thread(target=self.processar_filtro, args=(pasta_origem, pasta_destino, valores_filtro, tipo_filtro)).start()

    def processar_filtro(self, pasta_origem, pasta_destino, valores_filtro, tipo_filtro):
        total = mover_arquivos(pasta_origem, pasta_destino, valores_filtro, tipo_filtro, lambda msg: None)

        def atualizar_ui():
            if total == 0:
                self.label_resultado.configure(text="Nenhum arquivo XML foi extraído.")
            else:
                self.label_resultado.configure(text=f"Total de arquivos movidos: {total}")
            animar_fade_in_label(self.label_resultado)
            self.btn_executar.configure(state="normal")
            self.btn_limpar.configure(state="normal")

        self.after(0, atualizar_ui)

if __name__ == "__main__":
    app = XMLFilterApp()
    app.mainloop()
