import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from utils import recurso_path  

def configurar_tema():
    # Define modo escuro e usa o tema padrão dark do CTk
    ctk.set_appearance_mode("dark")

def carregar_icone(caminho, tamanho=(24, 24)):
    caminho_absoluto = recurso_path(caminho)
    imagem_pil = Image.open(caminho_absoluto).resize(tamanho, Image.Resampling.LANCZOS)
    ctk_imagem = CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=tamanho)
    return ctk_imagem

def animar_fade_in_label(label, i=0):
    if i > 10:
        return
    alfa = int(25 * i)
    cor = f"#{alfa:02x}{alfa:02x}{alfa:02x}"
    label.configure(text_color=cor)
    label.after(50, animar_fade_in_label, label, i+1)
