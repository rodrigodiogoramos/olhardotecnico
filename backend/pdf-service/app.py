import os
from flask import Flask, request, send_file
from flask_cors import CORS
from weasyprint import HTML
import io

app = Flask(__name__)
CORS(app)

# Rota de health check para a URL base
@app.route('/', methods=['GET'])
def health_check():
    return 'Service is running.'

# Rota para a API que gera o PDF
@app.route('/api/gerar-pdf', methods=['POST'])
def gerar_pdf():
    try:
        html_content = request.data.decode('utf-8')
        pdf_file = HTML(string=html_content).write_pdf()
        return send_file(
            io.BytesIO(pdf_file),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='analise-de-jogo-final.pdf'
        )
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)