import os
import threading
import time
from collections import Counter, deque
from datetime import datetime, timedelta

import cv2
import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox

from BACK_END.BANCO_DE_DADOS import ConexaoBanco
from BACK_END.VISAO import DetectorDados
from FRONT_END.INTERFACE import TelaMetalGear
from INFRA.CONFIG import carregar_memoria, salvar_memoria
from INFRA.LOGS import iniciar_caixa_preta


class MotorMetalGear:
    ESTADO_BLOQUEADO = "BLOQUEADO"
    ESTADO_AGUARDANDO = "AGUARDANDO"
    ESTADO_ANALISANDO = "ANALISANDO"
    ESTADO_REGISTRADO = "REGISTRADO"
    ESTADO_PAUSADO = "PAUSADO"
    ESTADO_EMERGENCIA = "EMERGÊNCIA"
    ESTADO_FALHA_API = "FALHA API"

    def __init__(self):
        self.log = iniciar_caixa_preta()
        self.log.info("=== INICIANDO SISTEMA METAL GEAR OS ===")

        self.config = carregar_memoria()
        configuracao_visao = self.config.get("visao", {})
        cam_index = int(self.config.get("camera_ativa", "0"))

        self.db = ConexaoBanco()
        self.ia = DetectorDados(configuracao_visao)

        self.frames_confirmacao = int(
            configuracao_visao.get("frames_confirmacao", 12)
        )
        self.confianca_minima = float(
            configuracao_visao.get("confianca_minima", 0.75)
        )
        self.frames_vazio_liberacao = int(
            configuracao_visao.get("frames_vazio_liberacao", 8)
        )
        self.frames_vazio_cancelamento = int(
            configuracao_visao.get("frames_vazio_cancelamento", 3)
        )

        self.log.info(f"Iniciando hardware de vídeo na porta {cam_index}...")
        self.camera = cv2.VideoCapture(cam_index)

        self.SESSAO_ATUAL = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.tempo_inicio = None
        self.aprovados = 0
        self.rejeitados = 0
        self.historico_pecas = []
        self.ultima_peca_confirmada = None
        self.ultima_confianca = 0.0

        self.ultimo_calculo_fps = time.perf_counter()
        self.frames_desde_fps = 0
        self.fps_atual = 0.0

        self.usuario_autenticado = False
        self.inspecao_pausada = False
        self.emergencia_ativa = False
        self.estado_inspecao = self.ESTADO_BLOQUEADO
        self.amostras = deque(maxlen=max(3, self.frames_confirmacao))
        self.frames_vazios = 0

        self.api_online = False
        self.verificacao_api_em_andamento = False
        self.encerrando = False

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.janela = ctk.CTk()
        self.janela.geometry("1360x780")
        self.janela.minsize(1160, 700)
        self.janela.title("METAL GEAR OS — Centro de Inspeção")

        self._configurar_icone()

        self.tela = TelaMetalGear(self.janela, self)
        self.tela.menu_camera.set(str(cam_index))
        self.tela.atualizar_status_camera(self.camera.isOpened())
        self.tela.atualizar_status_api(False)
        self.tela.atualizar_estado_inspecao(self.estado_inspecao)
        self.tela.atualizar_fps(0.0)

        self.janela.protocol("WM_DELETE_WINDOW", self.encerrar_sistema)

        self.sincronizar_relogio_uptime()
        self.monitorar_api()
        self.rodar_inspecao()
        self.janela.mainloop()

    def _configurar_icone(self):
        try:
            pasta_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_png = os.path.join(pasta_atual, "ASSETS", "final_image.png")
            caminho_ico = os.path.join(
                pasta_atual,
                "ASSETS",
                "icone_metal_gear.ico",
            )

            if not os.path.exists(caminho_ico):
                img_pil = Image.open(caminho_png)
                img_pil.save(caminho_ico, format="ICO", sizes=[(64, 64)])

            self.janela.iconbitmap(caminho_ico)
            self.log.info("Ícone tático carregado com sucesso.")
        except Exception as erro:
            self.log.warning(f"Não foi possível carregar o ícone: {erro}")

    def tentar_login(self, user, senha):
        if user == "admin" and senha == "admin":
            perfil = "admin"
        elif user == "operador" and senha == "123":
            perfil = "operador"
        else:
            self.tela.mostrar_erro_login("❌ Credenciais Inválidas")
            self.log.warning(
                f"Tentativa de login falhada. Usuário tentado: {user}"
            )
            return

        self.usuario_autenticado = True
        self.tempo_inicio = datetime.now()
        self.tela.liberar_acesso(perfil=perfil)
        self.aplicar_regras_dinamicas()
        self._reiniciar_ciclo(self.ESTADO_AGUARDANDO)
        self.log.info(f"Login de {perfil} realizado com sucesso.")

    def aplicar_regras_dinamicas(self):
        lista_cores, lista_numeros = self.tela.coletar_listas_permitidas()
        self.ia.atualizar_regras_multiplas(lista_cores, lista_numeros)

        self.config["regras"] = {
            "cores": lista_cores,
            "numeros": lista_numeros,
        }
        salvar_memoria(self.config)
        self.log.info(
            f"Regras atualizadas: {lista_cores} | {lista_numeros}"
        )

    def sincronizar_relogio_uptime(self):
        try:
            if not self.janela.winfo_exists():
                return

            agora = datetime.now()
            self.tela.atualizar_relogio_interface(agora.strftime("%H:%M:%S"))

            if self.tempo_inicio:
                delta = agora - self.tempo_inicio
                total_segundos = int(delta.total_seconds())
                horas, resto = divmod(total_segundos, 3600)
                minutos, segundos = divmod(resto, 60)
                self.tela.atualizar_uptime_interface(
                    f"{horas:02d}h {minutos:02d}m {segundos:02d}s"
                )

            self.janela.after(1000, self.sincronizar_relogio_uptime)
        except Exception:
            self.log.exception("Erro ao atualizar relógio e uptime.")

    def monitorar_api(self):
        if self.encerrando or self.verificacao_api_em_andamento:
            return

        self.verificacao_api_em_andamento = True

        def verificar():
            online = self.db.verificar_conexao()

            def aplicar_resultado():
                if self.encerrando:
                    return
                self.api_online = online
                self.verificacao_api_em_andamento = False
                self.tela.atualizar_status_api(online)
                self.janela.after(10000, self.monitorar_api)

            try:
                self.janela.after(0, aplicar_resultado)
            except Exception:
                pass

        threading.Thread(target=verificar, daemon=True).start()

    def alterar_camera(self, escolha_index):
        try:
            idx = int(escolha_index)
            self.log.info(f"Alterando câmera para a porta {idx}...")

            if self.camera:
                self.camera.release()

            self.camera = cv2.VideoCapture(idx)
            camera_online = self.camera.isOpened()
            self.tela.atualizar_status_camera(camera_online)

            self.config["camera_ativa"] = str(idx)
            salvar_memoria(self.config)

            if camera_online:
                self.log.info("Nova câmera ativada com sucesso.")
            else:
                self.log.error("Não foi possível abrir a câmera selecionada.")
        except Exception:
            self.log.exception("Erro ao alternar câmera.")
            self.tela.atualizar_status_camera(False)

    def alternar_pausa(self):
        if self.emergencia_ativa or not self.usuario_autenticado:
            return

        self.inspecao_pausada = not self.inspecao_pausada
        self.tela.atualizar_botao_pausa(self.inspecao_pausada)

        if self.inspecao_pausada:
            self._reiniciar_ciclo(self.ESTADO_PAUSADO)
            self.log.info("Inspeção pausada pelo operador.")
        else:
            self._reiniciar_ciclo(self.ESTADO_AGUARDANDO)
            self.log.info("Inspeção retomada pelo operador.")

    def acionar_emergencia(self):
        if not self.usuario_autenticado:
            return

        if not self.emergencia_ativa:
            self.emergencia_ativa = True
            self.inspecao_pausada = True
            self.tela.atualizar_botao_emergencia(True)
            self.tela.atualizar_botao_pausa(True)
            self._reiniciar_ciclo(self.ESTADO_EMERGENCIA)
            self.log.critical("PARADA DE EMERGÊNCIA DE SOFTWARE ATIVADA.")
            return

        self.emergencia_ativa = False
        self.inspecao_pausada = True
        self.tela.atualizar_botao_emergencia(False)
        self.tela.atualizar_botao_pausa(True)
        self._reiniciar_ciclo(self.ESTADO_PAUSADO)
        self.log.warning(
            "Sistema rearmado. A inspeção permanece pausada até liberação manual."
        )

    def _reiniciar_ciclo(self, novo_estado):
        self.amostras.clear()
        self.frames_vazios = 0
        if novo_estado == self.ESTADO_AGUARDANDO:
            self.ultima_peca_confirmada = None
            self.ultima_confianca = 0.0
        self.estado_inspecao = novo_estado
        self.tela.atualizar_estado_inspecao(novo_estado)

        mensagens = {
            self.ESTADO_AGUARDANDO: "Posicione uma peça dentro da zona de inspeção.",
            self.ESTADO_PAUSADO: "Inspeção pausada pelo operador.",
            self.ESTADO_EMERGENCIA: "EMERGÊNCIA ATIVA — sistema bloqueado.",
            self.ESTADO_BLOQUEADO: "Faça login para iniciar a inspeção.",
        }
        mensagem = mensagens.get(novo_estado)
        if mensagem:
            self.tela.atualizar_peca_atual(mensagem=mensagem)

    def obter_datas_do_filtro(self):
        modo, dt_in, dt_out = self.tela.get_valores_filtro()

        if modo == "Últimas 48 Horas":
            return (
                (datetime.now() - timedelta(days=2)).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                None,
            )
        if modo == "Sessão Atual (Desde que abriu)":
            return self.SESSAO_ATUAL, None
        if modo == "Apenas Hoje":
            hoje = datetime.now().strftime("%Y-%m-%d")
            return f"{hoje} 00:00:00", f"{hoje} 23:59:59"
        if modo == "Data Específica":
            def formatar(valor, fim=False):
                try:
                    dia, mes, ano = valor.split("/")
                    horario = "23:59:59" if fim else "00:00:00"
                    return f"{ano}-{mes}-{dia} {horario}"
                except (ValueError, AttributeError):
                    return None

            return formatar(dt_in), formatar(dt_out, True)

        return None, None

    def carregar_dados_na_tabela(self):
        data_in, data_out = self.obter_datas_do_filtro()
        sucesso, dados = self.db.buscar_historico(data_in, data_out)
        self.tela.atualizar_tabela(sucesso, dados)

    def solicitar_pdf(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Documentos PDF", "*.pdf")],
            title="Local para Salvar Relatório PDF",
        )
        if not caminho:
            return

        self.log.info("Solicitada exportação de relatório em PDF.")
        data_in, data_out = self.obter_datas_do_filtro()
        sucesso, mensagem, quantidade = self.db.exportar_pdf(
            caminho,
            data_in,
            data_out,
        )
        self.tela.mostrar_feedback_exportacao(
            sucesso,
            mensagem,
            quantidade,
            "PDF",
        )

    def solicitar_csv(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Planilhas Excel/CSV", "*.csv")],
            title="Local para Salvar Planilha Excel",
        )
        if not caminho:
            return

        self.log.info("Solicitada exportação de relatório em CSV.")
        data_in, data_out = self.obter_datas_do_filtro()
        sucesso, mensagem, quantidade = self.db.exportar_csv(
            caminho,
            data_in,
            data_out,
        )
        self.tela.mostrar_feedback_exportacao(
            sucesso,
            mensagem,
            quantidade,
            "Planilha CSV",
        )

    def solicitar_limpeza_banco(self):
        confirmar = messagebox.askyesno(
            "Confirmar limpeza",
            "Esta ação apagará todo o histórico de produção.\n\nDeseja continuar?",
            icon="warning",
        )
        if not confirmar:
            return

        self.log.warning("Limpeza total do banco solicitada pelo administrador.")

        if self.db.limpar_tabela_producao():
            self.aprovados = 0
            self.rejeitados = 0
            self.historico_pecas = []
            self.tela.atualizar_contadores(0, 0)
            self.tela.atualizar_historico_visual([])
            self.carregar_dados_na_tabela()
            self.tela.texto_feedback.configure(
                text="💥 Base de dados limpa!",
                text_color="red",
            )
            self.log.info("Banco de dados limpo com sucesso.")
        else:
            messagebox.showerror(
                "Falha na limpeza",
                "Não foi possível limpar o banco de dados.",
            )
            self.log.error("Falha ao limpar o banco de dados.")

    @staticmethod
    def _desenhar_aviso(frame, texto, cor):
        altura, largura = frame.shape[:2]
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        escala = 0.8
        espessura = 2
        (texto_largura, texto_altura), _ = cv2.getTextSize(
            texto,
            fonte,
            escala,
            espessura,
        )
        x = max(10, (largura - texto_largura) // 2)
        y = max(50, altura // 2)
        cv2.rectangle(
            frame,
            (x - 12, y - texto_altura - 12),
            (x + texto_largura + 12, y + 12),
            (15, 15, 15),
            -1,
        )
        cv2.rectangle(
            frame,
            (x - 12, y - texto_altura - 12),
            (x + texto_largura + 12, y + 12),
            cor,
            2,
        )
        cv2.putText(
            frame,
            texto,
            (x, y),
            fonte,
            escala,
            cor,
            espessura,
            cv2.LINE_AA,
        )

    def _processar_fluxo_inspecao(self, peca_vista, info_peca):
        if self.estado_inspecao == self.ESTADO_REGISTRADO:
            if peca_vista:
                self.frames_vazios = 0
                info_exibida = self.ultima_peca_confirmada or info_peca
                self.tela.atualizar_peca_atual(
                    info=info_exibida,
                    confianca=self.ultima_confianca,
                    progresso=1.0,
                    mensagem="REGISTRADA — retire a peça da zona para liberar o próximo ciclo.",
                )
                return

            self.frames_vazios += 1
            if self.frames_vazios >= self.frames_vazio_liberacao:
                self._reiniciar_ciclo(self.ESTADO_AGUARDANDO)
            return

        if peca_vista and info_peca and 1 <= info_peca.get("numero", 0) <= 6:
            self.frames_vazios = 0
            self.estado_inspecao = self.ESTADO_ANALISANDO
            self.tela.atualizar_estado_inspecao(self.estado_inspecao)

            chave = (
                info_peca["cor"],
                info_peca["numero"],
                info_peca["status"],
            )
            self.amostras.append(chave)

            mais_comum, quantidade = Counter(self.amostras).most_common(1)[0]
            confianca = quantidade / len(self.amostras)
            progresso = min(
                1.0,
                len(self.amostras) / max(1, self.frames_confirmacao),
            )

            leitura_estavel = {
                "cor": mais_comum[0],
                "numero": mais_comum[1],
                "status": mais_comum[2],
            }

            mensagem_analise = (
                f"Analisando {len(self.amostras)}/{self.frames_confirmacao} frames"
            )
            if (
                len(self.amostras) >= self.frames_confirmacao
                and confianca < self.confianca_minima
            ):
                mensagem_analise = (
                    "Leitura instável — mantenha a peça parada dentro da zona."
                )

            self.tela.atualizar_peca_atual(
                info=leitura_estavel,
                confianca=confianca,
                progresso=progresso,
                mensagem=mensagem_analise,
            )

            if (
                len(self.amostras) >= self.frames_confirmacao
                and confianca >= self.confianca_minima
            ):
                self._registrar_peca_confirmada(leitura_estavel, confianca)
            return

        self.frames_vazios += 1

        if self.estado_inspecao == self.ESTADO_ANALISANDO:
            if self.frames_vazios >= self.frames_vazio_cancelamento:
                self._reiniciar_ciclo(self.ESTADO_AGUARDANDO)
        elif self.estado_inspecao != self.ESTADO_AGUARDANDO:
            self._reiniciar_ciclo(self.ESTADO_AGUARDANDO)

    def _registrar_peca_confirmada(self, info_peca, confianca):
        self.ultima_peca_confirmada = dict(info_peca)
        self.ultima_confianca = float(confianca)

        sucesso = self.db.salvar_peca(
            info_peca["cor"],
            info_peca["numero"],
            info_peca["status"],
        )

        self.amostras.clear()
        self.frames_vazios = 0

        if not sucesso:
            self.api_online = False
            self.tela.atualizar_status_api(False)
            self.estado_inspecao = self.ESTADO_REGISTRADO
            self.tela.atualizar_estado_inspecao(self.ESTADO_FALHA_API)
            self.tela.atualizar_peca_atual(
                info=info_peca,
                confianca=confianca,
                progresso=1.0,
                mensagem="FALHA AO SALVAR — retire a peça e verifique a API.",
            )
            self.log.error(
                "Leitura confirmada, mas não foi possível salvá-la na API."
            )
            return

        self.api_online = True
        self.tela.atualizar_status_api(True)
        self.estado_inspecao = self.ESTADO_REGISTRADO
        self.tela.atualizar_estado_inspecao(self.estado_inspecao)

        if info_peca["status"] == "APROVADO":
            self.aprovados += 1
        else:
            self.rejeitados += 1

        self.tela.atualizar_contadores(self.aprovados, self.rejeitados)

        horario = datetime.now().strftime("%H:%M:%S")
        item_historico = (
            f'{horario}  |  {info_peca["cor"]}  •  FACE {info_peca["numero"]}  •  '
            f'{info_peca["status"]}  •  {confianca:.0%}'
        )
        self.historico_pecas.insert(0, item_historico)
        if len(self.historico_pecas) > 15:
            self.historico_pecas.pop()

        self.tela.atualizar_historico_visual(self.historico_pecas)
        self.tela.atualizar_peca_atual(
            info=info_peca,
            confianca=confianca,
            progresso=1.0,
            mensagem="REGISTRADA — retire a peça da zona.",
        )

        if self.tela.aba_relatorio_ativa():
            self.carregar_dados_na_tabela()

        self.log.info(
            "Peça confirmada e registrada: "
            f'{info_peca["cor"]} {info_peca["numero"]} '
            f'-> {info_peca["status"]} | confiança {confianca:.1%}'
        )

    def _atualizar_medicao_fps(self):
        self.frames_desde_fps += 1
        agora = time.perf_counter()
        intervalo = agora - self.ultimo_calculo_fps
        if intervalo >= 1.0:
            self.fps_atual = self.frames_desde_fps / intervalo
            self.frames_desde_fps = 0
            self.ultimo_calculo_fps = agora
            self.tela.atualizar_fps(self.fps_atual)

    def rodar_inspecao(self):
        try:
            if self.encerrando or not self.janela.winfo_exists():
                return

            sucesso, frame = self.camera.read()
            self.tela.atualizar_status_camera(bool(sucesso))

            if not sucesso:
                frame = self._criar_frame_sem_camera()
                self.tela.atualizar_camera(Image.fromarray(frame))
                self.janela.after(250, self.rodar_inspecao)
                return

            frame = cv2.flip(frame, 1)
            frame_processado = frame.copy()

            if not self.usuario_autenticado:
                self._desenhar_aviso(
                    frame_processado,
                    "AGUARDANDO LOGIN",
                    (0, 215, 255),
                )
            elif self.emergencia_ativa:
                self._desenhar_aviso(
                    frame_processado,
                    "EMERGENCIA ATIVA",
                    (0, 0, 255),
                )
            elif self.inspecao_pausada:
                self._desenhar_aviso(
                    frame_processado,
                    "INSPECAO PAUSADA",
                    (0, 165, 255),
                )
            else:
                frame_processado, peca_vista, info_peca = self.ia.processar_frame(
                    frame_processado
                )
                self._processar_fluxo_inspecao(peca_vista, info_peca)

            frame_rgb = cv2.cvtColor(frame_processado, cv2.COLOR_BGR2RGB)
            self.tela.atualizar_camera(Image.fromarray(frame_rgb))
            self._atualizar_medicao_fps()
            self.janela.after(15, self.rodar_inspecao)

        except Exception:
            self.log.exception("Erro no ciclo principal de inspeção.")
            if not self.encerrando:
                self.janela.after(250, self.rodar_inspecao)

    @staticmethod
    def _criar_frame_sem_camera():
        import numpy as np

        frame = np.zeros((600, 800, 3), dtype=np.uint8)
        cv2.putText(
            frame,
            "CAMERA INDISPONIVEL",
            (185, 300),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            2,
            cv2.LINE_AA,
        )
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def encerrar_sistema(self):
        self.encerrando = True
        try:
            self.log.info("Encerrando o Sistema Metal Gear de forma segura...")
            if self.camera and self.camera.isOpened():
                self.camera.release()
            self.janela.quit()
            self.janela.destroy()
        except Exception:
            self.log.exception("Erro durante o encerramento do sistema.")


if __name__ == "__main__":
    MotorMetalGear()
