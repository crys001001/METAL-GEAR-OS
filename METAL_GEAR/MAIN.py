import cv2
import os  # <-- Importação necessária para os caminhos
from PIL import Image, ImageTk  # <-- Adicionado o ImageTk
from datetime import datetime, timedelta  
import customtkinter as ctk
from tkinter import filedialog 

from BACK_END.BANCO_DE_DADOS import ConexaoBanco
from BACK_END.VISAO import DetectorDados
from FRONT_END.INTERFACE import TelaMetalGear

# Importando a nossa nova Infraestrutura!
from INFRA.LOGS import iniciar_caixa_preta
from INFRA.CONFIG import carregar_memoria, salvar_memoria

class MotorMetalGear:
    def __init__(self):
        # 1. Inicia a Caixa Preta (Logs)
        self.log = iniciar_caixa_preta()
        self.log.info("=== INICIANDO SISTEMA METAL GEAR OS ===")

        # 2. Carrega a Memória de Longo Prazo (config.json)
        self.config = carregar_memoria()
        cam_index = int(self.config["camera_ativa"])

        self.db = ConexaoBanco()
        self.ia = DetectorDados()
        
        # 3. Liga a câmara baseada na memória salva!
        self.log.info(f"Iniciando hardware de vídeo na porta {cam_index}...")
        self.camera = cv2.VideoCapture(cam_index)

        self.SESSAO_ATUAL = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.tempo_inicio = None 
        self.aprovados = 0
        self.rejeitados = 0
        self.peca_na_tela = False
        self.memoria_temporaria = {"cor": "", "numero": 0, "status": ""}
        self.historico_pecas = [] 

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.janela = ctk.CTk()
        self.janela.geometry("1300x750") 
        self.janela.title("METAL_GEAR - Sistema Operacional")

       # ==========================================
        # --- O TRUQUE DEFINITIVO DO ÍCONE (.ICO) ---
        # ==========================================
        try:
            pasta_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_png = os.path.join(pasta_atual, "ASSETS", "final_image.png")
            caminho_ico = os.path.join(pasta_atual, "ASSETS", "icone_metal_gear.ico")

            # 1. Se o ficheiro .ico ainda não existir, o Python fabrica um a partir do seu PNG!
            if not os.path.exists(caminho_ico):
                img_pil = Image.open(caminho_png)
                # Guarda a imagem no formato nativo de ícones do Windows
                img_pil.save(caminho_ico, format="ICO", sizes=[(64, 64)])

            # 2. Força o Windows a usar este ficheiro .ico nativo
            self.janela.iconbitmap(caminho_ico)
            
            self.log.info("Ícone tático (.ico) carregado no MAIN com sucesso.")
        except Exception as e:
            self.log.warning(f"Aviso: Não foi possível carregar o ícone nativo no MAIN. {e}")
        # ==========================================

        self.tela = TelaMetalGear(self.janela, self)
        
        # Ajusta o menu da interface para mostrar a câmera que foi carregada da memória
        self.tela.menu_camera.set(str(cam_index))

        self.janela.protocol("WM_DELETE_WINDOW", self.encerrar_sistema)

        self.sincronizar_relogio_uptime()
        self.rodar_inspecao()
        self.janela.mainloop()

    def tentar_login(self, user, senha):
        if user == "admin" and senha == "admin":
            self.tempo_inicio = datetime.now() 
            self.tela.liberar_acesso(perfil="admin")
            self.aplicar_regras_dinamicas() 
            self.log.info("Login de Administrador bem sucedido.")
        elif user == "operador" and senha == "123":
            self.tempo_inicio = datetime.now() 
            self.tela.liberar_acesso(perfil="operador")
            self.aplicar_regras_dinamicas()
            self.log.info("Login de Operador bem sucedido.")
        else:
            self.tela.mostrar_erro_login("❌ Credenciais Inválidas")
            self.log.warning(f"Tentativa de login falhada. Usuário tentado: {user}")

    def aplicar_regras_dinamicas(self):
        lista_cores, lista_numeros = self.tela.coletar_listas_permitidas()
        self.ia.atualizar_regras_multiplas(lista_cores, lista_numeros)
        
        # NOVIDADE: Quando o Admin clica numa caixinha, salva imediatamente no config.json!
        if hasattr(self, 'config'):
            self.config["regras"] = {
                "cores": lista_cores,
                "numeros": lista_numeros
            }
            from INFRA.CONFIG import salvar_memoria
            salvar_memoria(self.config)
            self.log.info(f"Novas regras guardadas na memória: {lista_cores} | {lista_numeros}")

    def sincronizar_relogio_uptime(self):
        try:
            if not self.janela.winfo_exists(): return
            agora = datetime.now()
            self.tela.atualizar_relogio_interface(agora.strftime('%H:%M:%S'))
            if self.tempo_inicio:
                delta = agora - self.tempo_inicio
                horas, resto = divmod(delta.seconds, 3600)
                minutos, segundos = divmod(resto, 60)
                self.tela.atualizar_uptime_interface(f"{horas:02d}h {minutos:02d}m {segundos:02d}s")
            self.janela.after(1000, self.sincronizar_relogio_uptime)
        except Exception: pass 

    def alterar_camera(self, escolha_index):
        try:
            idx = int(escolha_index)
            self.log.info(f"Alterando hardware de vídeo para porta {idx}...")
            self.camera.release()
            self.camera = cv2.VideoCapture(idx)
            
            # Atualiza a Memória JSON
            self.config["camera_ativa"] = str(idx)
            salvar_memoria(self.config)
            self.log.info("Nova porta de hardware salva com sucesso no config.json.")
            
        except Exception as e: 
            self.log.error(f"Erro crítico ao alternar hardware de vídeo: {e}")

    def obter_datas_do_filtro(self):
        modo, dt_in, dt_out = self.tela.get_valores_filtro()
        if modo == "Últimas 48 Horas": return (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'), None
        elif modo == "Sessão Atual (Desde que abriu)": return self.SESSAO_ATUAL, None
        elif modo == "Apenas Hoje": return f"{datetime.now().strftime('%Y-%m-%d')} 00:00:00", f"{datetime.now().strftime('%Y-%m-%d')} 23:59:59"
        elif modo == "Data Específica":
            def formatar(dt, fim=False):
                try: d, m, a = dt.split('/'); return f"{a}-{m}-{d} {'23:59:59' if fim else '00:00:00'}"
                except: return None
            return formatar(dt_in), formatar(dt_out, True)
        return None, None 

    def carregar_dados_na_tabela(self):
        data_in, data_out = self.obter_datas_do_filtro()
        sucesso, dados = self.db.buscar_historico(data_in, data_out)
        self.tela.atualizar_tabela(sucesso, dados)

    def solicitar_pdf(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Documentos PDF", "*.pdf")], title="Local para Salvar Relatório PDF")
        if not caminho: return 
        
        self.log.info("Solicitada exportação de relatório em PDF.")
        in_d, out_d = self.obter_datas_do_filtro()
        s, msg, q = self.db.exportar_pdf(caminho, in_d, out_d)
        self.tela.mostrar_feedback_exportacao(s, msg, q, "PDF")

    def solicitar_csv(self):
        caminho = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Planilhas Excel/CSV", "*.csv")], title="Local para Salvar Planilha Excel")
        if not caminho: return
        
        self.log.info("Solicitada exportação de relatório em CSV.")
        in_d, out_d = self.obter_datas_do_filtro()
        s, msg, q = self.db.exportar_csv(caminho, in_d, out_d)
        self.tela.mostrar_feedback_exportacao(s, msg, q, "Planilha CSV")

    def solicitar_limpeza_banco(self):
        self.log.warning("Comando de ZONA DE PERIGO ativado. Tentando limpar banco de dados...")
        if self.db.limpar_tabela_producao():
            self.aprovados, self.rejeitados, self.historico_pecas = 0, 0, []
            self.tela.atualizar_contadores(0, 0)
            self.tela.atualizar_historico_visual([])
            self.carregar_dados_na_tabela()
            self.tela.texto_feedback.configure(text="💥 Base de dados limpa!", text_color="red")
            self.log.info("Banco de dados do MySQL limpo com sucesso!")
        else:
            self.log.error("Falha ao tentar limpar o banco de dados do MySQL.")

    def rodar_inspecao(self):
        try:
            if not self.janela.winfo_exists(): return
            sucesso, frame = self.camera.read()
            if sucesso:
                frame = cv2.flip(frame, 1)
                frame_processado, peca_vista_agora, info_peca = self.ia.processar_frame(frame)
                
                if peca_vista_agora and info_peca:
                    if not self.peca_na_tela:
                        self.peca_na_tela = True
                        self.memoria_temporaria = info_peca 
                    else:
                        if info_peca["numero"] >= self.memoria_temporaria["numero"]:
                            self.memoria_temporaria = info_peca

                elif not peca_vista_agora and self.peca_na_tela:
                    if self.memoria_temporaria["numero"] > 0:
                        self.db.salvar_peca(self.memoria_temporaria["cor"], self.memoria_temporaria["numero"], self.memoria_temporaria["status"])
                        
                        # Logamos cada peça processada!
                        self.log.info(f"Peça Inspecionada: {self.memoria_temporaria['cor']} {self.memoria_temporaria['numero']} -> {self.memoria_temporaria['status']}")
                        
                        if self.memoria_temporaria["status"] == "APROVADO": self.aprovados += 1
                        else: self.rejeitados += 1
                        self.tela.atualizar_contadores(self.aprovados, self.rejeitados)
                        
                        dados_item = f'{self.memoria_temporaria["cor"]} {self.memoria_temporaria["numero"]} - {self.memoria_temporaria["status"]}'
                        self.historico_pecas.insert(0, dados_item)
                        if len(self.historico_pecas) > 15: self.historico_pecas.pop()
                        
                        self.tela.atualizar_historico_visual(self.historico_pecas)
                        if self.tela.aba_relatorio_ativa(): self.carregar_dados_na_tabela()
                    self.peca_na_tela = False

                frame_rgb = cv2.cvtColor(frame_processado, cv2.COLOR_BGR2RGB)
                self.tela.atualizar_camera(Image.fromarray(frame_rgb))
            
            self.janela.after(15, self.rodar_inspecao)
        except Exception: pass

    def encerrar_sistema(self):
        try:
            self.log.info("Encerrando o Sistema Metal Gear de forma segura...")
            if self.camera.isOpened(): self.camera.release()
            self.janela.quit()
            self.janela.destroy()
        except Exception: pass

if __name__ == "__main__":
    MotorMetalGear()