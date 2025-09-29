import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify
from premailer import transform

app = Flask(__name__)

# Configurações do ambiente de e-mail
SMTP_SERVER = 'smtp.gmail.com' # Exemplo para Gmail
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
RECIPIENT_EMAIL = 'rodrigodiogoramos@gmail.com'

@app.route('/enviar-email', methods=['POST'])
def enviar_email():
    try:
        data = request.json
        html_content = data.get('html_content')

        if not html_content:
            return jsonify({'error': 'Nenhum conteúdo HTML fornecido.'}), 400

        # Converte o CSS para estilos in-line (crucial para e-mail)
        inline_html = transform(html_content)

        # Cria a mensagem de e-mail
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Relatório Importante: Seu Resultado"
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL

        # Anexa o HTML ao e-mail
        part = MIMEText(inline_html, 'html')
        msg.attach(part)

        # Envia o e-mail via SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

        return jsonify({'message': 'E-mail enviado com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))