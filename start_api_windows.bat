@echo off
echo Ativando o ambiente Brabo...

call activate brabo


echo Navegando para o diretório do script...
cd /d "%~dp0"

echo Iniciando o servidor FastAPI...
fastapi dev main_api.py --port 8003

pause
