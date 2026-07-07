@echo off
title BroserAuto Web
chcp 65001 >nul 2>&1

echo.
echo  BroserAuto - Automacao Web
echo  ==============================
echo.

REM Try Python 3 first (native implementation)
py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo  Usando Python...
    echo.
    py -3 main.py
    goto :end
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo  Usando Python...
    echo.
    python main.py
    goto :end
)

REM Fallback to Node.js
node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo  Usando Node.js...
    echo.
    node server.js
    goto :end
)

echo  ERRO: Nenhum runtime encontrado.
echo.
echo  Instale Python 3 (https://python.org) ou Node.js (https://nodejs.org)
echo  para rodar o BroserAuto.
echo.
pause

:end
