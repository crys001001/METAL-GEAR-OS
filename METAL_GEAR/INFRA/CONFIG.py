import copy
import json
import os


ARQUIVO_MEMORIA = "config.json"
CORES_SUPORTADAS = {"VERMELHO", "VERDE", "AZUL"}

CONFIG_FABRICA = {
    "camera_ativa": "0",
    "regras": {
        "cores": ["VERMELHO", "VERDE", "AZUL"],
        "numeros": [1, 2, 3, 4, 5, 6],
    },
    "visao": {
        "roi": {
            "x": 0.22,
            "y": 0.16,
            "largura": 0.56,
            "altura": 0.68,
        },
        "area_minima": 1800,
        "area_maxima": 80000,
        "proporcao_minima": 0.65,
        "proporcao_maxima": 1.40,
        "area_ponto_minima": 20,
        "area_ponto_maxima": 500,
        "circularidade_minima": 0.58,
        "frames_confirmacao": 12,
        "confianca_minima": 0.75,
        "frames_vazio_liberacao": 8,
        "frames_vazio_cancelamento": 3,
        "escurecimento_externo": 0.42,
        "mostrar_mira": True,
    },
}


def _mesclar_configuracao(base, carregada):
    resultado = copy.deepcopy(base)
    if not isinstance(carregada, dict):
        return resultado
    for chave, valor in carregada.items():
        if (
            chave in resultado
            and isinstance(resultado[chave], dict)
            and isinstance(valor, dict)
        ):
            resultado[chave] = _mesclar_configuracao(resultado[chave], valor)
        else:
            resultado[chave] = valor
    return resultado


def _normalizar(dados):
    regras = dados.setdefault("regras", {})
    cores = regras.get("cores", [])
    regras["cores"] = [
        cor for cor in cores if str(cor).upper() in CORES_SUPORTADAS
    ]
    if not regras["cores"]:
        regras["cores"] = ["VERMELHO", "VERDE", "AZUL"]

    numeros = regras.get("numeros", [1, 2, 3, 4, 5, 6])
    regras["numeros"] = sorted(
        {int(numero) for numero in numeros if str(numero).isdigit() and 1 <= int(numero) <= 6}
    )
    if not regras["numeros"]:
        regras["numeros"] = [1, 2, 3, 4, 5, 6]
    return dados


def carregar_memoria():
    if not os.path.exists(ARQUIVO_MEMORIA):
        dados = copy.deepcopy(CONFIG_FABRICA)
        salvar_memoria(dados)
        return dados

    try:
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as arquivo:
            dados_salvos = json.load(arquivo)
        dados_completos = _normalizar(
            _mesclar_configuracao(CONFIG_FABRICA, dados_salvos)
        )
        if dados_completos != dados_salvos:
            salvar_memoria(dados_completos)
        return dados_completos
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return copy.deepcopy(CONFIG_FABRICA)


def salvar_memoria(dados_atualizados):
    dados_atualizados = _normalizar(dados_atualizados)
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados_atualizados,
            arquivo,
            indent=4,
            ensure_ascii=False,
        )
