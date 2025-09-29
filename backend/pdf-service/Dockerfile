# Use a imagem base oficial do Python
FROM python:3.11-slim

# Define o diret¢rio de trabalho no contˆiner
WORKDIR /app

# Copia os arquivos de dependˆncia
COPY requirements.txt .

# Instala as dependˆncias
RUN pip install --no-cache-dir -r requirements.txt

# Copia o c¢digo da aplica‡Æo
COPY . .

# Define a vari vel de ambiente para o host
ENV HOST=0.0.0.0

# Expäe a porta que o Flask vai usar
EXPOSE 8080

# Define o comando para rodar a aplica‡Æo
