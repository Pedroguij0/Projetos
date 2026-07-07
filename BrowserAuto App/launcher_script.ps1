Write-Host ""
Write-Host "  BroserAuto - Automacao Web" -ForegroundColor Cyan
Write-Host "  ==============================" -ForegroundColor Cyan
Write-Host ""

try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Usando Node.js..." -ForegroundColor Green
        Write-Host ""
        node server.js
        exit
    }
} catch {}

try {
    $pyVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Usando Python..." -ForegroundColor Green
        Write-Host ""
        python main.py
        exit
    }
} catch {}

Write-Host "  ERRO: Nenhum runtime encontrado." -ForegroundColor Red
Write-Host ""
Write-Host "  Instale Node.js (https://nodejs.org) ou Python 3 (https://python.org)"
Write-Host "  para rodar o BroserAuto."
Read-Host "  Pressione Enter para sair"
