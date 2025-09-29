# Use a imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de dependência
COPY requirements.txt .

# Instala as dependências, incluindo o gunicorn
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o código da aplicação
COPY . .

# Define a variável de ambiente para o host
ENV HOST=0.0.0.0

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8080

# Define o comando para rodar a aplicação usando o gunicorn
# A flag -w 4 especifica o número de workers.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]