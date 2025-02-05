#!/bin/bash

# Espera o PostgreSQL iniciar na porta 5432
echo "Waiting for PostgreSQL to start..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Inicializa o banco de dados
python3 -c "from app import init_db; init_db()"

# Inicia a aplicação
flask run --host=0.0.0.0 