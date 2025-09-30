import os
import io
import uuid # Importa o módulo uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from weasyprint import HTML
from google.cloud import storage

app = Flask(__name__)
CORS(app)

# Variável de ambiente para o nome do bucket do Cloud Storage
BUCKET_NAME = os.environ.get('CLOUD_STORAGE_BUCKET')

@app.route('/', methods=['GET'])
def health_check():
    return 'PDF Service is running.'

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        if not BUCKET_NAME:
            raise ValueError("CLOUD_STORAGE_BUCKET environment variable is not set.")

        html_content = request.data.decode('utf-8')
        pdf_file = HTML(string=html_content).write_pdf()

        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Gera um nome de arquivo único usando UUID
        unique_filename = f"relatorios/{uuid.uuid4()}.pdf"
        
        blob = bucket.blob(unique_filename)
        blob.upload_from_file(io.BytesIO(pdf_file), content_type='application/pdf')
        
        public_url = blob.public_url

        return jsonify({'message': 'PDF gerado e armazenado com sucesso!', 'pdf_url': public_url}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 500
    except Exception as e:
        print(f"Erro ao gerar o PDF: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)