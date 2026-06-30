import logging as log
from pathlib import Path

CONFIG_GERAL = {
    "DELAY_POR_ACAO": 0.5,        
    "DELAY_DIGITACAO": 0.2,      
    "DELAY_CRIACAO_USUARIO": 3, 
    "TEMPO_ESPERA_MAX": 10       
}

Path('data/logs').mkdir(parents=True, exist_ok=True)
log.basicConfig(
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d',
    handlers=[
        log.FileHandler(Path('data/logs/registros.log'), encoding='utf-8'),
        log.StreamHandler()
    ]
)

POSICOES_TELA = {
    "campo_nomeEmail": None,
    "campo_nomeExibicao": None,
    "campo_senha": None,
    "botao_senhaAuto": None,
    "botao_examinar": None,
    "botao_criarUsuario": None
}