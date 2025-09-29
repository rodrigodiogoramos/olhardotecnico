# Use a imagem base oficial do Python
FROM python:3.11

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Instala as dependências do sistema necessárias para o WeasyPrint
RUN apt-get update && \
    apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-xlib-2.0-0 libffi-dev

# Copia os arquivos de dependência do Python
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8080

# Define o comando para rodar a aplicação usando o gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]