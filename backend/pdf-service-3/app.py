import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SENDER_EMAIL = "rodrigodiogoramos@gmail.com"
SENDER_PASSWORD = "SUA_SENHA_DE_APLICATIVO_AQUI"
RECIPIENT_EMAIL = "rodrigodiogoramos@gmail.com"

@app.route('/', methods=['GET'])
def health_check():
    return 'Email Service is running.'

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        html_content = data.get('html_content', 'Conteúdo HTML vazio.')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Relatório de Análise de Jogo"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL

        part1 = MIMEText(html_content, 'html')
        msg.attach(part1)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)

        return jsonify({'message': 'Email enviado com sucesso!'}), 200

    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)