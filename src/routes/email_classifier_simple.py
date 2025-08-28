from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import json
import re

email_classifier_bp = Blueprint('email_classifier', __name__)

def classify_email_simple(email_text):
    """
    Classificação simples baseada em palavras-chave e padrões
    """
    email_lower = email_text.lower()
    
    # Palavras-chave que indicam emails improdutivos
    spam_keywords = [
        'promoção', 'desconto', 'oferta', 'grátis', 'ganhe', 'clique aqui',
        'urgente', 'limitada', 'exclusiva', 'selecionado', 'parabéns',
        'prêmio', 'sorteio', 'loteria', 'dinheiro', 'investimento',
        'viagra', 'remédio', 'medicamento', 'empréstimo', 'crédito'
    ]
    
    # Palavras-chave que indicam emails produtivos
    work_keywords = [
        'reunião', 'projeto', 'relatório', 'apresentação', 'deadline',
        'cronograma', 'orçamento', 'cliente', 'contrato', 'proposta',
        'agenda', 'meeting', 'kpi', 'meta', 'objetivo', 'estratégia',
        'planejamento', 'equipe', 'departamento', 'gerente', 'diretor'
    ]
    
    # Padrões de spam
    spam_patterns = [
        r'[🎉🔥✨⏰👆💰🎁]',  # Emojis excessivos
        r'[A-Z]{3,}',  # Palavras em maiúscula
        r'!!!+',  # Múltiplas exclamações
        r'www\.[a-z-]+\.com',  # Links suspeitos
        r'\d+%',  # Percentuais (descontos)
    ]
    
    spam_score = 0
    work_score = 0
    
    # Contar palavras-chave de spam
    for keyword in spam_keywords:
        spam_score += email_lower.count(keyword)
    
    # Contar palavras-chave de trabalho
    for keyword in work_keywords:
        work_score += email_lower.count(keyword)
    
    # Verificar padrões de spam
    for pattern in spam_patterns:
        if re.search(pattern, email_text):
            spam_score += 2
    
    # Verificar se tem domínio corporativo
    if re.search(r'@[a-zA-Z0-9-]+\.(com|org|gov|edu)\.br', email_text):
        work_score += 3
    
    # Verificar se tem assinatura profissional
    if re.search(r'(atenciosamente|cordialmente|abraços)', email_lower):
        work_score += 1
    
    # Determinar classificação
    if work_score > spam_score:
        categoria = "Produtivo"
        confianca = "Alta" if work_score >= 3 else "Média"
        sugestao = "Email relacionado ao trabalho. Recomendo responder conforme a urgência e importância do assunto."
    elif spam_score > work_score:
        categoria = "Improdutivo"
        confianca = "Alta" if spam_score >= 3 else "Média"
        sugestao = "Email promocional ou spam. Recomendo deletar ou marcar como spam."
    else:
        categoria = "Improdutivo"
        confianca = "Baixa"
        sugestao = "Classificação incerta. Recomendo revisar o conteúdo manualmente."
    
    return {
        "categoria": categoria,
        "sugestao_resposta": sugestao,
        "confianca": confianca
    }

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
        
        # Usar classificação simples
        result = classify_email_simple(email_text)
        
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

