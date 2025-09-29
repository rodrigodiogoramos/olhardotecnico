import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
import base64
from weasyprint import HTML
import io

app = Flask(__name__)
CORS(app)

# Variável de ambiente para a chave de API do SendGrid
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDER_EMAIL = 'rodrigodiogoramos@gmail.com'
RECIPIENT_EMAIL = 'rodrigodiogoramos@gmail.com'

@app.route('/', methods=['GET'])
def health_check():
    return 'SendGrid Service is running.'

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        if not SENDGRID_API_KEY:
            raise ValueError("SENDGRID_API_KEY environment variable is not set.")

        data = request.json
        html_content = data.get('html_content')

        if not html_content:
            return jsonify({'error': 'No HTML content provided'}), 400

        # 1. Converte o HTML para PDF em memória
        pdf_file = HTML(string=html_content).write_pdf()

        # 2. Prepara o e-mail com anexo
        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=RECIPIENT_EMAIL,
            subject='Seu Relatório de Análise de Jogo',
            html_content='<strong>Aqui está o seu relatório em anexo!</strong>'
        )

        # Codifica o PDF em base64
        encoded_file = base64.b64encode(pdf_file).decode()

        attachedFile = Attachment(
            FileContent(encoded_file),
            FileName('relatorio_analise.pdf'),
            FileType('application/pdf'),
            Disposition('attachment')
        )
        message.attachment = attachedFile

        # 3. Envia o e-mail usando a chave de API do SendGrid
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        return jsonify({'message': f"E-mail enviado com sucesso! Status Code: {response.status_code}"}), 200

    except ValueError as ve:
        print(f"Erro de configuração: {ve}")
        return jsonify({'error': str(ve)}), 500
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)