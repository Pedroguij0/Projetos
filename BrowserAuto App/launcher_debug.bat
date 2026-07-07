@echo off
title BroserAuto Web
chcp 65001 >nul 2>&1

echo.
echo  BroserAuto - Automacao Web
echo  ==============================
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo  Usando Python...
    echo.
    python main.py
    goto :end
)

node --version >nul 2>&1
if %errorlevel% equ 0 (
    echo  Usando Node.js...
    echo.
    node server.js
    goto :end
)

echo  ERRO: Nenhum runtime encontrado.
echo.
echo  Instale Node.js (https://nodejs.org) ou Python 3 (https://python.org)
echo  para rodar o BroserAuto.
echo.
echo  Node.js ja disponivel neste PC.
echo.

:end
