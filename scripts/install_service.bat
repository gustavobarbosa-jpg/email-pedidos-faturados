@echo off
echo ========================================
echo   INSTALADOR DO SERVIÇO AUTOMÁTICO
echo ========================================
echo.
echo Este script cria uma tarefa agendada no Windows
echo para executar o pipeline todos os dias às 09:00
echo.
echo ATENÇÃO: Execute como Administrador
echo ========================================
echo.

set SCRIPT_PATH=%~dp0schedule_pipeline.py
set TASK_NAME=EmailReportsPipeline

echo Criando tarefa agendada...
schtasks /create /tn "%TASK_NAME%" /tr "cmd /c \"cd /d %~dp0.. && scripts\schedule_pipeline.py\"" /sc daily /st 09:00 /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Tarefa agendada criada com sucesso!
    echo 📅 O pipeline será executado todos os dias às 09:00
    echo 📋 Para verificar: taskschd.msc
    echo 🗑️  Para remover: schtasks /delete /tn "%TASK_NAME%" /f
) else (
    echo.
    echo ❌ Erro ao criar tarefa agendada
    echo Verifique se executou como Administrador
)

echo.
pause
