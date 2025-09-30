import os
import io
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.cloud import storage

# Inicializa o aplicativo Flask
app = Flask(__name__)
# Habilita o CORS para permitir requisições do frontend
CORS(app)

# Obtém o nome do bucket do Cloud Storage a partir de uma variável de ambiente
BUCKET_NAME = os.environ.get('CLOUD_STORAGE_BUCKET')

@app.route('/', methods=['GET'])
def health_check():
    """Endpoint para verificação de saúde do serviço."""
    return 'HTML Report Service is running.', 200

@app.route('/generate-html-report', methods=['POST'])
def generate_html_report():
    """
    Recebe o HTML, salva no Cloud Storage e retorna a URL pública.
    """
    try:
        # Verifica se a variável de ambiente do bucket está configurada
        if not BUCKET_NAME:
            raise ValueError("CLOUD_STORAGE_BUCKET environment variable is not set.")

        # Obtém o conteúdo HTML do corpo da requisição
        html_content = request.data.decode('utf-8')
        
        # Inicializa o cliente do Cloud Storage
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        
        # Gera um nome de arquivo único para evitar conflitos
        unique_filename = f"html_reports/{uuid.uuid4()}.html"
        
        # Cria um blob (objeto) no bucket e faz o upload do conteúdo HTML
        blob = bucket.blob(unique_filename)
        blob.upload_from_file(io.BytesIO(html_content.encode('utf-8')), content_type='text/html')
        
        # Define a URL pública do arquivo
        public_url = blob.public_url

        # Retorna a URL em uma resposta JSON
        return jsonify({'message': 'HTML gerado e armazenado com sucesso!', 'html_url': public_url}), 200

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 500
    except Exception as e:
        print(f"Erro ao gerar o HTML: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)