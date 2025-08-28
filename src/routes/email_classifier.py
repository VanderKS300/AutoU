from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import openai
import os
import json

email_classifier_bp = Blueprint('email_classifier', __name__)

# Configuração do cliente OpenAI
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE')
)

@email_classifier_bp.route('/classify-email', methods=['POST'])
@cross_origin()
def classify_email():
    try:
        # Obter o texto do email do request
        data = request.get_json()
        if not data or 'email_text' not in data:
            return jsonify({'error': 'Texto do email é obrigatório'}), 400
        
        email_text = data['email_text']
        
        if not email_text.strip():
            return jsonify({'error': 'Texto do email não pode estar vazio'}), 400
        
        # Prompt para a IA
        prompt = f"""
        Você é um assistente especializado em classificação de emails corporativos. 
        Analise o seguinte email e determine se ele é PRODUTIVO ou IMPRODUTIVO para o ambiente de trabalho.
        
        Critérios:
        - PRODUTIVO: Emails relacionados a trabalho, projetos, reuniões, decisões importantes, informações relevantes para o negócio
        - IMPRODUTIVO: Spam, promoções, emails pessoais, correntes, piadas, conteúdo irrelevante para o trabalho
        
        Além da classificação, gere uma sugestão de resposta apropriada e profissional.
        
        Email para análise:
        {email_text}
        
        Retorne APENAS um objeto JSON válido com esta estrutura:
        {{
            "categoria": "Produtivo" ou "Improdutivo",
            "sugestao_resposta": "Uma resposta curta e apropriada ao email",
            "confianca": "Alta" ou "Média" ou "Baixa"
        }}
        """
        
        # Chamada para a API da OpenAI
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em classificação de emails. Sempre responda apenas com JSON válido."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )
        
        # Extrair a resposta
        ai_response = response.choices[0].message.content.strip()
        
        # Tentar fazer parse do JSON
        try:
            result = json.loads(ai_response)
        except json.JSONDecodeError:
            # Se não conseguir fazer parse, criar uma resposta padrão
            result = {
                "categoria": "Improdutivo",
                "sugestao_resposta": "Email analisado. Recomendo revisar o conteúdo.",
                "confianca": "Baixa"
            }
        
        return jsonify({
            'success': True,
            'resultado': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro interno do servidor: {str(e)}'
        }), 500

@email_classifier_bp.route('/health', methods=['GET'])
@cross_origin()
def health_check():
    return jsonify({
        'status': 'OK',
        'message': 'Serviço de classificação de emails funcionando'
    })

