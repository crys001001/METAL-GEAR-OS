import customtkinter as ctk
from PIL import Image, ImageTk  # <-- Adicionado para o ícone
import os  # <-- Adicionado para localizar o ícone

class JanelaLogin:
    def __init__(self, janela_principal, controlador):
        self.janela_principal = janela_principal
        self.controlador = controlador
        
        self.janela_principal.withdraw() 
        self.tela_login = ctk.CTkToplevel(self.janela_principal)
        self.tela_login.title("METAL GEAR - Acesso Restrito")
        self.tela_login.geometry("400x350")
        self.tela_login.resizable(False, False)
        self.tela_login.transient(self.janela_principal) 
        self.tela_login.protocol("WM_DELETE_WINDOW", self.janela_principal.destroy)
        
        # ==========================================
        # --- ÍCONE TÁTICO NA TELA DE LOGIN ---
        # ==========================================
        try:
            pasta_frontend = os.path.dirname(os.path.abspath(__file__))
            pasta_raiz = os.path.dirname(pasta_frontend)
            caminho_icone = os.path.join(pasta_raiz, "ASSETS", "final_image.png")
            
            img_icone = ImageTk.PhotoImage(Image.open(caminho_icone))
            self.tela_login.after(10, lambda: self.tela_login.iconphoto(False, img_icone))
        except Exception:
            pass
        # ==========================================
        
        # CORES E FONTES ATUALIZADAS PARA COMBINAR COM A LOGO
        cor_militar = "#E5B800"

        ctk.CTkLabel(self.tela_login, text="METAL GEAR", font=("Impact", 36), text_color=cor_militar).pack(pady=(30, 5))
        ctk.CTkLabel(self.tela_login, text="AUTENTICAÇÃO DE SEGURANÇA", font=("Consolas", 12, "bold"), text_color="#A0A0A0").pack(pady=(0, 20))
        
        self.entrada_usuario = ctk.CTkEntry(self.tela_login, placeholder_text="Nome de Utilizador", width=250, height=40)
        self.entrada_usuario.pack(pady=10)
        
        self.entrada_senha = ctk.CTkEntry(self.tela_login, placeholder_text="Palavra-passe", show="*", width=250, height=40)
        self.entrada_senha.pack(pady=10)
        
        self.label_erro = ctk.CTkLabel(self.tela_login, text="", text_color="red", font=("Arial", 12))
        self.label_erro.pack()
        
        botao_entrar = ctk.CTkButton(self.tela_login, text="ENTRAR NO SISTEMA", font=("Consolas", 14, "bold"), width=250, height=45, fg_color="#1A4D2E", hover_color="#0d2b18", command=lambda: self.controlador.tentar_login(self.entrada_usuario.get(), self.entrada_senha.get()))
        botao_entrar.pack(pady=15)

    def mostrar_erro(self, msg):
        self.label_erro.configure(text=msg)

    def fechar_e_liberar(self):
        self.tela_login.destroy()
        self.janela_principal.deiconify()