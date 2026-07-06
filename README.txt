=== AUTOMAÇÃO DE CRIAÇÃO DE USUÁRIOS ===

Sistema automatizado para provisionamento de usuários no Microsoft Azure via interface web, utilizando PyAutoGUI para controle de mouse e teclado.

== Funcionalidades ==

- Leitura de planilha CSV com dados dos usuários
- Calibragem interativa de posições dos campos na tela
- Preenchimento automático dos campos de cadastro
- Geração de senha automática ou manual
- Controle de progresso com pausa entre usuários
- Screenshots automáticos em caso de erro
- Relatório final de sucessos e falhas

== Requisitos ==

- Python 3.8+
- Bibliotecas: pandas, pyautogui, pynput

== Instalação ==

    pip install pandas pyautogui pynput

== Estrutura de Arquivos ==

    data/
        usuarios_SENSITIVE_RAW_DATA.csv   # Base de usuários (não versionada)
        posicoes_SistemaAZURE.json         # Posições calibradas da tela
        logs/                              # Logs e screenshots de erro
    main.py                                # Script principal
    config.py                              # Configurações gerais
    webconfig.py                           # Classe de automação web
    MANUAL_DE_USO.txt                      # Manual detalhado de uso

== Uso Básico ==

    python main.py

Para mais detalhes, consulte o MANUAL_DE_USO.txt.
