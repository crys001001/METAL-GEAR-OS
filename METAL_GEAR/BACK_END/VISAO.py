import cv2
import numpy as np

class DetectorDados:
    def __init__(self):
        self.filtros_dados = {
            "AZUL": ((np.array([90, 100, 50]), np.array([130, 255, 255])), (255, 0, 0)),
            "VERDE": ((np.array([40, 70, 50]), np.array([85, 255, 255])), (0, 255, 0)),
            "AMARELO": ((np.array([20, 100, 100]), np.array([35, 255, 255])), (0, 255, 255))
        }
        
        # Estrutura inicial para receber múltiplos alvos
        self.cores_permitidas = ["VERMELHO"]
        self.numeros_permitidos = [4]

    def atualizar_regras_multiplas(self, lista_cores, lista_numeros):
        self.cores_permitidas = lista_cores
        self.numeros_permitidos = lista_numeros

    def processar_frame(self, frame):
        frame_suave = cv2.GaussianBlur(frame, (9, 9), 0)
        hsv = cv2.cvtColor(frame_suave, cv2.COLOR_BGR2HSV)

        mask_vermelho = cv2.bitwise_or(
            cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255])),
            cv2.inRange(hsv, np.array([170, 120, 70]), np.array([180, 255, 255]))
        )
        
        mascaras = {"VERMELHO": (mask_vermelho, (0, 0, 255))}
        for nome_cor, dados in self.filtros_dados.items():
            mascaras[nome_cor] = (cv2.inRange(hsv, dados[0][0], dados[0][1]), dados[1])

        peca_vista = False
        info_peca = None

        for nome_cor, (mask_cor, cor_bgr) in mascaras.items():
            contornos, _ = cv2.findContours(mask_cor, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contorno in contornos:
                if cv2.contourArea(contorno) > 2000:
                    x, y, w, h = cv2.boundingRect(contorno)
                    
                    proporcao = float(w) / h
                    if 0.7 <= proporcao <= 1.3:
                        peca_vista = True
                        cv2.rectangle(frame, (x, y), (x+w, y+h), cor_bgr, 2)
                        
                        recorte = frame_suave[y:y+h, x:x+w]
                        hsv_recorte = cv2.cvtColor(recorte, cv2.COLOR_BGR2HSV)

                        limite_min, limite_max = np.array([0, 0, 180]), np.array([180, 60, 255])
                        mask_pontos = cv2.inRange(hsv_recorte, limite_min, limite_max)
                        bolinhas, _ = cv2.findContours(mask_pontos, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                        numero_lido = 0
                        for bolinha in bolinhas:
                            area = cv2.contourArea(bolinha)
                            if 20 < area < 400:
                                perimetro = cv2.arcLength(bolinha, True)
                                if perimetro > 0:
                                    circularidade = 4 * np.pi * (area / (perimetro * perimetro))
                                    if circularidade > 0.6:
                                        numero_lido += 1

                        if numero_lido > 6: 
                            numero_lido = 6

                        # AJUSTE CIRÚRGICO: Validação dinâmica por Lote Misto
                        if nome_cor in self.cores_permitidas and numero_lido in self.numeros_permitidos:
                            status = "APROVADO"
                        else:
                            status = "REJEITADO"
                        
                        info_peca = {
                            "cor": nome_cor,
                            "numero": numero_lido,
                            "status": status
                        }

                        cv2.putText(frame, f"{nome_cor} {numero_lido}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_bgr, 2)

        return frame, peca_vista, info_peca