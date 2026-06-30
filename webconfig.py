import pyautogui as py
import time
import logging as log
from config import CONFIG_GERAL, POSICOES_TELA
from pynput import mouse

logger = log.getLogger(__name__)


class AutomacaoWeb:
    """Classe responsável por automatizar a criação de usuários via interface web."""

    def __init__(self):
        # Ativa o modo FAILSAFE: mover o mouse para o canto da tela interrompe a execução
        py.FAILSAFE = True
        py.PAUSE = CONFIG_GERAL["DELAY_POR_ACAO"]
    
    def registrar_posicao_clique(self, x: int, y: int, button, pressed: bool) -> bool:
        if pressed:
            self.clique = (x, y)
            return False  # Interrompe o listener após o clique
        return True

    def calibrar_posicoes(self, sistema: str) -> dict:
        """Executa a calibragem interativa das posições dos botões e campos na tela.
        
        Este método deve ser executado apenas na primeira utilização da automação
        ou quando a resolução/layout do sistema alvo for alterado.
        Após a calibragem, as posições são salvas em um arquivo JSON para reuso.
        
        Args:
            sistema: Nome do sistema alvo (ex.: 'azure')
            
        Returns:
            Dicionário com as posições calibradas de cada campo/botão
        """
        logger.info(f"---- INICIANDO A CALIBRAGEM DE {sistema} ----")
        for campo, _ in POSICOES_TELA.items():
            print(f"Clique em '{campo}' para calibrá-lo")
            with mouse.Listener(on_click=self.registrar_posicao_clique) as listener:
                listener.join()
            POSICOES_TELA[campo] = self.clique
            logger.info(f'Posição de {campo} calibrada para {self.clique}')
        return POSICOES_TELA

    def capturar_erro_tela(self, nome_usuario: str) -> None:
        """Captura um screenshot da tela no momento da falha para diagnóstico.
        
        Args:
            nome_usuario: Nome do usuário que estava sendo processado no momento do erro
        """
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        arquivo_gravacao = f"data/logs/Erro_{nome_usuario}-{timestamp}.png"
        py.screenshot(arquivo_gravacao)
        logger.info(f"Screenshot de erro salvo em: {arquivo_gravacao}")

    def criar_usuario(
        self,
        nome_email: str,
        nome_exibicao: str,
        posicoes: dict,
        senha_auto: bool = False,
        senha: str = ""
    ) -> bool:
        """Executa a automação de criação de um usuário no sistema alvo.
        
        O fluxo consiste em:
        1. Preencher o campo de e-mail
        2. Preencher o campo de nome de exibição
        3. Opcionalmente, definir senha manualmente (se senha_auto for False)
        4. Clicar em 'Examinar' e depois em 'Criar Usuário'
        
        Args:
            nome_email: Prefixo do e-mail do usuário
            nome_exibicao: Nome de exibição do usuário
            posicoes: Dicionário com coordenadas dos campos/botões na tela
            senha_auto: Se True, usa senha gerada automaticamente pelo sistema
            senha: Senha manual (usada apenas se senha_auto for False)
            
        Returns:
            True se o usuário foi criado com sucesso, False caso contrário
        """
        try:
            # --- Etapa 1: Inserção do nome de e-mail do usuário ---
            py.click(posicoes["campo_nomeEmail"])
            py.hotkey("ctrl", "a")  # Seleciona todo o conteúdo existente
            py.write(nome_email, interval=CONFIG_GERAL["DELAY_DIGITACAO"])
            time.sleep(1)

            # --- Etapa 2: Inserção do nome de exibição do usuário ---
            py.click(posicoes["campo_nomeExibicao"])
            py.hotkey("ctrl", "a")
            py.write(nome_exibicao, interval=CONFIG_GERAL["DELAY_DIGITACAO"])
            time.sleep(1)

            # --- Etapa 3: Definição da senha ---
            if senha_auto is False:
                py.click(posicoes["botao_senhaAuto"])
                py.click(posicoes["campo_senha"])
                py.write(senha, interval=CONFIG_GERAL["DELAY_DIGITACAO"])

            # --- Etapa 4: Confirmação da criação do usuário ---
            time.sleep(0.5)
            py.click(posicoes['botao_examinar'])
            time.sleep(0.5)
            py.click(posicoes['botao_criarUsuario'])
            return True

        except Exception as ex:
            logger.error(f"Erro ao criar o(a) usuário(a) '{nome_exibicao}': {str(ex)}")
            self.capturar_erro_tela(nome_exibicao)
            return False