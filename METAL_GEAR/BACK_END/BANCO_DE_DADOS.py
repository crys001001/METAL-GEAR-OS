import csv
from datetime import datetime

import requests
from fpdf import FPDF


class ConexaoBanco:
    def __init__(self):
        # API hospedada no servidor CasaOS
        self.api_url = "http://192.168.0.7:8001"
        self.timeout = 10

    def salvar_peca(self, cor, numero, status):
        try:
            resposta = requests.post(
                f"{self.api_url}/producao",
                json={
                    "cor": cor,
                    "numero": numero,
                    "status": status
                },
                timeout=self.timeout
            )

            return resposta.status_code == 201

        except requests.RequestException as erro:
            print(f"Erro ao comunicar com a API: {erro}")
            return False

    def buscar_historico(self, data_inicio=None, data_fim=None):
        try:
            parametros = {
                "limite": 1000
            }

            if data_inicio:
                parametros["data_inicio"] = str(data_inicio).replace(
                    " ", "T", 1
                )

            if data_fim:
                parametros["data_fim"] = str(data_fim).replace(
                    " ", "T", 1
                )

            resposta = requests.get(
                f"{self.api_url}/producao",
                params=parametros,
                timeout=self.timeout
            )

            if resposta.status_code != 200:
                return False, f"Erro HTTP: {resposta.status_code}"

            conteudo = resposta.json()
            registros = conteudo.get("dados", [])

            dados_formatados = []

            for registro in registros:
                data_hora = registro.get("data_hora", "")

                try:
                    data_hora = datetime.fromisoformat(
                        data_hora
                    ).strftime("%d/%m/%Y %H:%M:%S")
                except (ValueError, TypeError):
                    data_hora = str(data_hora)

                dados_formatados.append((
                    registro.get("id"),
                    registro.get("cor_dado"),
                    registro.get("numero_lido"),
                    registro.get("status_peca"),
                    data_hora
                ))

            return True, dados_formatados

        except requests.RequestException as erro:
            return False, f"Erro ao comunicar com a API: {erro}"

        except (ValueError, TypeError) as erro:
            return False, f"Resposta inválida da API: {erro}"

    def exportar_pdf(
        self,
        caminho_arquivo,
        data_inicio=None,
        data_fim=None
    ):
        sucesso, dados = self.buscar_historico(
            data_inicio,
            data_fim
        )

        if not sucesso:
            return False, dados, 0

        if len(dados) == 0:
            return (
                False,
                "Nenhuma peça foi processada neste período.",
                0
            )

        try:
            pdf = FPDF()
            pdf.add_page()

            pdf.set_font("Arial", "B", 16)
            pdf.cell(
                0,
                10,
                "Relatorio Oficial - METAL GEAR",
                ln=True,
                align="C"
            )

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
                pdf.cell(
                    20,
                    10,
                    str(linha[0]),
                    border=1,
                    align="C"
                )
                pdf.cell(
                    40,
                    10,
                    str(linha[1]),
                    border=1,
                    align="C"
                )
                pdf.cell(
                    30,
                    10,
                    str(linha[2]),
                    border=1,
                    align="C"
                )
                pdf.cell(
                    40,
                    10,
                    str(linha[3]),
                    border=1,
                    align="C"
                )
                pdf.cell(
                    50,
                    10,
                    str(linha[4]),
                    border=1,
                    align="C"
                )
                pdf.ln()

            pdf.output(caminho_arquivo)

            return True, caminho_arquivo, len(dados)

        except Exception as erro:
            return False, str(erro), 0

    def exportar_csv(
        self,
        caminho_arquivo,
        data_inicio=None,
        data_fim=None
    ):
        sucesso, dados = self.buscar_historico(
            data_inicio,
            data_fim
        )

        if not sucesso:
            return False, dados, 0

        if len(dados) == 0:
            return (
                False,
                "Nenhuma peça encontrada para gerar planilha.",
                0
            )

        try:
            with open(
                caminho_arquivo,
                mode="w",
                newline="",
                encoding="utf-8-sig"
            ) as arquivo:
                escritor = csv.writer(
                    arquivo,
                    delimiter=";"
                )

                escritor.writerow([
                    "ID",
                    "Cor",
                    "Face",
                    "Status",
                    "Data e Hora"
                ])

                for linha in dados:
                    escritor.writerow(linha)

            return True, caminho_arquivo, len(dados)

        except Exception as erro:
            return False, str(erro), 0

    def limpar_tabela_producao(self):
        try:
            resposta = requests.delete(
                f"{self.api_url}/producao",
                timeout=self.timeout
            )

            if resposta.status_code != 200:
                return False

            conteudo = resposta.json()
            return conteudo.get("sucesso", False)

        except requests.RequestException as erro:
            print(f"Erro ao comunicar com a API: {erro}")
            return False