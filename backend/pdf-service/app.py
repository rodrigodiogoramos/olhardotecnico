import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask import Flask, request, jsonify
from weasyprint import HTML

app = Flask(__name__)

# Configurações para o envio de e-mail
SENDER_EMAIL = "rodrigodiogoramos@gmail.com"
SENDER_PASSWORD = "SEU_APP_PASSWORD_AQUI" # Utilize uma senha de aplicativo do Gmail

@app.route('/send_pdf_email', methods=['POST'])
def send_pdf_email():
    try:
        data = request.json
        html_content = data.get('html_content')
        recipient_email = "rodrigodiogoramos@gmail.com"
        subject = "Seu Relatório de Análise de Jogo"

        if not html_content:
            return jsonify({'error': 'No HTML content provided'}), 400

        # 1. Converte o HTML para PDF
        pdf_file = HTML(string=html_content).write_pdf()

        # 2. Configura o e-mail
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # 3. Adiciona o PDF como anexo
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_file)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="relatorio_analise.pdf"')
        msg.attach(part)

        # 4. Envia o e-mail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)

        return jsonify({'message': 'PDF gerado e enviado com sucesso!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # O Gunicorn definirá a porta, então em produção a porta não será 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)