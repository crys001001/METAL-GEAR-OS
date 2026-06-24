import json
import os

ARQUIVO_MEMORIA = "config.json"

# Agora a memória de fábrica lembra-se da câmara E das regras de qualidade!
CONFIG_FABRICA = {
    "camera_ativa": "0",
    "regras": {
        "cores": ["VERMELHO", "VERDE", "AZUL", "AMARELO"],
        "numeros": [1, 2, 3, 4, 5, 6]
    }
}

def carregar_memoria():
    if not os.path.exists(ARQUIVO_MEMORIA):
        salvar_memoria(CONFIG_FABRICA)
        return CONFIG_FABRICA
    
    try:
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return CONFIG_FABRICA

def salvar_memoria(dados_atualizados):
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(dados_atualizados, f, indent=4)