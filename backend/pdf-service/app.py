import os
from flask import Flask, request, send_file
from weasyprint import HTML
import io

app = Flask(__name__)

# Rota para a API que gera o PDF
@app.route('/api/gerar-pdf', methods=['POST'])
def gerar_pdf():
    try:
        # Recebe o HTML do corpo da requisição POST
        html_content = request.data.decode('utf-8')

        # Converte o HTML para PDF em memória
        pdf_file = HTML(string=html_content).write_pdf()

        # Envia o arquivo PDF como resposta
        return send_file(
            io.BytesIO(pdf_file),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='analise-de-jogo-final.pdf'
        )
    except Exception as e:
        # Em caso de erro, retorna uma resposta com o status de erro
        return {"error": str(e)}, 500

# Executa a aplicação Flask
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)