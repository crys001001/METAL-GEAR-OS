import logging
import os
from datetime import datetime

def iniciar_caixa_preta():
    # Cria a pasta 'logs' automaticamente se ela não existir
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Cria um arquivo de log novo por dia (ex: metal_gear_2026-06-23.log)
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    arquivo_log = f"logs/metal_gear_{data_hoje}.log"
    
    # Configura como as mensagens vão aparecer
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        handlers=[
            logging.FileHandler(arquivo_log, encoding='utf-8'), # Salva no arquivo texto
            logging.StreamHandler()                             # E continua a mostrar no terminal do VS Code
        ]
    )
    return logging.getLogger("MetalGearOS")