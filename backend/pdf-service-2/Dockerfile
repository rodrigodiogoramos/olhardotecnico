# Usa uma imagem base oficial do Python que é adequada para aplicações web.
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Instala as dependências de sistema operacional para o WeasyPrint.
# Essas bibliotecas (Pango, HarfBuzz, Cairo, GDK-Pixbuf) são essenciais para a renderização.
# Também incluímos bibliotecas de fontes e SSL para maior compatibilidade.
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libharfbuzz0b \
    libcairo2 \
    libgdk-pixbuf-xlib-2.0-0 \
    fonts-dejavu-core \
    libffi-dev \
    libssl-dev \
    zlib1g-dev

# Copia o arquivo de dependências e instala as bibliotecas Python.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da sua aplicação para o contêiner.
COPY . .

# Expõe a porta que a aplicação irá escutar.
EXPOSE 8080

# Define a variável de ambiente PORT que o Flask usa.
ENV PORT=8080

# Comando para iniciar a aplicação.
# O Gunicorn é um servidor de produção mais robusto que o servidor de desenvolvimento do Flask.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]