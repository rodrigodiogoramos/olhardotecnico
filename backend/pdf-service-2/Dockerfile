# Use uma imagem base Debian que inclui as bibliotecas necessárias.
# wkhtmltopdf funciona melhor em ambientes Debian.
FROM debian:bullseye-slim

# Instala o Python 3.9 e o pip.
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    wkhtmltopdf

# Define o diretório de trabalho.
WORKDIR /app

# Copia e instala as dependências Python.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da sua aplicação para o contêiner.
COPY . .

# Expõe a porta e define a variável de ambiente.
EXPOSE 8080
ENV PORT=8080

# Comando para iniciar a aplicação com Gunicorn.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]