@echo off
echo ========================================
echo   PIPELINE DE RELATÓRIOS
echo ========================================
echo.
echo Executando o pipeline de relatórios...
echo.

REM Ativar ambiente virtual
call .\.venv\Scripts\activate.bat

REM Executar o pipeline
python main.py %*

echo.
echo ========================================
echo   EXECUÇÃO CONCLUÍDA
echo ========================================
