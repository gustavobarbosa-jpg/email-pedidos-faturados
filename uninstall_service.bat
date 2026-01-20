@echo off
echo ========================================
echo   REMOVER SERVIÇO AUTOMÁTICO
echo ========================================
echo.
echo Este script remove a tarefa agendada do Windows
echo para o pipeline de relatórios
echo.
echo ATENÇÃO: Execute como Administrador
echo ========================================
echo.

set TASK_NAME=EmailReportsPipeline

echo Removendo tarefa agendada...
schtasks /delete /tn "%TASK_NAME%" /f

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Tarefa agendada removida com sucesso!
    echo 📋 O pipeline não será mais executado automaticamente
) else (
    echo.
    echo ❌ Erro ao remover tarefa agendada
    echo Verifique se executou como Administrador
    echo ou se a tarefa existe
)

echo.
pause
