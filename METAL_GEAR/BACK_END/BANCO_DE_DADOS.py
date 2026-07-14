import os
import csv
from datetime import datetime

import requests
from fpdf import FPDF


class ConexaoBanco:
    """Cliente HTTP da Metal Gear API usado pelo aplicativo desktop."""

    def __init__(self):
        self.api_url = os.getenv(
            "METAL_GEAR_API_URL",
            "http://192.168.0.7:8001",
        ).rstrip("/")
        self.timeout = (5, 20)
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    @staticmethod
    def _normalizar_data_api(valor):
        if not valor:
            return None
        if isinstance(valor, datetime):
            return valor.isoformat(timespec="seconds")
        texto = str(valor).strip()
        if " " in texto and "T" not in texto:
            texto = texto.replace(" ", "T", 1)
        return texto

    @staticmethod
    def _formatar_data_interface(valor):
        if not valor:
            return ""
        if isinstance(valor, datetime):
            return valor.strftime("%d/%m/%Y %H:%M:%S")
        texto = str(valor)
        try:
            return datetime.fromisoformat(
                texto.replace("Z", "+00:00")
            ).strftime("%d/%m/%Y %H:%M:%S")
        except ValueError:
            return texto

    @staticmethod
    def _mensagem_erro(resposta):
        try:
            corpo = resposta.json()
            if isinstance(corpo, dict) and corpo.get("detail"):
                return str(corpo["detail"])
        except ValueError:
            pass
        return f"Erro HTTP {resposta.status_code}: {resposta.text[:300]}"

    def verificar_conexao(self):
        """Retorna True quando a API e o banco respondem normalmente."""
        try:
            resposta = requests.get(
                f"{self.api_url}/health",
                timeout=(2, 3),
            )
            if resposta.status_code != 200:
                return False
            corpo = resposta.json()
            return corpo.get("api") == "online" and corpo.get("banco") == "online"
        except (requests.RequestException, ValueError, TypeError):
            return False

    def salvar_peca(self, cor, numero, status):
        try:
            resposta = self.session.post(
                f"{self.api_url}/producao",
                json={
                    "cor": str(cor).upper(),
                    "numero": int(numero),
                    "status": str(status).upper(),
                },
                timeout=self.timeout,
            )
            if resposta.status_code != 201:
                print(f"Erro ao salvar peça pela API: {self._mensagem_erro(resposta)}")
                return False
            return bool(resposta.json().get("sucesso"))
        except requests.RequestException as erro:
            print(f"Erro de comunicação com a Metal Gear API: {erro}")
            return False
        except (TypeError, ValueError) as erro:
            print(f"Dados inválidos ao salvar peça: {erro}")
            return False

    def buscar_historico(self, data_inicio=None, data_fim=None):
        try:
            parametros = {"limite": 1000}
            data_inicio_api = self._normalizar_data_api(data_inicio)
            data_fim_api = self._normalizar_data_api(data_fim)

            if data_inicio_api:
                parametros["data_inicio"] = data_inicio_api
            if data_fim_api:
                parametros["data_fim"] = data_fim_api

            resposta = self.session.get(
                f"{self.api_url}/producao",
                params=parametros,
                timeout=self.timeout,
            )
            if resposta.status_code != 200:
                return False, self._mensagem_erro(resposta)

            registros = resposta.json().get("dados", [])
            dados_formatados = []
            for registro in registros:
                dados_formatados.append((
                    registro.get("id"),
                    registro.get("cor_dado", ""),
                    registro.get("numero_lido", 0),
                    registro.get("status_peca", ""),
                    self._formatar_data_interface(registro.get("data_hora")),
                ))
            return True, dados_formatados
        except requests.RequestException as erro:
            return False, f"Falha de comunicação com a API: {erro}"
        except (TypeError, ValueError, KeyError) as erro:
            return False, f"Resposta inválida recebida da API: {erro}"

    def exportar_pdf(self, caminho_arquivo, data_inicio=None, data_fim=None):
        sucesso, dados = self.buscar_historico(data_inicio, data_fim)
        if not sucesso:
            return False, dados, 0
        if len(dados) == 0:
            return False, "Nenhuma peça foi processada neste período.", 0

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Relatorio Oficial - METAL GEAR", ln=True, align="C")
            pdf.ln(5)

            pdf.set_font("Arial", "B", 10)
            pdf.cell(20, 10, "ID", border=1, align="C")
            pdf.cell(40, 10, "Cor", border=1, align="C")
            pdf.cell(30, 10, "Face", border=1, align="C")
            pdf.cell(40, 10, "Status", border=1, align="C")
            pdf.cell(50, 10, "Data/Hora", border=1, align="C")
            pdf.ln()

            pdf.set_font("Arial", "", 10)
            for linha in dados:
                pdf.cell(20, 10, str(linha[0]), border=1, align="C")
                pdf.cell(40, 10, str(linha[1]), border=1, align="C")
                pdf.cell(30, 10, str(linha[2]), border=1, align="C")
                pdf.cell(40, 10, str(linha[3]), border=1, align="C")
                pdf.cell(50, 10, str(linha[4]), border=1, align="C")
                pdf.ln()

            pdf.output(caminho_arquivo)
            return True, caminho_arquivo, len(dados)
        except Exception as erro:
            return False, str(erro), 0

    def exportar_csv(self, caminho_arquivo, data_inicio=None, data_fim=None):
        sucesso, dados = self.buscar_historico(data_inicio, data_fim)
        if not sucesso:
            return False, dados, 0
        if len(dados) == 0:
            return False, "Nenhuma peça encontrada para gerar planilha.", 0

        try:
            with open(caminho_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
                escritor = csv.writer(arquivo, delimiter=";")
                escritor.writerow(["ID", "Cor", "Face", "Status", "Data e Hora"])
                escritor.writerows(dados)
            return True, caminho_arquivo, len(dados)
        except Exception as erro:
            return False, str(erro), 0

    def limpar_tabela_producao(self):
        try:
            resposta = self.session.delete(
                f"{self.api_url}/producao",
                timeout=self.timeout,
            )
            if resposta.status_code != 200:
                print(f"Erro ao limpar tabela pela API: {self._mensagem_erro(resposta)}")
                return False
            return bool(resposta.json().get("sucesso"))
        except requests.RequestException as erro:
            print(f"Erro de comunicação com a Metal Gear API: {erro}")
            return False
