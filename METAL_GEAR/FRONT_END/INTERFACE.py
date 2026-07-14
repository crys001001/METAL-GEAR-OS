import customtkinter as ctk
from tkinter import ttk

from FRONT_END.UI_ESTILOS import (
    aplicar_tema_tabela,
    MENU_PRODUTOS,
    MENU_RELATORIO,
    CHECKBOX,
    CORES,
    FONTE,
)
from FRONT_END.UI_LOGIN import JanelaLogin
from FRONT_END.UI_GRAFICO import GraficoProducao
from FRONT_END.UI_SOBRE import JanelaSobre


class TelaMetalGear:
    def __init__(self, janela, controlador):
        self.janela = janela
        self.controlador = controlador

        self.NOME_ABA_1 = "  PAINEL  "
        self.NOME_ABA_2 = "  RELATÓRIOS  "
        self.NOME_ABA_3 = "  CONFIGURAÇÕES  "

        aplicar_tema_tabela()
        self.construir_tela_principal()
        self.login = JanelaLogin(self.janela, self.controlador)

    @staticmethod
    def _cartao(pai, borda=None, cor=None, raio=14):
        return ctk.CTkFrame(
            pai,
            fg_color=cor or CORES["cartao"],
            border_width=1,
            border_color=borda or CORES["borda"],
            corner_radius=raio,
        )

    @staticmethod
    def _titulo_secao(pai, titulo, subtitulo=None):
        ctk.CTkLabel(
            pai,
            text=titulo,
            font=(FONTE, 14, "bold"),
            text_color=CORES["texto_secundario"],
            anchor="w",
        ).pack(fill="x", padx=13, pady=(7, 1))
        if subtitulo:
            ctk.CTkLabel(
                pai,
                text=subtitulo,
                font=(FONTE, 12),
                text_color=CORES["texto_secundario"],
                anchor="w",
            ).pack(fill="x", padx=13, pady=(0, 5))

    def construir_tela_principal(self):
        self.janela.configure(fg_color=CORES["fundo"])
        self.janela.grid_columnconfigure(0, weight=7, uniform="layout")
        self.janela.grid_columnconfigure(1, weight=4, uniform="layout")
        self.janela.grid_rowconfigure(0, weight=1)

        # PAINEL DA CÂMERA
        self.frame_camera = ctk.CTkFrame(
            self.janela,
            corner_radius=16,
            fg_color=CORES["painel"],
            border_width=1,
            border_color=CORES["borda"],
        )
        self.frame_camera.grid(
            row=0,
            column=0,
            padx=(12, 6),
            pady=12,
            sticky="nsew",
        )
        self.frame_camera.grid_columnconfigure(0, weight=1)
        self.frame_camera.grid_rowconfigure(1, weight=1)

        cabecalho = ctk.CTkFrame(
            self.frame_camera,
            fg_color="transparent",
            height=62,
        )
        cabecalho.grid(row=0, column=0, padx=18, pady=(9, 3), sticky="ew")
        cabecalho.grid_columnconfigure(0, weight=1)

        bloco_titulo = ctk.CTkFrame(cabecalho, fg_color="transparent")
        bloco_titulo.grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            bloco_titulo,
            text="METAL GEAR VISION",
            font=(FONTE, 24, "bold"),
            text_color=CORES["texto"],
            anchor="w",
        ).pack(anchor="w")
        ctk.CTkLabel(
            bloco_titulo,
            text="INSPEÇÃO ÓPTICA  •  LINHA 01",
            font=(FONTE, 12, "bold"),
            text_color=CORES["texto_secundario"],
            anchor="w",
        ).pack(anchor="w", pady=(1, 0))

        self.label_live_camera = ctk.CTkLabel(
            cabecalho,
            text="●  LIVE",
            width=84,
            height=28,
            corner_radius=15,
            fg_color="#16271E",
            text_color=CORES["verde"],
            font=(FONTE, 11, "bold"),
        )
        self.label_live_camera.grid(row=0, column=1, padx=(10, 0), sticky="e")

        self.frame_video = ctk.CTkFrame(
            self.frame_camera,
            fg_color="#0B0E13",
            border_width=1,
            border_color="#302B42",
            corner_radius=14,
        )
        self.frame_video.grid(
            row=1,
            column=0,
            padx=14,
            pady=6,
            sticky="nsew",
        )
        self.frame_video.grid_columnconfigure(0, weight=1)
        self.frame_video.grid_rowconfigure(0, weight=1)

        self.tela_video = ctk.CTkLabel(
            self.frame_video,
            text="INICIALIZANDO CÂMERA...",
            font=(FONTE, 14, "bold"),
            text_color=CORES["texto_secundario"],
            fg_color="#0B0E13",
        )
        self.tela_video.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        rodape = ctk.CTkFrame(
            self.frame_camera,
            fg_color="transparent",
            height=38,
        )
        rodape.grid(row=2, column=0, padx=18, pady=(2, 8), sticky="ew")
        rodape.grid_columnconfigure(0, weight=1)

        self.label_relogio = ctk.CTkLabel(
            rodape,
            text="HORÁRIO  00:00:00",
            font=(FONTE, 10, "bold"),
            text_color=CORES["ciano"],
        )
        self.label_relogio.grid(row=0, column=0, sticky="w")

        self.label_uptime = ctk.CTkLabel(
            rodape,
            text="SESSÃO  00h 00m 00s",
            font=(FONTE, 10, "bold"),
            text_color=CORES["texto_secundario"],
        )
        self.label_uptime.grid(row=0, column=1, sticky="e")

        # PAINEL LATERAL
        def quando_mudar_aba():
            if self.abas.get() == self.NOME_ABA_2:
                self.controlador.carregar_dados_na_tabela()

        self.abas = ctk.CTkTabview(
            self.janela,
            command=quando_mudar_aba,
            fg_color=CORES["painel"],
            segmented_button_fg_color=CORES["cartao"],
            segmented_button_selected_color=CORES["azul_escuro"],
            segmented_button_selected_hover_color=CORES["azul"],
            segmented_button_unselected_color=CORES["cartao"],
            segmented_button_unselected_hover_color=CORES["cartao_2"],
            border_width=1,
            border_color=CORES["borda"],
            corner_radius=16,
        )
        self.abas.grid(
            row=0,
            column=1,
            padx=(6, 12),
            pady=12,
            sticky="nsew",
        )
        self.abas._segmented_button.configure(font=(FONTE, 13, "bold"))

        self.aba_controle = self.abas.add(self.NOME_ABA_1)
        self.aba_relatorio = self.abas.add(self.NOME_ABA_2)
        self.aba_config = self.abas.add(self.NOME_ABA_3)

        self._construir_aba_controle()
        self._construir_aba_relatorios()
        self._construir_aba_configuracoes()

    def _construir_aba_controle(self):
        # Layout compacto: todos os cartões permanecem visíveis sem rolagem.
        frame_acoes = ctk.CTkFrame(self.aba_controle, fg_color="transparent")
        frame_acoes.pack(side="bottom", fill="x", padx=7, pady=(4, 7))

        self.botao_pausa = ctk.CTkButton(
            frame_acoes,
            text="PAUSAR INSPEÇÃO",
            fg_color="#B7791F",
            hover_color="#8A5E12",
            font=(FONTE, 13, "bold"),
            height=37,
            corner_radius=9,
            command=self.controlador.alternar_pausa,
        )
        self.botao_pausa.pack(fill="x", pady=(0, 4))

        self.botao_emergencia = ctk.CTkButton(
            frame_acoes,
            text="PARADA DE EMERGÊNCIA",
            fg_color=CORES["vermelho"],
            hover_color=CORES["vermelho_escuro"],
            font=(FONTE, 14, "bold"),
            height=42,
            corner_radius=9,
            command=self.controlador.acionar_emergencia,
        )
        self.botao_emergencia.pack(fill="x")

        painel = ctk.CTkFrame(self.aba_controle, fg_color="transparent")
        painel.pack(side="top", fill="both", expand=True, padx=1)

        # Regras do lote
        frame_regras = self._cartao(painel, borda="#4A3D74", raio=12)
        frame_regras.pack(pady=(4, 3), padx=7, fill="x")
        self._titulo_secao(frame_regras, "REGRAS DO LOTE")

        regras_salvas = self.controlador.config.get(
            "regras",
            {
                "cores": ["VERMELHO", "VERDE", "AZUL"],
                "numeros": [1, 2, 3, 4, 5, 6],
            },
        )
        cores_mem = regras_salvas.get("cores", [])
        num_mem = regras_salvas.get("numeros", [])

        grade_cores = ctk.CTkFrame(frame_regras, fg_color="transparent")
        grade_cores.pack(fill="x", padx=13, pady=(0, 5))
        grade_cores.grid_columnconfigure((0, 1, 2), weight=1)

        self.var_vermelho = ctk.BooleanVar(value="VERMELHO" in cores_mem)
        self.var_verde = ctk.BooleanVar(value="VERDE" in cores_mem)
        self.var_azul = ctk.BooleanVar(value="AZUL" in cores_mem)

        self.cb_vermelho = ctk.CTkCheckBox(
            grade_cores,
            text="Vermelho",
            variable=self.var_vermelho,
            command=self.controlador.aplicar_regras_dinamicas,
            **CHECKBOX,
        )
        self.cb_verde = ctk.CTkCheckBox(
            grade_cores,
            text="Verde",
            variable=self.var_verde,
            command=self.controlador.aplicar_regras_dinamicas,
            **CHECKBOX,
        )
        self.cb_azul = ctk.CTkCheckBox(
            grade_cores,
            text="Azul",
            variable=self.var_azul,
            command=self.controlador.aplicar_regras_dinamicas,
            **CHECKBOX,
        )
        self.cb_vermelho.grid(row=0, column=0, padx=3, pady=2, sticky="w")
        self.cb_verde.grid(row=0, column=1, padx=3, pady=2, sticky="w")
        self.cb_azul.grid(row=0, column=2, padx=3, pady=2, sticky="w")

        ctk.CTkLabel(
            frame_regras,
            text="FACES PERMITIDAS",
            font=(FONTE, 11, "bold"),
            text_color=CORES["texto_secundario"],
        ).pack(anchor="w", padx=13, pady=(1, 0))

        grade_numeros = ctk.CTkFrame(frame_regras, fg_color="transparent")
        grade_numeros.pack(fill="x", padx=13, pady=(0, 7))
        grade_numeros.grid_columnconfigure(tuple(range(6)), weight=1)

        checkboxes = []
        for numero in range(1, 7):
            variavel = ctk.BooleanVar(value=numero in num_mem)
            checkbox = ctk.CTkCheckBox(
                grade_numeros,
                text=str(numero),
                variable=variavel,
                command=self.controlador.aplicar_regras_dinamicas,
                **CHECKBOX,
            )
            checkbox.grid(row=0, column=numero - 1, padx=1, pady=2)
            setattr(self, f"var_{numero}", variavel)
            setattr(self, f"cb_{numero}", checkbox)
            checkboxes.append(checkbox)

        self.lista_todas_checkboxes = [
            self.cb_vermelho,
            self.cb_verde,
            self.cb_azul,
            *checkboxes,
        ]

        # Saúde dos serviços
        frame_status = self._cartao(painel, raio=12)
        frame_status.pack(pady=3, padx=7, fill="x")
        self._titulo_secao(frame_status, "SAÚDE DO SISTEMA")

        grade_status = ctk.CTkFrame(frame_status, fg_color="transparent")
        grade_status.pack(fill="x", padx=9, pady=(0, 7))
        grade_status.grid_columnconfigure((0, 1, 2), weight=1, uniform="status")

        self.label_status_camera = self._criar_chip_status(
            grade_status, "CÂMERA", 0
        )
        self.label_status_api = self._criar_chip_status(
            grade_status, "API / BANCO", 1
        )
        self.label_status_inspecao = self._criar_chip_status(
            grade_status, "INSPEÇÃO", 2
        )

        # Peça atual
        self.frame_peca = self._cartao(
            painel, borda="#5A4686", cor="#131822", raio=12
        )
        self.frame_peca.pack(pady=3, padx=7, fill="x")
        self._titulo_secao(self.frame_peca, "PEÇA ATUAL")

        self.label_peca_atual = ctk.CTkLabel(
            self.frame_peca,
            text="AGUARDANDO PEÇA",
            font=(FONTE, 18, "bold"),
            text_color=CORES["texto"],
            justify="left",
            anchor="w",
            wraplength=430,
        )
        self.label_peca_atual.pack(fill="x", padx=13, pady=(0, 1))

        self.label_mensagem_peca = ctk.CTkLabel(
            self.frame_peca,
            text="Posicione uma peça dentro da zona de inspeção.",
            font=(FONTE, 13),
            text_color=CORES["texto_secundario"],
            justify="left",
            anchor="w",
            wraplength=430,
        )
        self.label_mensagem_peca.pack(fill="x", padx=13, pady=(0, 4))

        linha_progresso = ctk.CTkFrame(self.frame_peca, fg_color="transparent")
        linha_progresso.pack(fill="x", padx=13)
        self.label_progresso = ctk.CTkLabel(
            linha_progresso,
            text="PROGRESSO  0%",
            font=(FONTE, 10, "bold"),
            text_color=CORES["texto_secundario"],
        )
        self.label_progresso.pack(side="left")
        self.barra_progresso = ctk.CTkProgressBar(
            self.frame_peca,
            height=5,
            corner_radius=3,
            fg_color="#25293A",
            progress_color=CORES["azul"],
        )
        self.barra_progresso.pack(fill="x", padx=13, pady=(1, 4))
        self.barra_progresso.set(0)

        linha_confianca = ctk.CTkFrame(self.frame_peca, fg_color="transparent")
        linha_confianca.pack(fill="x", padx=13)
        self.label_confianca = ctk.CTkLabel(
            linha_confianca,
            text="CONFIANÇA  0%",
            font=(FONTE, 10, "bold"),
            text_color=CORES["texto_secundario"],
        )
        self.label_confianca.pack(side="left")
        self.barra_confianca = ctk.CTkProgressBar(
            self.frame_peca,
            height=5,
            corner_radius=3,
            fg_color="#25293A",
            progress_color=CORES["verde"],
        )
        self.barra_confianca.pack(fill="x", padx=13, pady=(1, 7))
        self.barra_confianca.set(0)

        # Métricas compactas
        frame_metricas = ctk.CTkFrame(painel, fg_color="transparent")
        frame_metricas.pack(pady=3, padx=7, fill="x")
        frame_metricas.grid_columnconfigure((0, 1), weight=1, uniform="metricas")

        card_aprovados = self._cartao(
            frame_metricas, borda="#206545", cor="#0F221B", raio=12
        )
        card_aprovados.grid(row=0, column=0, padx=(0, 3), sticky="nsew")
        ctk.CTkLabel(
            card_aprovados,
            text="APROVADOS",
            font=(FONTE, 11, "bold"),
            text_color="#86EFAC",
        ).pack(pady=(7, 0))
        self.texto_aprovados = ctk.CTkLabel(
            card_aprovados,
            text="0",
            font=(FONTE, 28, "bold"),
            text_color=CORES["texto"],
        )
        self.texto_aprovados.pack()
        self.percentual_aprovados = ctk.CTkLabel(
            card_aprovados,
            text="0% DO CICLO",
            font=(FONTE, 10, "bold"),
            text_color="#86EFAC",
        )
        self.percentual_aprovados.pack(pady=(0, 6))

        card_rejeitados = self._cartao(
            frame_metricas, borda="#8B2434", cor="#2A131A", raio=12
        )
        card_rejeitados.grid(row=0, column=1, padx=(3, 0), sticky="nsew")
        ctk.CTkLabel(
            card_rejeitados,
            text="REJEITADOS",
            font=(FONTE, 11, "bold"),
            text_color="#FDA4AF",
        ).pack(pady=(7, 0))
        self.texto_rejeitados = ctk.CTkLabel(
            card_rejeitados,
            text="0",
            font=(FONTE, 28, "bold"),
            text_color=CORES["texto"],
        )
        self.texto_rejeitados.pack()
        self.percentual_rejeitados = ctk.CTkLabel(
            card_rejeitados,
            text="0% DO CICLO",
            font=(FONTE, 10, "bold"),
            text_color="#FDA4AF",
        )
        self.percentual_rejeitados.pack(pady=(0, 6))

        # Histórico curto: tamanho fixo e legível em janela reduzida.
        frame_historico = self._cartao(painel, raio=12)
        frame_historico.configure(height=112)
        frame_historico.pack(pady=(3, 4), padx=7, fill="x", expand=False)
        frame_historico.pack_propagate(False)
        self._titulo_secao(frame_historico, "ÚLTIMAS INSPEÇÕES")
        self.label_historico = ctk.CTkLabel(
            frame_historico,
            text="Nenhuma peça processada nesta sessão.",
            font=(FONTE, 13),
            text_color=CORES["texto_secundario"],
            justify="left",
            anchor="nw",
            height=62,
        )
        self.label_historico.pack(
            fill="both", expand=True, padx=13, pady=(0, 7)
        )

    def _criar_chip_status(self, pai, titulo, coluna):
        card = ctk.CTkFrame(
            pai,
            fg_color=CORES["cartao_2"],
            corner_radius=9,
            border_width=1,
            border_color=CORES["borda"],
        )
        card.grid(row=0, column=coluna, padx=2, sticky="nsew")
        ctk.CTkLabel(
            card,
            text=titulo,
            font=(FONTE, 10, "bold"),
            text_color=CORES["texto_secundario"],
        ).pack(pady=(5, 0))
        label = ctk.CTkLabel(
            card,
            text="● OFFLINE",
            font=(FONTE, 11, "bold"),
            text_color=CORES["vermelho"],
        )
        label.pack(pady=(0, 5))
        return label

    def _construir_aba_relatorios(self):
        # Grid responsivo: a tabela reduz de altura antes de ocultar os botões.
        self.aba_relatorio.grid_columnconfigure(0, weight=1)
        self.aba_relatorio.grid_rowconfigure(3, weight=1, minsize=170)

        cabecalho = ctk.CTkFrame(self.aba_relatorio, fg_color="transparent")
        cabecalho.grid(row=0, column=0, sticky="ew", padx=9, pady=(5, 2))
        ctk.CTkLabel(
            cabecalho,
            text="CENTRO DE DADOS",
            font=(FONTE, 24, "bold"),
            text_color=CORES["texto"],
        ).pack(anchor="w")
        ctk.CTkLabel(
            cabecalho,
            text="Histórico centralizado no MariaDB através da Metal Gear API.",
            font=(FONTE, 11),
            text_color=CORES["texto_secundario"],
        ).pack(anchor="w")

        frame_filtros = self._cartao(self.aba_relatorio, raio=12)
        frame_filtros.grid(row=1, column=0, sticky="ew", pady=4, padx=9)
        self._titulo_secao(frame_filtros, "PERÍODO DE ANÁLISE")

        self.opcao_filtro = ctk.StringVar(value="Últimas 48 Horas")

        def alternar_campos_data(escolha):
            if escolha == "Data Específica":
                self.frame_datas_manuais.pack(pady=(0, 7))
            else:
                self.frame_datas_manuais.pack_forget()

        self.menu_filtro = ctk.CTkComboBox(
            frame_filtros,
            variable=self.opcao_filtro,
            values=[
                "Últimas 48 Horas",
                "Sessão Atual (Desde que abriu)",
                "Apenas Hoje",
                "Todo o Histórico",
                "Data Específica",
            ],
            command=alternar_campos_data,
            height=34,
            **MENU_RELATORIO,
        )
        self.menu_filtro.pack(pady=(2, 7), padx=13, fill="x")

        self.frame_datas_manuais = ctk.CTkFrame(
            frame_filtros, fg_color="transparent"
        )
        self.frame_datas_manuais.grid_columnconfigure((1, 3), weight=1)
        ctk.CTkLabel(
            self.frame_datas_manuais,
            text="Início",
            font=(FONTE, 11, "bold"),
            text_color=CORES["texto_secundario"],
        ).grid(row=0, column=0, padx=(0, 4))
        self.input_data_inicio = ctk.CTkEntry(
            self.frame_datas_manuais,
            width=105,
            height=28,
            placeholder_text="DD/MM/AAAA",
            fg_color=CORES["cartao_2"],
            border_color=CORES["borda"],
        )
        self.input_data_inicio.grid(row=0, column=1, padx=(0, 7), sticky="ew")
        self.input_data_inicio.bind(
            "<KeyRelease>",
            lambda evento: self.aplicar_mascara_data(
                evento, self.input_data_inicio
            ),
        )
        ctk.CTkLabel(
            self.frame_datas_manuais,
            text="Fim",
            font=(FONTE, 11, "bold"),
            text_color=CORES["texto_secundario"],
        ).grid(row=0, column=2, padx=(0, 4))
        self.input_data_fim = ctk.CTkEntry(
            self.frame_datas_manuais,
            width=105,
            height=28,
            placeholder_text="DD/MM/AAAA",
            fg_color=CORES["cartao_2"],
            border_color=CORES["borda"],
        )
        self.input_data_fim.grid(row=0, column=3, sticky="ew")
        self.input_data_fim.bind(
            "<KeyRelease>",
            lambda evento: self.aplicar_mascara_data(evento, self.input_data_fim),
        )

        self.frame_grafico = ctk.CTkFrame(
            self.aba_relatorio, height=118, fg_color="transparent"
        )
        self.frame_grafico.grid(row=2, column=0, sticky="ew", pady=2, padx=9)
        self.frame_grafico.grid_propagate(False)
        self.grafico = GraficoProducao(self.frame_grafico)

        self.frame_tabela_relatorio = self._cartao(self.aba_relatorio, raio=12)
        self.frame_tabela_relatorio.grid(
            row=3, column=0, sticky="nsew", pady=4, padx=9
        )

        colunas = ("ID", "Cor", "Face", "Status", "Data/Hora")
        self.tabela = ttk.Treeview(
            self.frame_tabela_relatorio, columns=colunas, show="headings"
        )
        for coluna in colunas:
            self.tabela.heading(coluna, text=coluna.upper())
        self.tabela.column("ID", width=38, anchor="center")
        self.tabela.column("Cor", width=74, anchor="center")
        self.tabela.column("Face", width=48, anchor="center")
        self.tabela.column("Status", width=82, anchor="center")
        self.tabela.column("Data/Hora", width=128, anchor="center")

        scrollbar = ctk.CTkScrollbar(
            self.frame_tabela_relatorio, orientation="vertical", command=self.tabela.yview
        )
        self.tabela.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y", padx=(0, 5), pady=6)
        self.tabela.pack(side="left", fill="both", expand=True, padx=6, pady=6)

        frame_botoes = ctk.CTkFrame(self.aba_relatorio, fg_color="transparent")
        frame_botoes.grid(row=4, column=0, sticky="ew", padx=9, pady=(2, 1))
        frame_botoes.grid_columnconfigure((0, 1, 2), weight=1, uniform="acoes")

        ctk.CTkButton(
            frame_botoes,
            text="ATUALIZAR",
            font=(FONTE, 12, "bold"),
            fg_color=CORES["azul_escuro"],
            hover_color=CORES["azul"],
            height=32,
            command=self.controlador.carregar_dados_na_tabela,
        ).grid(row=0, column=0, padx=(0, 3), sticky="ew")
        ctk.CTkButton(
            frame_botoes,
            text="GERAR PDF",
            font=(FONTE, 13, "bold"),
            fg_color=CORES["vermelho_escuro"],
            hover_color=CORES["vermelho"],
            height=32,
            command=self.controlador.solicitar_pdf,
        ).grid(row=0, column=1, padx=3, sticky="ew")
        ctk.CTkButton(
            frame_botoes,
            text="EXPORTAR CSV",
            font=(FONTE, 12, "bold"),
            fg_color=CORES["verde_escuro"],
            hover_color=CORES["verde"],
            height=32,
            command=self.controlador.solicitar_csv,
        ).grid(row=0, column=2, padx=(3, 0), sticky="ew")

        self.texto_feedback = ctk.CTkLabel(
            self.aba_relatorio,
            text="Tabela sincronizada.",
            font=(FONTE, 11),
            text_color=CORES["texto_secundario"],
        )
        self.texto_feedback.grid(row=5, column=0, pady=(1, 4))

        self.aba_relatorio.bind(
            "<Configure>", self._ajustar_relatorio_responsivo
        )
        self.aba_relatorio.after(120, self._ajustar_relatorio_responsivo)

    def _ajustar_relatorio_responsivo(self, evento=None):
        """Em altura reduzida, prioriza tabela e botões em vez do gráfico."""
        try:
            altura = (
                evento.height
                if evento is not None
                else self.aba_relatorio.winfo_height()
            )
            largura = (
                evento.width
                if evento is not None
                else self.aba_relatorio.winfo_width()
            )
            compacto = altura < 700 or largura < 460

            if compacto:
                self.frame_grafico.grid_remove()
            else:
                self.frame_grafico.grid(
                    row=2, column=0, sticky="ew", pady=2, padx=9
                )
        except Exception:
            pass

    def _construir_aba_configuracoes(self):
        ctk.CTkLabel(
            self.aba_config,
            text="CONFIGURAÇÕES OPERACIONAIS",
            font=(FONTE, 24, "bold"),
            text_color=CORES["texto"],
        ).pack(anchor="w", padx=16, pady=(16, 3))
        ctk.CTkLabel(
            self.aba_config,
            text="Hardware, visão e ações administrativas.",
            font=(FONTE, 12),
            text_color=CORES["texto_secundario"],
        ).pack(anchor="w", padx=16, pady=(0, 10))

        frame_cam = self._cartao(self.aba_config)
        frame_cam.pack(pady=7, padx=16, fill="x")
        self._titulo_secao(frame_cam, "CÂMERA ATIVA")
        self.menu_camera = ctk.CTkOptionMenu(
            frame_cam,
            values=["0", "1", "2"],
            command=self.controlador.alterar_camera,
            **MENU_PRODUTOS,
        )
        self.menu_camera.set("0")
        self.menu_camera.pack(pady=(3, 14), padx=16, fill="x")

        visao = self.controlador.config.get("visao", {})
        frame_visao = self._cartao(self.aba_config, borda="#4D5F72")
        frame_visao.pack(pady=7, padx=16, fill="x")
        self._titulo_secao(frame_visao, "PERFIL DE VISÃO")
        resumo = (
            f'{visao.get("frames_confirmacao", 12)} frames de confirmação  •  '
            f'{float(visao.get("confianca_minima", 0.75)):.0%} de confiança mínima\n'
            f'Área mínima {visao.get("area_minima", 1800)} px  •  '
            f'{visao.get("frames_vazio_liberacao", 8)} frames para liberar novo ciclo'
        )
        ctk.CTkLabel(
            frame_visao,
            text=resumo,
            font=(FONTE, 13),
            text_color=CORES["texto_secundario"],
            justify="left",
            anchor="w",
        ).pack(fill="x", padx=16, pady=(2, 14))

        frame_perigo = self._cartao(
            self.aba_config, borda="#7E2935", cor="#251317"
        )
        frame_perigo.pack(pady=12, padx=16, fill="x")
        self._titulo_secao(
            frame_perigo,
            "ZONA ADMINISTRATIVA CRÍTICA",
            "A ação abaixo remove todo o histórico armazenado no servidor.",
        )
        ctk.CTkButton(
            frame_perigo,
            text="LIMPAR BASE DE DADOS",
            font=(FONTE, 13, "bold"),
            fg_color=CORES["vermelho_escuro"],
            hover_color=CORES["vermelho"],
            height=40,
            command=self.controlador.solicitar_limpeza_banco,
        ).pack(pady=(3, 14), padx=16, fill="x")

        ctk.CTkButton(
            self.aba_config,
            text="SOBRE O CRIADOR",
            font=(FONTE, 12, "bold"),
            fg_color="transparent",
            border_width=1,
            border_color=CORES["borda"],
            text_color=CORES["texto_secundario"],
            command=lambda: JanelaSobre(self.janela),
        ).pack(pady=18, padx=16, side="bottom", fill="x")

    def aplicar_mascara_data(self, event, entry):
        if event.keysym in ("BackSpace", "Delete", "Left", "Right"):
            return
        texto = entry.get()
        numeros = "".join(filter(str.isdigit, texto))
        resultado = ""
        for indice, numero in enumerate(numeros):
            if indice in (2, 4):
                resultado += "/"
            resultado += numero
        if texto != resultado[:10]:
            entry.delete(0, "end")
            entry.insert(0, resultado[:10])

    def coletar_listas_permitidas(self):
        cores = []
        numeros = []
        if self.var_vermelho.get():
            cores.append("VERMELHO")
        if self.var_verde.get():
            cores.append("VERDE")
        if self.var_azul.get():
            cores.append("AZUL")
        for numero in range(1, 7):
            if getattr(self, f"var_{numero}").get():
                numeros.append(numero)
        return cores, numeros

    def liberar_acesso(self, perfil):
        if perfil == "operador":
            for checkbox in self.lista_todas_checkboxes:
                checkbox.configure(state="disabled")
            self.abas.delete(self.NOME_ABA_2)
            self.abas.delete(self.NOME_ABA_3)
        self.login.fechar_e_liberar()

    def mostrar_erro_login(self, msg):
        self.login.mostrar_erro(msg)

    def atualizar_relogio_interface(self, hora_str):
        self.label_relogio.configure(text=f"HORÁRIO  {hora_str}")

    def atualizar_uptime_interface(self, uptime_str):
        self.label_uptime.configure(text=f"SESSÃO  {uptime_str}")

    def atualizar_fps(self, fps):
        # Mantido por compatibilidade com o controlador; indicador oculto na UI.
        return None

    def atualizar_camera(self, imagem_pil):
        largura_widget = max(640, self.tela_video.winfo_width() - 10)
        altura_widget = max(420, self.tela_video.winfo_height() - 10)
        largura_original, altura_original = imagem_pil.size
        escala = min(
            largura_widget / max(1, largura_original),
            altura_widget / max(1, altura_original),
        )
        largura = max(320, int(largura_original * escala))
        altura = max(240, int(altura_original * escala))
        imagem = ctk.CTkImage(
            light_image=imagem_pil,
            dark_image=imagem_pil,
            size=(largura, altura),
        )
        self.tela_video.configure(image=imagem, text="")
        self.tela_video.image = imagem

    def atualizar_contadores(self, aprovados, rejeitados):
        self.texto_aprovados.configure(text=str(aprovados))
        self.texto_rejeitados.configure(text=str(rejeitados))
        total = aprovados + rejeitados
        p_aprovados = (aprovados / total * 100) if total else 0
        p_rejeitados = (rejeitados / total * 100) if total else 0
        self.percentual_aprovados.configure(text=f"{p_aprovados:.0f}% DO CICLO")
        self.percentual_rejeitados.configure(text=f"{p_rejeitados:.0f}% DO CICLO")

    def atualizar_historico_visual(self, historico_pecas):
        if not historico_pecas:
            self.label_historico.configure(
                text="Nenhuma peça processada nesta sessão."
            )
            return
        itens = historico_pecas[:3]
        self.label_historico.configure(text="\n".join(itens))

    def atualizar_status_camera(self, online):
        if online:
            self.label_status_camera.configure(
                text="● ONLINE", text_color=CORES["verde"]
            )
            self.label_live_camera.configure(
                text="●  LIVE", fg_color="#16271E", text_color=CORES["verde"]
            )
        else:
            self.label_status_camera.configure(
                text="● OFFLINE", text_color=CORES["vermelho"]
            )
            self.label_live_camera.configure(
                text="●  OFFLINE",
                fg_color="#34131A",
                text_color=CORES["vermelho"],
            )

    def atualizar_status_api(self, online):
        self.label_status_api.configure(
            text="● ONLINE" if online else "● OFFLINE",
            text_color=CORES["verde"] if online else CORES["vermelho"],
        )

    def atualizar_estado_inspecao(self, estado):
        mapa = {
            "AGUARDANDO": ("● PRONTA", CORES["ciano"]),
            "ANALISANDO": ("● ANALISANDO", CORES["amarelo"]),
            "REGISTRADO": ("● REGISTRADA", CORES["verde"]),
            "PAUSADO": ("● PAUSADA", CORES["amarelo"]),
            "EMERGÊNCIA": ("● EMERGÊNCIA", CORES["vermelho"]),
            "FALHA API": ("● FALHA API", CORES["vermelho"]),
            "BLOQUEADO": ("● BLOQUEADA", CORES["cinza"]),
        }
        texto, cor = mapa.get(estado, (f"● {estado}", CORES["texto"]))
        self.label_status_inspecao.configure(text=texto, text_color=cor)

    def atualizar_peca_atual(
        self,
        info=None,
        confianca=0.0,
        progresso=0.0,
        mensagem=None,
    ):
        confianca = max(0.0, min(1.0, float(confianca)))
        progresso = max(0.0, min(1.0, float(progresso)))

        if info:
            texto = (
                f'{info.get("cor", "-")}  •  FACE {info.get("numero", "-")}  •  '
                f'{info.get("status", "-")}'
            )
            cor = (
                CORES["verde"]
                if info.get("status") == "APROVADO"
                else CORES["vermelho"]
            )
            self.label_peca_atual.configure(text=texto, text_color=cor)
        else:
            self.label_peca_atual.configure(
                text="AGUARDANDO PEÇA", text_color=CORES["texto"]
            )

        self.label_mensagem_peca.configure(
            text=mensagem or "Posicione uma peça dentro da zona de inspeção."
        )
        self.barra_progresso.set(progresso)
        self.label_progresso.configure(text=f"PROGRESSO  {progresso:.0%}")
        self.barra_confianca.set(confianca)
        self.label_confianca.configure(text=f"CONFIANÇA  {confianca:.0%}")

        if confianca >= 0.80:
            cor_conf = CORES["verde"]
        elif confianca >= 0.50:
            cor_conf = CORES["amarelo"]
        else:
            cor_conf = CORES["vermelho"]
        self.barra_confianca.configure(progress_color=cor_conf)

    def atualizar_botao_pausa(self, pausado):
        if pausado:
            self.botao_pausa.configure(
                text="RETOMAR INSPEÇÃO",
                fg_color=CORES["verde_escuro"],
                hover_color=CORES["verde"],
            )
        else:
            self.botao_pausa.configure(
                text="PAUSAR INSPEÇÃO",
                fg_color="#B7791F",
                hover_color="#8A5E12",
            )

    def atualizar_botao_emergencia(self, ativa):
        if ativa:
            self.botao_emergencia.configure(
                text="REARMAR SISTEMA",
                fg_color="#6B1324",
                hover_color="#4B1020",
            )
        else:
            self.botao_emergencia.configure(
                text="PARADA DE EMERGÊNCIA",
                fg_color=CORES["vermelho"],
                hover_color=CORES["vermelho_escuro"],
            )

    def aba_relatorio_ativa(self):
        try:
            return self.abas.get() == self.NOME_ABA_2
        except Exception:
            return False

    def get_valores_filtro(self):
        return (
            self.opcao_filtro.get(),
            self.input_data_inicio.get(),
            self.input_data_fim.get(),
        )

    def atualizar_tabela(self, sucesso, dados):
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)
        aprovados = 0
        rejeitados = 0
        if sucesso and isinstance(dados, list) and dados:
            for item in dados:
                self.tabela.insert("", "end", values=item)
                if item[3] == "APROVADO":
                    aprovados += 1
                else:
                    rejeitados += 1
            self.texto_feedback.configure(
                text=f"{len(dados)} registros carregados.",
                text_color=CORES["texto_secundario"],
            )
        else:
            mensagem = (
                "Nenhum dado encontrado."
                if sucesso
                else f"Falha ao consultar dados: {dados}"
            )
            self.texto_feedback.configure(
                text=mensagem,
                text_color=CORES["amarelo"] if sucesso else CORES["vermelho"],
            )
        self.grafico.atualizar(aprovados, rejeitados)

    def mostrar_feedback_exportacao(self, sucesso, msg, qtd, formato="PDF"):
        if sucesso:
            self.texto_feedback.configure(
                text=f"{formato} salvo com sucesso ({qtd} peças).",
                text_color=CORES["verde"],
            )
        else:
            self.texto_feedback.configure(
                text=f"Erro ao exportar: {msg}",
                text_color=CORES["vermelho"],
            )
