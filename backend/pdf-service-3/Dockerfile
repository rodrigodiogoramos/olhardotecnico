# Usa uma imagem base Python oficial leve
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta que o Flask vai usar
EXPOSE 8080

# Comando para iniciar o servidor Flask
CMD ["python", "app.py"]