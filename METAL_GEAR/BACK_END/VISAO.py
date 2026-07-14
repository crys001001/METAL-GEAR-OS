import cv2
import numpy as np


class DetectorDados:
    """Detector RGB com zona de inspeção e overlay industrial moderno."""

    def __init__(self, configuracao=None):
        self.filtros_dados = {
            "AZUL": (
                (np.array([90, 100, 50]), np.array([130, 255, 255])),
                (235, 128, 52),
            ),
            "VERDE": (
                (np.array([40, 70, 50]), np.array([85, 255, 255])),
                (60, 214, 124),
            ),
        }
        self.cores_permitidas = ["VERMELHO", "VERDE", "AZUL"]
        self.numeros_permitidos = [1, 2, 3, 4, 5, 6]
        self.configurar(configuracao or {})

    def configurar(self, configuracao):
        roi = configuracao.get("roi", {})
        self.roi_x = float(roi.get("x", 0.22))
        self.roi_y = float(roi.get("y", 0.16))
        self.roi_largura = float(roi.get("largura", 0.56))
        self.roi_altura = float(roi.get("altura", 0.68))

        self.area_minima = int(configuracao.get("area_minima", 1800))
        self.area_maxima = int(configuracao.get("area_maxima", 80000))
        self.proporcao_minima = float(
            configuracao.get("proporcao_minima", 0.65)
        )
        self.proporcao_maxima = float(
            configuracao.get("proporcao_maxima", 1.40)
        )
        self.area_ponto_minima = int(
            configuracao.get("area_ponto_minima", 20)
        )
        self.area_ponto_maxima = int(
            configuracao.get("area_ponto_maxima", 500)
        )
        self.circularidade_minima = float(
            configuracao.get("circularidade_minima", 0.58)
        )
        self.escurecimento_externo = float(
            configuracao.get("escurecimento_externo", 0.42)
        )
        self.mostrar_mira = bool(configuracao.get("mostrar_mira", True))

    def atualizar_regras_multiplas(self, lista_cores, lista_numeros):
        self.cores_permitidas = [
            cor for cor in lista_cores if cor in {"VERMELHO", "VERDE", "AZUL"}
        ]
        self.numeros_permitidos = list(lista_numeros)

    @staticmethod
    def _calcular_roi(frame, x, y, largura, altura):
        h, w = frame.shape[:2]
        x1 = max(0, min(int(w * x), w - 2))
        y1 = max(0, min(int(h * y), h - 2))
        x2 = max(x1 + 1, min(int(w * (x + largura)), w - 1))
        y2 = max(y1 + 1, min(int(h * (y + altura)), h - 1))
        return x1, y1, x2, y2

    @staticmethod
    def _texto_com_fundo(
        frame,
        texto,
        origem,
        cor_texto,
        escala=0.52,
        espessura=1,
        margem_x=9,
        margem_y=6,
    ):
        fonte = cv2.FONT_HERSHEY_DUPLEX
        (tw, th), base = cv2.getTextSize(
            texto, fonte, escala, espessura
        )
        x, y = origem
        x = max(4, min(x, frame.shape[1] - tw - 2 * margem_x - 4))
        y = max(th + margem_y + 4, min(y, frame.shape[0] - base - margem_y - 4))

        overlay = frame.copy()
        cv2.rectangle(
            overlay,
            (x, y - th - margem_y),
            (x + tw + 2 * margem_x, y + base + margem_y),
            (14, 16, 22),
            -1,
        )
        cv2.addWeighted(overlay, 0.88, frame, 0.12, 0, frame)
        cv2.rectangle(
            frame,
            (x, y - th - margem_y),
            (x + 4, y + base + margem_y),
            cor_texto,
            -1,
        )
        cv2.putText(
            frame,
            texto,
            (x + margem_x, y),
            fonte,
            escala,
            cor_texto,
            espessura,
            cv2.LINE_AA,
        )

    @staticmethod
    def _desenhar_cantos(frame, x1, y1, x2, y2, cor, espessura=2):
        comprimento = max(18, int(min(x2 - x1, y2 - y1) * 0.08))
        # superior esquerdo
        cv2.line(frame, (x1, y1), (x1 + comprimento, y1), cor, espessura)
        cv2.line(frame, (x1, y1), (x1, y1 + comprimento), cor, espessura)
        # superior direito
        cv2.line(frame, (x2, y1), (x2 - comprimento, y1), cor, espessura)
        cv2.line(frame, (x2, y1), (x2, y1 + comprimento), cor, espessura)
        # inferior esquerdo
        cv2.line(frame, (x1, y2), (x1 + comprimento, y2), cor, espessura)
        cv2.line(frame, (x1, y2), (x1, y2 - comprimento), cor, espessura)
        # inferior direito
        cv2.line(frame, (x2, y2), (x2 - comprimento, y2), cor, espessura)
        cv2.line(frame, (x2, y2), (x2, y2 - comprimento), cor, espessura)

    def _aplicar_foco_roi(self, frame, x1, y1, x2, y2):
        fator = max(0.15, min(0.85, 1.0 - self.escurecimento_externo))
        original_roi = frame[y1:y2, x1:x2].copy()
        frame[:] = np.clip(frame.astype(np.float32) * fator, 0, 255).astype(
            np.uint8
        )
        frame[y1:y2, x1:x2] = original_roi

    def _contar_pontos(self, recorte_suave):
        hsv_recorte = cv2.cvtColor(recorte_suave, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(
            hsv_recorte,
            np.array([0, 0, 175]),
            np.array([180, 75, 255]),
        )
        mascara = cv2.morphologyEx(
            mascara,
            cv2.MORPH_OPEN,
            np.ones((3, 3), np.uint8),
        )

        contornos, _ = cv2.findContours(
            mascara,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )
        quantidade = 0
        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if not self.area_ponto_minima < area < self.area_ponto_maxima:
                continue
            perimetro = cv2.arcLength(contorno, True)
            if perimetro <= 0:
                continue
            circularidade = 4 * np.pi * area / (perimetro * perimetro)
            if circularidade >= self.circularidade_minima:
                quantidade += 1
        return min(quantidade, 6)

    def _desenhar_overlay_zona(self, frame, coords, alvo_encontrado):
        x1, y1, x2, y2 = coords
        cor_zona = (32, 170, 247)  # âmbar-dourado em BGR
        self._aplicar_foco_roi(frame, x1, y1, x2, y2)
        self._desenhar_cantos(frame, x1, y1, x2, y2, cor_zona, 2)

        estado = "ALVO DETECTADO" if alvo_encontrado else "AGUARDANDO"
        self._texto_com_fundo(
            frame,
            f"ZONA DE INSPECAO  /  {estado}",
            (x1, max(28, y1 - 12)),
            cor_zona,
            escala=0.48,
            espessura=1,
        )

        if self.mostrar_mira:
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            cv2.line(frame, (cx - 9, cy), (cx + 9, cy), (104, 94, 132), 1)
            cv2.line(frame, (cx, cy - 9), (cx, cy + 9), (104, 94, 132), 1)
            cv2.circle(frame, (cx, cy), 18, (78, 68, 102), 1)

    def _desenhar_alvo(self, frame, alvo, status):
        x = alvo["x"]
        y = alvo["y"]
        largura = alvo["largura"]
        altura = alvo["altura"]
        cor = alvo["cor_bgr"]
        x2 = x + largura
        y2 = y + altura

        self._desenhar_cantos(frame, x, y, x2, y2, cor, 4)

        etiqueta = f'{alvo["cor"]}  •  FACE {alvo["numero"]}'
        self._texto_com_fundo(
            frame,
            etiqueta,
            (x, max(32, y - 13)),
            cor,
            escala=0.56,
            espessura=1,
        )

        cor_status = (60, 214, 124) if status == "APROVADO" else (92, 92, 245)
        self._texto_com_fundo(
            frame,
            status,
            (x, min(frame.shape[0] - 10, y2 + 26)),
            cor_status,
            escala=0.46,
            espessura=1,
        )

    def processar_frame(self, frame):
        # Sempre analisa uma cópia limpa; nenhum desenho entra na segmentação.
        frame_limpo = frame.copy()
        coords = self._calcular_roi(
            frame_limpo,
            self.roi_x,
            self.roi_y,
            self.roi_largura,
            self.roi_altura,
        )
        x_roi1, y_roi1, x_roi2, y_roi2 = coords
        roi_original = frame_limpo[y_roi1:y_roi2, x_roi1:x_roi2]

        if roi_original.size == 0:
            return frame, False, None

        roi_suave = cv2.GaussianBlur(roi_original, (9, 9), 0)
        hsv = cv2.cvtColor(roi_suave, cv2.COLOR_BGR2HSV)

        mascara_vermelho = cv2.bitwise_or(
            cv2.inRange(
                hsv,
                np.array([0, 120, 70]),
                np.array([10, 255, 255]),
            ),
            cv2.inRange(
                hsv,
                np.array([170, 120, 70]),
                np.array([180, 255, 255]),
            ),
        )

        mascaras = {
            "VERMELHO": (mascara_vermelho, (92, 92, 245)),
        }
        for nome_cor, dados in self.filtros_dados.items():
            mascaras[nome_cor] = (
                cv2.inRange(hsv, dados[0][0], dados[0][1]),
                dados[1],
            )

        candidatos = []
        centro_roi_x = (x_roi2 - x_roi1) / 2
        centro_roi_y = (y_roi2 - y_roi1) / 2
        diagonal_roi = max(
            1.0,
            np.hypot(x_roi2 - x_roi1, y_roi2 - y_roi1),
        )
        kernel_abertura = np.ones((3, 3), np.uint8)
        kernel_fechamento = np.ones((5, 5), np.uint8)

        for nome_cor, (mascara_cor, cor_bgr) in mascaras.items():
            mascara_cor = cv2.morphologyEx(
                mascara_cor,
                cv2.MORPH_OPEN,
                kernel_abertura,
            )
            mascara_cor = cv2.morphologyEx(
                mascara_cor,
                cv2.MORPH_CLOSE,
                kernel_fechamento,
            )
            contornos, _ = cv2.findContours(
                mascara_cor,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE,
            )

            for contorno in contornos:
                area = cv2.contourArea(contorno)
                if not self.area_minima <= area <= self.area_maxima:
                    continue

                x, y, largura, altura = cv2.boundingRect(contorno)
                if altura <= 0:
                    continue
                proporcao = largura / float(altura)
                if not self.proporcao_minima <= proporcao <= self.proporcao_maxima:
                    continue

                recorte = roi_suave[y:y + altura, x:x + largura]
                if recorte.size == 0:
                    continue
                numero_lido = self._contar_pontos(recorte)
                if not 1 <= numero_lido <= 6:
                    continue

                centro_x = x + largura / 2
                centro_y = y + altura / 2
                distancia = (
                    np.hypot(
                        centro_x - centro_roi_x,
                        centro_y - centro_roi_y,
                    )
                    / diagonal_roi
                )
                quadratura = max(0.0, 1.0 - abs(1.0 - proporcao))
                pontuacao = (
                    area
                    * (0.70 + 0.30 * quadratura)
                    * (1.0 - 0.35 * distancia)
                )
                qualidade = max(
                    0.0,
                    min(1.0, 0.60 * quadratura + 0.40 * (1.0 - distancia)),
                )

                candidatos.append(
                    {
                        "cor": nome_cor,
                        "numero": numero_lido,
                        "cor_bgr": cor_bgr,
                        "x": x + x_roi1,
                        "y": y + y_roi1,
                        "largura": largura,
                        "altura": altura,
                        "area": area,
                        "pontuacao": pontuacao,
                        "qualidade_geometrica": qualidade,
                    }
                )

        if not candidatos:
            self._desenhar_overlay_zona(frame, coords, False)
            return frame, False, None

        alvo = max(candidatos, key=lambda item: item["pontuacao"])
        status = (
            "APROVADO"
            if alvo["cor"] in self.cores_permitidas
            and alvo["numero"] in self.numeros_permitidos
            else "REJEITADO"
        )

        self._desenhar_overlay_zona(frame, coords, True)
        self._desenhar_alvo(frame, alvo, status)

        info_peca = {
            "cor": alvo["cor"],
            "numero": alvo["numero"],
            "status": status,
            "area": int(alvo["area"]),
            "qualidade_geometrica": round(
                float(alvo["qualidade_geometrica"]), 3
            ),
            "caixa": (
                alvo["x"],
                alvo["y"],
                alvo["largura"],
                alvo["altura"],
            ),
        }
        return frame, True, info_peca
