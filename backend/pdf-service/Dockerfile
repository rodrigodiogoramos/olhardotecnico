# Use a imagem base oficial do Python
FROM python:3.11

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Instala as dependências do sistema necessárias para o WeasyPrint
RUN apt-get update && \
    apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libharfbuzz-icu0 libgirepository-1.0-1

# Copia os arquivos de dependência do Python
COPY requirements.txt .

# Instala as dependências do Python, incluindo o gunicorn
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o código da aplicação
COPY . .

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8080

# Define o comando para rodar a aplicação usando o gunicorn
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8080", "app:app"]