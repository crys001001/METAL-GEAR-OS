import customtkinter as ctk
from PIL import Image, ImageTk  # Manipulação avançada de imagens para o ícone
import webbrowser
import os

class JanelaSobre:
    def __init__(self, janela_principal):
        self.janela = ctk.CTkToplevel(janela_principal)
        self.janela.title("Sobre o Metal Gear OS")
        
        # --- CORREÇÃO AQUI: Aumentado de 620 para 680 para a frase caber perfeitamente! ---
        self.janela.geometry("500x680")
        self.janela.resizable(False, False)
        
        self.janela.transient(janela_principal)
        self.janela.grab_set() 
        
        # --- CONFIGURAÇÃO DO CAMINHO DA MÍDIA ---
        pasta_frontend = os.path.dirname(os.path.abspath(__file__))
        pasta_raiz = os.path.dirname(pasta_frontend)
        caminho_imagem = os.path.join(pasta_raiz, "ASSETS", "final_image.png")
        
        try:
            img_pil = Image.open(caminho_imagem)
            
            # --- VÍNCULO DO ÍCONE DA JANELA ---
            img_icone = ImageTk.PhotoImage(img_pil)
            self.janela.after(10, lambda: self.janela.iconphoto(False, img_icone))
            
            # Exibição centralizada ajustada
            img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(240, 250))
            ctk.CTkLabel(self.janela, text="", image=img_ctk).pack(pady=(20, 10))
            
        except Exception as erro:
            ctk.CTkLabel(self.janela, text=f"[ ERRO AO CARREGAR IMAGEM ]\nCaminho procurado:\n{caminho_imagem}", text_color="yellow").pack(pady=20)
        
        # --- CONFIGURAÇÃO DE DESIGN INTERNO E TIPOGRAFIA ---
        cor_militar = "#E5B800" # Amarelo/Dourado tático presente nos detalhes da arte
        
        # Título Principal com tipografia de impacto
        ctk.CTkLabel(self.janela, text="METAL GEAR OS", font=("Impact", 32), text_color=cor_militar).pack(pady=(10, 0))
        
        # Linha de metadados estilo terminal
        ctk.CTkLabel(self.janela, text="SISTEMA DE INSPEÇÃO POR VISÃO COMPUTACIONAL [v1.3.4]", font=("Consolas", 11, "bold"), text_color="#A0A0A0").pack(pady=(0, 15))
        
        # Painel do desenvolvedor com borda combinada
        frame_dev = ctk.CTkFrame(self.janela, fg_color="#1E1E1E", corner_radius=8, border_width=2, border_color=cor_militar)
        frame_dev.pack(pady=10, padx=30, fill="x")
        
        ctk.CTkLabel(frame_dev, text="> DESENVOLVEDOR LÍDER:", font=("Consolas", 11, "bold"), text_color=cor_militar).pack(pady=(15, 2))
        ctk.CTkLabel(frame_dev, text="Crystyan Vicente Gomes de Arruda", font=("Arial", 18, "bold"), text_color="#00FF00").pack(pady=2)
        ctk.CTkLabel(frame_dev, text="Análise e Desenvolvimento de Sistemas (ADS)", font=("Consolas", 11, "italic"), text_color="#CCCCCC").pack(pady=(0, 15))
        
        # Botões de Redes Sociais
        frame_links = ctk.CTkFrame(self.janela, fg_color="transparent")
        frame_links.pack(pady=15)
        
        meu_linkedin = "https://www.linkedin.com/in/crystyan-vicente-92723a26b/" 
        meu_github = "https://github.com/crys001001"          
        meu_youtube = "https://www.youtube.com/@crystyanvicente7681"
        
        btn_linkedin = ctk.CTkButton(frame_links, text="🔗 LinkedIn", font=("Arial", 13, "bold"), fg_color="#0077B5", hover_color="#005582", width=120, command=lambda: webbrowser.open(meu_linkedin))
        btn_linkedin.grid(row=0, column=0, padx=5)
        
        btn_github = ctk.CTkButton(frame_links, text="💻 GitHub", font=("Arial", 13, "bold"), fg_color="#333333", hover_color="#111111", width=120, command=lambda: webbrowser.open(meu_github))
        btn_github.grid(row=0, column=1, padx=5)
        
        btn_youtube = ctk.CTkButton(frame_links, text="▶️ YouTube", font=("Arial", 13, "bold"), fg_color="#FF0000", hover_color="#CC0000", width=120, command=lambda: webbrowser.open(meu_youtube))
        btn_youtube.grid(row=0, column=2, padx=5)
        
        # Rodapé com a citação do Venom Snake em fonte monoespaçada
        frase_venom = '"This is our new home. This is our heaven, and our hell.\nThis is Diamond Dogs."'
        ctk.CTkLabel(self.janela, text=f"{frase_venom}\n- Venom Snake", font=("Consolas", 10, "italic"), text_color="gray").pack(side="bottom", pady=20)