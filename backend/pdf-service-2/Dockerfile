# Usa uma imagem base oficial do Python que é adequada para aplicações web.
# Usamos a versão "slim" para um tamanho de imagem menor.
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Instala as dependências de sistema operacional necessárias para o WeasyPrint.
# Essas são as bibliotecas (Pango, HarfBuzz, Cairo, GDK-Pixbuf)
# que causam o erro de dependência.
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libharfbuzz0b \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0

# Copia o arquivo de dependências e instala as bibliotecas Python.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da sua aplicação para o contêiner.
COPY . .

# Expõe a porta que a aplicação irá escutar. O Cloud Run exige isso.
EXPOSE 8080

# Define a variável de ambiente PORT que o Flask usa.
# O valor 8080 é o padrão no Cloud Run.
ENV PORT=8080

# Comando para iniciar a aplicação.
# O Gunicorn é um servidor de produção mais robusto que o servidor de desenvolvimento do Flask.
# Ele serve a aplicação `app` definida no seu arquivo `main.py`.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]