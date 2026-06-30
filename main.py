import pandas as pd
from webconfig import AutomacaoWeb
from config import CONFIG_GERAL
import logging as log
import json
import time
from pathlib import Path

logger = log.getLogger(__name__)


def carregar_usuarios(caminho_csv: str) -> pd.DataFrame:
    """Carrega a planilha com a base de usuários a serem criados.
    
    O arquivo CSV deve conter as colunas:
        - nome_exibicao: Nome de exibição do usuário
        - nome_email: Prefixo do e-mail
        - senha: Senha do usuário
        - criado: Flag indicando se o usuário já foi criado (True/False)
    
    Requisitos de senha (a serem validados externamente):
        - Mínimo 8 caracteres
        - Deve conter ao menos 3 dos 4 tipos: minúsculas, maiúsculas, números, símbolos
        - Não deve ser fraca ou comumente usada
    
    Args:
        caminho_csv: Caminho do arquivo CSV com os dados dos usuários
        
    Returns:
        DataFrame com os dados carregados
        
    Raises:
        Exception: Se houver erro na leitura do arquivo
    """
    try:
        db = pd.read_csv(caminho_csv, sep=';')
        logger.info(f"{len(db)} usuários carregados da planilha '{caminho_csv}'")
        return db
    except Exception as ex:
        logger.error(f"Falha ao carregar o arquivo de usuários: {ex}")
        raise


def main():
    """Função principal que orquestra o fluxo completo de automação."""
    logger.info("---- INICIANDO AUTOMAÇÃO DE CRIAÇÃO DE USUÁRIOS ----")
    automacao_criacao = AutomacaoWeb()

    # --- Seleção do sistema ---
    while True:
        sistema = str(input(
            "Digite o nome do sistema para provisionamento:\n"
            "1 - Azure\n"
        ))
        sistema = sistema.lower()
        if sistema == "azure":
            break
        else:
            print("Opção inválida. Digite apenas as opções disponíveis.")

    # --- Carregamento ou calibragem das posições de tela ---
    arquivo_posicoes = Path(f"data/posicoes_Sistema{sistema.upper()}.json")
    if arquivo_posicoes.exists():
        with open(arquivo_posicoes, 'r') as f:
            posicoes = json.load(f)
        logger.info(f"Posições carregadas de: {arquivo_posicoes}")
    else:
        logger.info(
            "----- ARQUIVO DE POSIÇÕES NÃO ENCONTRADO -----\n"
            "===== INICIANDO CALIBRAGEM DO SISTEMA ====="
        )
        posicoes = automacao_criacao.calibrar_posicoes(sistema)
        with open(arquivo_posicoes, 'w') as f:
            json.dump(posicoes, f, indent=2)
        logger.info(f"Posições de tela salvas em: {arquivo_posicoes}")

    # --- Carregamento da base de usuários ---
    caminho_csv = 'data/usuarios_SENSITIVE_RAW_DATA.csv'
    base_usuarios = carregar_usuarios(caminho_csv)

    input('===== PRESSIONE ENTER PARA INICIAR A AUTOMAÇÃO (POSICIONE A TELA DO SISTEMA) =====')
    time.sleep(3)

    # --- Loop principal de criação ---
    sucessos = 0
    fracassos = 0
    for i, row in base_usuarios.iterrows():
        if row['criado'] is False or str(row['criado']).strip().lower() == 'false':
            logger.info(f"Criando usuário: {row['nome_exibicao']}")
            print("Você tem 5 segundos para garantir que a tela do sistema está visível...")
            time.sleep(CONFIG_GERAL["DELAY_CRIACAO_USUARIO"])
            resultado = automacao_criacao.criar_usuario(
                nome_email=row['nome_email'],
                nome_exibicao=row['nome_exibicao'],
                senha=row['senha'],
                posicoes=posicoes
            )
            if resultado:
                sucessos += 1
                base_usuarios.at[i, 'criado'] = True
                base_usuarios.to_csv(caminho_csv, sep=';', index=False)
                logger.info(f"Usuário '{row['nome_exibicao']}' marcado como criado no CSV.")
            else:
                fracassos += 1
        confirmacao = str(input(
            f"\nJá foram processados {i + 1} usuário(s).\n"
            "Deseja continuar? (s/n): "
        ))
        while True:
            if confirmacao.lower() == "n":
                logger.info("Automação interrompida pelo usuário.")
                return
            elif confirmacao.lower() == "s":
                logger.info(f"{i + 1} usuário(s) criado(s). Prosseguindo...")
                time.sleep(CONFIG_GERAL["DELAY_CRIACAO_USUARIO"])
                break
            else:
                confirmacao = input("Resposta inválida. Digite 's' para continuar ou 'n' para parar: ")

    # --- Relatório final ---
    total = sucessos + fracassos
    logger.info(
        f"\n"
        f"========== RELATÓRIO FINAL ==========\n"
        f"  SUCESSOS: {sucessos}\n"
        f"  FALHAS:   {fracassos}\n"
        f"  TOTAL:    {total}\n"
        f"=====================================\n"
    )


if __name__ == "__main__":
    while True:
        print("\n=== AUTOMAÇÃO DE CRIAÇÃO DE USUÁRIOS ===")
        print("ATENÇÃO: Esta automação controlará o mouse e teclado.")
        print("Para interromper, mova o mouse para um dos cantos da tela.")
        confirmacao = input("Digite SIM para iniciar a automação: ")
        if confirmacao.upper() == "SIM":
            main()
        else:
            conf = input("Tem certeza que deseja cancelar? (s/n): ")
            if conf.lower() == "s":
                print("Automação cancelada.")
                break
            elif conf.lower() != "n":
                print("Resposta inválida. Digite 's' ou 'n'.")
else:
    print("Execute este script diretamente (não como módulo).")