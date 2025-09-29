import os
import requests
import base64
import sendgrid
from bs4 import BeautifulSoup
from weasyprint import HTML
from flask import Flask, request, jsonify
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

# --- CONFIGURAÇÃO ---
# A chave de API do SendGrid é obtida de uma variável de ambiente.
# Isso garante que ela seja injetada de forma segura pelo Google Cloud Secret Manager.
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

# Crie a instância da aplicação Flask.
# Esta instância é o ponto de entrada que o Gunicorn irá usar.
app = Flask(__name__)

# O endpoint da sua API. Ele aceita requisições POST.
@app.route('/', methods=['POST'])
def processar_pagina_e_enviar_email():
    """
    Recebe um corpo JSON com 'url' e 'email',
    gera um PDF do HTML da URL e o envia por e-mail.
    """
    # 1. TRATAMENTO DA REQUISIÇÃO
    try:
        # Pega o corpo da requisição JSON
        request_data = request.get_json(silent=True)
        
        # Valida se os campos 'url' e 'email' estão presentes.
        if not request_data or 'url' not in request_data or 'email' not in request_data:
            return jsonify({'erro': 'Campos "url" e "email" são obrigatórios.'}), 400

        url = request_data['url']
        email_destino = request_data['email']
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar a requisição: {e}'}), 400

    # 2. EXTRAÇÃO E GERAÇÃO DE PDF
    try:
        # Faz a requisição HTTP para a URL fornecida
        response = requests.get(url)
        # Lança um erro se a requisição falhar (código de status >= 400)
        response.raise_for_status()

        # Usa o WeasyPrint para converter o conteúdo HTML em PDF
        html_content = response.text
        pdf_bytes = HTML(string=html_content).write_pdf()

    except requests.exceptions.RequestException as e:
        return jsonify({'erro': f'Erro ao acessar a URL: {e}'}), 500
    except Exception as e:
        return jsonify({'erro': f'Erro ao gerar o PDF: {e}'}), 500

    # 3. ENVIO DO E-MAIL
    try:
        if not SENDGRID_API_KEY:
            return jsonify({'erro': 'Chave de API do SendGrid não configurada.'}), 500

        # Configura o SendGrid
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        # Prepara o anexo
        encoded_file = base64.b64encode(pdf_bytes).decode('utf-8')
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('relatorio.pdf'),
            FileType('application/pdf'),
            Disposition('attachment')
        )

        # Monta o e-mail
        mail = Mail(
            from_email='noreply@seudominio.com',
            to_emails=email_destino,
            subject='Seu Relatório em PDF',
            html_content='<strong>Olá,</strong><p>Segue em anexo o relatório que você solicitou.</p>'
        )
        mail.attachment = attachedFile

        # Envia o e-mail
        response = sg.client.mail.send.post(request_body=mail.get())

        if response.status_code == 202:
            return jsonify({'status': 'sucesso', 'mensagem