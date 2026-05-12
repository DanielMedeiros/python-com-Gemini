#!/bin/bash
echo "Configurando ambiente Gemini..."

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

echo "Ambiente configurado!"
echo "Lembre-se de configurar sua API Key no arquivo .env"