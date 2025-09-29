import os
from flask import Flask, Request, jsonify
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
import base64
import sendgrid
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition

# --- CONFIGURAÇÃO ---
# No ambiente de produção, a chave de API deve ser acessada do Google Cloud Secret Manager.
# Para testes locais, você pode usar os.getenv('SENDGRID_API_KEY') e um arquivo .env.
SENDGRID_API_KEY = "SUA_CHAVE_DE_API_DO_SENDGRID" # Substitua pela sua chave

# Crie uma instância do aplicativo Flask
app = Flask(__name__)

# A função que contém a sua lógica de negócio
def processar_pagina_e_enviar_email_logica(request: Request):
    # 1. TRATAMENTO DA REQUISIÇÃO
    try:
        request_json = request.get_json(silent=True)
        
        if not request_json or 'url' not in request_json or 'email' not in request_json:
            return jsonify({'erro': 'Campos "url" e "email" são obrigatórios.'}), 400

        url = request_json['url']
        email_destino = request_json['email']
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar a requisição: {e}'}), 400

    # 2. EXTRAÇÃO E GERAÇÃO DE PDF
    try:
        response = requests.get(url)
        response.raise_for_status()

        html_content = response.text
        
        pdf_bytes = HTML(string=html_content).write_pdf()

    except requests.exceptions.RequestException as e:
        return jsonify({'erro': f'Erro ao acessar a URL: {e}'}), 500
    except Exception as e:
        return jsonify({'erro': f'Erro ao gerar o PDF: {e}'}), 500

    # 3. ENVIO DO E-MAIL
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

        encoded_file = base64.b64encode(pdf_bytes).decode('utf-8')
        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('relatorio.pdf'),
            FileType('application/pdf'),
            Disposition('attachment')
        )

        mail = Mail(
            from_email='noreply@seudominio.com',
            to_emails=email_destino,
            subject='Seu Relatório em PDF',
            html_content='<strong>Olá,</strong><p>Segue em anexo o relatório que você solicitou.</p>'
        )
        mail.attachment = attachedFile

        response = sg.client.mail.send.post(request_body=mail.get())

        if response.status_code == 202:
            return jsonify({'status': 'sucesso', 'mensagem': 'E-mail enviado com sucesso.'}), 202
        else:
            return jsonify({'status': 'erro', 'mensagem': f'Erro ao enviar o e-mail: {response.body}'}), response.status_code

    except Exception as e:
        return jsonify({'erro': f'Erro inesperado ao enviar o e-mail: {e}'}), 500

# Esta rota irá expor sua função para a web
@app.route('/', methods=['POST'])
def handle_request():
    return processar_pagina_e_enviar_email_logica(app.request)

# Esta é a parte nova para o Cloud Run / Cloud Functions 2ª Geração
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))