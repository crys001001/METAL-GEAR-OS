import mysql.connector
from mysql.connector import Error
from fpdf import FPDF
from datetime import datetime
import csv 

class ConexaoBanco:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'metal_gear_db'
        self.user = 'root'
        self.password = 'Locadora123$' 

    def salvar_peca(self, cor, numero, status):
        try:
            conexao = mysql.connector.connect(
                host=self.host, database=self.database, user=self.user, password=self.password
            )
            if conexao.is_connected():
                cursor = conexao.cursor()
                comando_sql = "INSERT INTO producao (cor_dado, numero_lido, status_peca) VALUES (%s, %s, %s)"
                cursor.execute(comando_sql, (cor, numero, status))
                conexao.commit()
                cursor.close()
                conexao.close()
                return True
        except Error as erro:
            print(f"Erro Crítico no Banco: {erro}")
            return False

    def buscar_historico(self, data_inicio=None, data_fim=None):
        try:
            conexao = mysql.connector.connect(
                host=self.host, database=self.database, user=self.user, password=self.password
            )
            if conexao.is_connected():
                cursor = conexao.cursor()
                comando_sql = "SELECT id, cor_dado, numero_lido, status_peca, data_hora FROM producao WHERE 1=1"
                filtros = []

                if data_inicio:
                    comando_sql += " AND data_hora >= %s"
                    filtros.append(data_inicio)
                if data_fim:
                    comando_sql += " AND data_hora <= %s"
                    filtros.append(data_fim)

                comando_sql += " ORDER BY id DESC LIMIT 1000" 
                cursor.execute(comando_sql, tuple(filtros))
                linhas = cursor.fetchall()
                
                dados_formatados = []
                for linha in linhas:
                    dt = linha[4]
                    if isinstance(dt, datetime):
                        dt_str = dt.strftime('%d/%m/%Y %H:%M:%S')
                    else:
                        dt_str = str(dt)
                    dados_formatados.append((linha[0], linha[1], linha[2], linha[3], dt_str))
                
                cursor.close()
                conexao.close()
                return True, dados_formatados
        except Error as erro:
            return False, str(erro)

    def exportar_pdf(self, caminho_arquivo, data_inicio=None, data_fim=None):
        sucesso, dados = self.buscar_historico(data_inicio, data_fim)
        if not sucesso: return False, dados, 0
        if len(dados) == 0: return False, "Nenhuma peça foi processada neste período.", 0

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
        if not sucesso: return False, dados, 0
        if len(dados) == 0: return False, "Nenhuma peça encontrada para gerar planilha.", 0

        try:
            with open(caminho_arquivo, mode='w', newline='', encoding='utf-8-sig') as arquivo:
                escritor = csv.writer(arquivo, delimiter=';')
                escritor.writerow(["ID", "Cor", "Face", "Status", "Data e Hora"])
                for linha in dados:
                    escritor.writerow(linha)
            return True, caminho_arquivo, len(dados)
        except Exception as erro:
            return False, str(erro), 0

    def limpar_tabela_producao(self):
        try:
            conexao = mysql.connector.connect(
                host=self.host, database=self.database, user=self.user, password=self.password
            )
            if conexao.is_connected():
                cursor = conexao.cursor()
                cursor.execute("DELETE FROM producao") 
                conexao.commit()
                cursor.close()
                conexao.close()
                return True
        except Error:
            return False