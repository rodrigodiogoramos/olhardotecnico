# Use a imagem base oficial do Python
FROM python:3.11

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de dependência do Python
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8080

# Define o comando para rodar a aplicação usando o gunicorn
# A correção está na linha abaixo, usando a sintaxe padrão do Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]