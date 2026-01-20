@echo off
echo ========================================
echo   SCHEDULER DO PIPELINE
echo ========================================
echo.
echo Iniciando scheduler do pipeline...
echo O pipeline vai rodar todos os dias as 09:00
echo.
echo Para testar com equipe 200: python schedule_pipeline.py --test
echo Para parar: feche esta janela (Ctrl+C)
echo ========================================
echo.

python schedule_pipeline.py

pause
