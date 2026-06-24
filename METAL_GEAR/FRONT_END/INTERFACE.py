import customtkinter as ctk
from tkinter import ttk

from FRONT_END.UI_ESTILOS import aplicar_tema_tabela, MENU_PRODUTOS, MENU_RELATORIO, CHECKBOX
from FRONT_END.UI_LOGIN import JanelaLogin
from FRONT_END.UI_GRAFICO import GraficoProducao
from FRONT_END.UI_SOBRE import JanelaSobre  # <-- Nova importação da tela de créditos adicionada aqui!

class TelaMetalGear:
    def __init__(self, janela, controlador):
        self.janela = janela
        self.controlador = controlador  
        
        # 1. TEXTOS BALANCEADOS (Mesma largura para os botões ficarem iguais)
        self.NOME_ABA_1 = "     ⚙️ Painel     "
        self.NOME_ABA_2 = "   📊 Relatórios   "
        self.NOME_ABA_3 = " ⚙️ Configurações "
        
        aplicar_tema_tabela() 
        
        self.construir_tela_principal()
        self.login = JanelaLogin(self.janela, self.controlador)
        
    def construir_tela_principal(self):
        self.janela.grid_columnconfigure(0, weight=6, uniform="a") 
        self.janela.grid_columnconfigure(1, weight=4, uniform="a")
        self.janela.grid_rowconfigure(0, weight=1)
        
        self.frame_camera = ctk.CTkFrame(self.janela, corner_radius=10, fg_color="#1E1E1E")
        self.frame_camera.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.frame_camera, text="CONTROLE DE QUALIDADE", font=("Arial", 40, "bold"), text_color="white").pack(pady=20)
        self.tela_video = ctk.CTkLabel(self.frame_camera, text="", fg_color="black")
        self.tela_video.pack(pady=10, padx=10, expand=True, fill="both")
        
        self.frame_status_bar = ctk.CTkFrame(self.frame_camera, fg_color="transparent", height=30)
        self.frame_status_bar.pack(side="bottom", fill="x", padx=15, pady=5)
        self.label_relogio = ctk.CTkLabel(self.frame_status_bar, text="🕒 Hora: 00:00:00", font=("Arial", 12, "bold"), text_color="#3A7EB8")
        self.label_relogio.pack(side="left", padx=10)
        self.label_uptime = ctk.CTkLabel(self.frame_status_bar, text="⏳ Operação: 00h 00m 00s", font=("Arial", 12, "bold"), text_color="white")
        self.label_uptime.pack(side="right", padx=10)
        
        def quando_mudar_aba():
            if self.abas.get() == self.NOME_ABA_2: self.controlador.carregar_dados_na_tabela()
                
        self.abas = ctk.CTkTabview(self.janela, command=quando_mudar_aba)
        self.abas.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # 2. FONTE REDUZIDA PARA CABER PERFEITAMENTE EM MODO JANELA
        self.abas._segmented_button.configure(font=("Arial", 14, "bold"))
        
        self.aba_controle = self.abas.add(self.NOME_ABA_1)
        self.aba_relatorio = self.abas.add(self.NOME_ABA_2)
        self.aba_config = self.abas.add(self.NOME_ABA_3)
        
        # ==========================================
        # --- ABA 1: PAINEL DE CONTROLE ---
        # ==========================================
        botao_emergencia = ctk.CTkButton(self.aba_controle, text="PARADA DE EMERGÊNCIA", fg_color="red", hover_color="#5c0000", font=("Arial", 16, "bold"), height=50)
        botao_emergencia.pack(side="bottom", pady=10, padx=10, fill="x")
        
        painel_scroll = ctk.CTkScrollableFrame(self.aba_controle, fg_color="transparent")
        painel_scroll.pack(side="top", fill="both", expand=True)
        
        frame_seletor = ctk.CTkFrame(painel_scroll, fg_color="#1E1E1E", border_width=2, border_color="#3A7EB8", corner_radius=8)
        frame_seletor.pack(pady=5, padx=10, fill="x")
        
        # LER A MEMÓRIA PARA SABER QUAIS CAIXINHAS DEVEM ESTAR MARCADAS
        regras_salvas = self.controlador.config.get("regras", {"cores": ["VERMELHO", "VERDE", "AZUL", "AMARELO"], "numeros": [1, 2, 3, 4, 5, 6]})
        cores_mem = regras_salvas.get("cores", [])
        num_mem = regras_salvas.get("numeros", [])

        ctk.CTkLabel(frame_seletor, text="Cores Permitidas", font=("Arial", 14, "bold"), text_color="#3A7EB8").pack(pady=(8, 0))
        frame_grid_cores = ctk.CTkFrame(frame_seletor, fg_color="transparent")
        frame_grid_cores.pack(fill="x", padx=10, pady=2)
        frame_grid_cores.grid_columnconfigure((0, 1), weight=1)
        
        self.var_vermelho = ctk.BooleanVar(value=("VERMELHO" in cores_mem))
        self.var_verde = ctk.BooleanVar(value=("VERDE" in cores_mem))
        self.var_azul = ctk.BooleanVar(value=("AZUL" in cores_mem))
        self.var_amarelo = ctk.BooleanVar(value=("AMARELO" in cores_mem))
        
        self.cb_vermelho = ctk.CTkCheckBox(frame_grid_cores, text="Vermelho", variable=self.var_vermelho, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        self.cb_verde = ctk.CTkCheckBox(frame_grid_cores, text="Verde", variable=self.var_verde, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        self.cb_azul = ctk.CTkCheckBox(frame_grid_cores, text="Azul", variable=self.var_azul, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        self.cb_amarelo = ctk.CTkCheckBox(frame_grid_cores, text="Amarelo", variable=self.var_amarelo, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        
        self.cb_vermelho.grid(row=0, column=0, pady=4); self.cb_verde.grid(row=0, column=1, pady=4)
        self.cb_azul.grid(row=1, column=0, pady=4); self.cb_amarelo.grid(row=1, column=1, pady=4)
        
        ctk.CTkLabel(frame_seletor, text="Números Permitidos", font=("Arial", 14, "bold"), text_color="#3A7EB8").pack(pady=(8, 0))
        frame_grid_numeros = ctk.CTkFrame(frame_seletor, fg_color="transparent")
        frame_grid_numeros.pack(fill="x", padx=10, pady=(2, 8))
        frame_grid_numeros.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.var_1 = ctk.BooleanVar(value=(1 in num_mem)); self.var_2 = ctk.BooleanVar(value=(2 in num_mem)); self.var_3 = ctk.BooleanVar(value=(3 in num_mem))
        self.var_4 = ctk.BooleanVar(value=(4 in num_mem)); self.var_5 = ctk.BooleanVar(value=(5 in num_mem)); self.var_6 = ctk.BooleanVar(value=(6 in num_mem))
        
        self.cb_1 = ctk.CTkCheckBox(frame_grid_numeros, text="1", variable=self.var_1, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        self.cb_2 = ctk.CTkCheckBox(frame_grid_numeros, text="2", variable=self.var_2, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        self.cb_3 = ctk.CTkCheckBox(frame_grid_numeros, text="3", variable=self.var_3, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        self.cb_4 = ctk.CTkCheckBox(frame_grid_numeros, text="4", variable=self.var_4, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        self.cb_5 = ctk.CTkCheckBox(frame_grid_numeros, text="5", variable=self.var_5, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        self.cb_6 = ctk.CTkCheckBox(frame_grid_numeros, text="6", variable=self.var_6, command=lambda: self.controlador.aplicar_regras_dinamicas(), **CHECKBOX)
        
        self.cb_1.grid(row=0, column=0, pady=4); self.cb_2.grid(row=0, column=1, pady=4); self.cb_3.grid(row=0, column=2, pady=4)
        self.cb_4.grid(row=1, column=0, pady=4); self.cb_5.grid(row=1, column=1, pady=4); self.cb_6.grid(row=1, column=2, pady=4)
        
        self.lista_todas_checkboxes = [self.cb_vermelho, self.cb_verde, self.cb_azul, self.cb_amarelo, self.cb_1, self.cb_2, self.cb_3, self.cb_4, self.cb_5, self.cb_6]
        
        frame_contadores = ctk.CTkFrame(painel_scroll, fg_color="transparent")
        frame_contadores.pack(pady=5, padx=10, fill="x")
        frame_contadores.grid_columnconfigure((0, 1), weight=1, uniform="b")
        
        frame_aprovados = ctk.CTkFrame(frame_contadores, fg_color="#1A4D2E")
        frame_aprovados.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        ctk.CTkLabel(frame_aprovados, text="APROVADOS", font=("Arial", 14, "bold")).pack(pady=5)
        self.texto_aprovados = ctk.CTkLabel(frame_aprovados, text="0", font=("Arial", 36, "bold"))
        self.texto_aprovados.pack(pady=(0, 5))
        
        frame_rejeitados = ctk.CTkFrame(frame_contadores, fg_color="#780000")
        frame_rejeitados.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        ctk.CTkLabel(frame_rejeitados, text="REJEITADOS", font=("Arial", 14, "bold")).pack(pady=5)
        self.texto_rejeitados = ctk.CTkLabel(frame_rejeitados, text="0", font=("Arial", 36, "bold"))
        self.texto_rejeitados.pack(pady=(0, 5))
        
        frame_historico = ctk.CTkFrame(painel_scroll, fg_color="#1E1E1E", border_width=2, border_color="#3A7EB8", corner_radius=8)
        frame_historico.pack(pady=5, padx=10, fill="both", expand=True) 
        ctk.CTkLabel(frame_historico, text="Relatório Atual", font=("Arial", 14, "bold"), text_color="white").pack(pady=(5, 2))
        self.label_historico = ctk.CTkLabel(frame_historico, text="Nenhuma peça processada", font=("Arial", 16, "bold"), text_color="yellow", justify="center", height=130, anchor="n")
        self.label_historico.pack(pady=5, padx=10, fill="both", expand=True)
        

        # ==========================================
        # --- ABA 2: RELATÓRIOS ---
        # ==========================================
        self.texto_feedback = ctk.CTkLabel(self.aba_relatorio, text="Tabela sincronizada.", font=("Arial", 12))
        self.texto_feedback.pack(side="bottom", pady=(0, 10))
        
        frame_botoes = ctk.CTkFrame(self.aba_relatorio, fg_color="transparent")
        frame_botoes.pack(side="bottom", fill="x", padx=10, pady=(5, 0))
        
        botao_atualizar = ctk.CTkButton(frame_botoes, text="🔄 ATUALIZAÇÃO DE DADOS", font=("Arial", 14, "bold"), fg_color="#1F538D", hover_color="#14375E", height=40, command=self.controlador.carregar_dados_na_tabela)
        botao_atualizar.pack(side="top", pady=5, fill="x")
        
        frame_exportadores = ctk.CTkFrame(frame_botoes, fg_color="transparent")
        frame_exportadores.pack(side="top", fill="x", pady=5)
        frame_exportadores.grid_columnconfigure((0, 1), weight=1, uniform="b")

        botao_exportar_pdf = ctk.CTkButton(frame_exportadores, text="📥 GERAR PDF", font=("Arial", 14, "bold"), fg_color="#780000", hover_color="#5c0000", height=40, command=self.controlador.solicitar_pdf)
        botao_exportar_pdf.grid(row=0, column=0, padx=4, sticky="ew")

        botao_exportar_csv = ctk.CTkButton(frame_exportadores, text="📊 EXPORTAR EXCEL", font=("Arial", 14, "bold"), fg_color="#1A4D2E", hover_color="#0d2b18", height=40, command=self.controlador.solicitar_csv)
        botao_exportar_csv.grid(row=0, column=1, padx=4, sticky="ew")


        ctk.CTkLabel(self.aba_relatorio, text="EXPORTAÇÃO DE DADOS", font=("Arial", 24, "bold")).pack(side="top", pady=10)
        
        frame_filtros = ctk.CTkFrame(self.aba_relatorio)
        frame_filtros.pack(side="top", pady=5, padx=10, fill="x")
        ctk.CTkLabel(frame_filtros, text="Período:", font=("Arial", 14, "bold")).pack(pady=5)
        self.opcao_filtro = ctk.StringVar(value="Últimas 48 Horas")
        
        def alternar_campos_data(escolha):
            if escolha == "Data Específica": self.frame_datas_manuais.pack(pady=5)
            else: self.frame_datas_manuais.pack_forget()
                
        self.menu_filtro = ctk.CTkComboBox(frame_filtros, variable=self.opcao_filtro, values=["Últimas 48 Horas", "Sessão Atual (Desde que abriu)", "Apenas Hoje", "Todo o Histórico", "Data Específica"], command=alternar_campos_data, **MENU_RELATORIO)
        self.menu_filtro.pack(pady=5, padx=20, fill="x")
        
        self.frame_datas_manuais = ctk.CTkFrame(frame_filtros, fg_color="transparent")
        ctk.CTkLabel(self.frame_datas_manuais, text="Início:").grid(row=0, column=0, padx=2)
        self.input_data_inicio = ctk.CTkEntry(self.frame_datas_manuais, width=95, placeholder_text="DD/MM/AAAA")
        self.input_data_inicio.grid(row=0, column=1, padx=2)
        self.input_data_inicio.bind("<KeyRelease>", lambda e: self.aplicar_mascara_data(e, self.input_data_inicio))
        ctk.CTkLabel(self.frame_datas_manuais, text="Fim:").grid(row=0, column=2, padx=2)
        self.input_data_fim = ctk.CTkEntry(self.frame_datas_manuais, width=95, placeholder_text="DD/MM/AAAA")
        self.input_data_fim.grid(row=0, column=3, padx=2)
        self.input_data_fim.bind("<KeyRelease>", lambda e: self.aplicar_mascara_data(e, self.input_data_fim))
        
        self.frame_grafico = ctk.CTkFrame(self.aba_relatorio, height=180, fg_color="transparent")
        self.frame_grafico.pack(side="top", pady=5, padx=10, fill="x")
        self.grafico = GraficoProducao(self.frame_grafico)


        frame_tabela = ctk.CTkFrame(self.aba_relatorio)
        frame_tabela.pack(side="top", pady=10, padx=10, fill="both", expand=True)
        
        colunas = ("ID", "Cor", "Face", "Status", "Data/Hora")
        self.tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")
        for col in colunas: self.tabela.heading(col, text=col)
        self.tabela.column("ID", width=40, anchor="center"); self.tabela.column("Cor", width=100, anchor="center"); self.tabela.column("Face", width=50, anchor="center")
        self.tabela.column("Status", width=90, anchor="center"); self.tabela.column("Data/Hora", width=140, anchor="center")
        
        scrollbar = ctk.CTkScrollbar(frame_tabela, orientation="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y"); self.tabela.pack(side="left", fill="both", expand=True)


        # ==========================================
        # --- ABA 3: CONFIGURAÇÕES AVANÇADAS ---
        # ==========================================
        ctk.CTkLabel(self.aba_config, text="CONFIGURAÇÕES OPERACIONAIS", font=("Arial", 24, "bold")).pack(pady=15)
        
        frame_cam_config = ctk.CTkFrame(self.aba_config, fg_color="#1E1E1E", border_width=2, border_color="#3A7EB8", corner_radius=8)
        frame_cam_config.pack(pady=15, padx=30, fill="x")
        ctk.CTkLabel(frame_cam_config, text="Seletor de Câmera Ativa (Hardware)", font=("Arial", 14, "bold"), text_color="white").pack(pady=(10, 5))
        
        self.menu_camera = ctk.CTkOptionMenu(frame_cam_config, values=["0", "1", "2"], command=self.controlador.alterar_camera, **MENU_PRODUTOS)
        self.menu_camera.set("0")
        self.menu_camera.pack(pady=(5, 15), padx=20, fill="x")
        
        frame_perigo = ctk.CTkFrame(self.aba_config, fg_color="#2B1B1B", border_width=2, border_color="#780000", corner_radius=8)
        frame_perigo.pack(pady=25, padx=30, fill="x")
        ctk.CTkLabel(frame_perigo, text="⚠️ ZONA DE PERIGO CRÍTICO ⚠️", font=("Arial", 14, "bold"), text_color="red").pack(pady=(10, 5))
        ctk.CTkLabel(frame_perigo, text="Atenção: A ação abaixo apagará permanentemente o histórico do MySQL.", font=("Arial", 11), text_color="white").pack(pady=2)
        botao_limpar = ctk.CTkButton(frame_perigo, text="LIMPAR BASE DE DADOS", font=("Arial", 14, "bold"), fg_color="#780000", hover_color="#5c0000", height=40, command=self.controlador.solicitar_limpeza_banco)
        botao_limpar.pack(pady=(10, 15), padx=20, fill="x")

        # --- BOTÃO DE CRÉDITOS E REDES SOCIAIS ADICIONADO AQUI ---
        botao_sobre = ctk.CTkButton(self.aba_config, text="ℹ️ Sobre o Criador", font=("Arial", 14, "bold"), fg_color="transparent", border_width=2, text_color="white", command=lambda: JanelaSobre(self.janela))
        botao_sobre.pack(pady=30, side="bottom")

    def aplicar_mascara_data(self, event, entry):
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right'): return
        texto = entry.get()
        numeros = "".join(filter(str.isdigit, texto)) 
        resultado = ""
        for i, num in enumerate(numeros):
            if i == 2 or i == 4: resultado += "/"
            resultado += num
        if texto != resultado[:10]:
            entry.delete(0, 'end'); entry.insert(0, resultado[:10])

    def coletar_listas_permitidas(self):
        cores, numeros = [], []
        if self.var_vermelho.get(): cores.append("VERMELHO")
        if self.var_verde.get(): cores.append("VERDE")
        if self.var_azul.get(): cores.append("AZUL")
        if self.var_amarelo.get(): cores.append("AMARELO")
        if self.var_1.get(): numeros.append(1)
        if self.var_2.get(): numeros.append(2)
        if self.var_3.get(): numeros.append(3)
        if self.var_4.get(): numeros.append(4)
        if self.var_5.get(): numeros.append(5)
        if self.var_6.get(): numeros.append(6)
        return cores, numeros

    def liberar_acesso(self, perfil):
        if perfil == "operador":
            for cb in self.lista_todas_checkboxes: cb.configure(state="disabled")
            self.abas.delete(self.NOME_ABA_2) 
            self.abas.delete(self.NOME_ABA_3) 
        self.login.fechar_e_liberar() 

    def mostrar_erro_login(self, msg): 
        self.login.mostrar_erro(msg) 
        
    def atualizar_relogio_interface(self, hora_str): self.label_relogio.configure(text=f"🕒 Hora: {hora_str}")
    def atualizar_uptime_interface(self, uptime_str): self.label_uptime.configure(text=f"⏳ Operação: {uptime_str}")
    def atualizar_camera(self, imagem_pil): self.tela_video.configure(image=ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=(800, 600)))
    def atualizar_contadores(self, aprovados, rejeitados): self.texto_aprovados.configure(text=str(aprovados)); self.texto_rejeitados.configure(text=str(rejeitados))
    def atualizar_historico_visual(self, historico_pecas):
        texto = ""
        for item in historico_pecas: texto += f"{item}\n"
        self.label_historico.configure(text=texto.strip())

    def aba_relatorio_ativa(self):
        try: return self.abas.get() == self.NOME_ABA_2
        except: return False

    def get_valores_filtro(self): return self.opcao_filtro.get(), self.input_data_inicio.get(), self.input_data_fim.get()

    def atualizar_tabela(self, sucesso, dados):
        for linha in self.tabela.get_children(): self.tabela.delete(linha)
        aprovados, rejeitados = 0, 0
        if sucesso and isinstance(dados, list) and len(dados) > 0:
            for item in dados: 
                self.tabela.insert("", "end", values=item)
                if item[3] == "APROVADO": aprovados += 1
                else: rejeitados += 1
            self.texto_feedback.configure(text=f"A mostrar {len(dados)} registos.", text_color="white")
        else:
            self.texto_feedback.configure(text="Nenhum dado encontrado.", text_color="yellow")
            
        self.grafico.atualizar(aprovados, rejeitados)

    def mostrar_feedback_exportacao(self, sucesso, msg, qtd, formato="PDF"):
        if sucesso: self.texto_feedback.configure(text=f"✅ {formato} Salvo! ({qtd} peças)", text_color="#00FF00")
        else: self.texto_feedback.configure(text=f"❌ Erro ao exportar:\n{msg}", text_color="red")