# Classificador de Emails IA

Uma aplicação web completa para classificação automática de emails corporativos usando inteligência artificial.

## 📋 Descrição do Projeto

Este projeto foi desenvolvido como uma solução para automatizar a classificação de emails em ambientes corporativos, ajudando profissionais a identificar rapidamente se um email é **Produtivo** (relacionado ao trabalho) ou **Improdutivo** (spam, promoções, conteúdo irrelevante).

### ✨ Funcionalidades Principais

- **Classificação Automática**: Analisa o conteúdo do email e classifica como Produtivo ou Improdutivo
- **Nível de Confiança**: Indica o grau de certeza da classificação (Alta, Média, Baixa)
- **Sugestão de Resposta**: Fornece recomendações sobre como lidar com o email
- **Interface Moderna**: Design responsivo e intuitivo
- **Processamento em Tempo Real**: Análise instantânea do conteúdo

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.11**: Linguagem principal
- **Flask**: Framework web
- **Flask-CORS**: Suporte a requisições cross-origin
- **SQLAlchemy**: ORM para banco de dados

### Frontend
- **HTML5**: Estrutura da página
- **CSS3**: Estilização moderna com gradientes e animações
- **JavaScript (ES6+)**: Lógica de interação e comunicação com API
- **Font Awesome**: Ícones
- **Google Fonts (Inter)**: Tipografia

### Inteligência Artificial
- **Algoritmo de Classificação Baseado em Palavras-chave**: Sistema inteligente que analisa padrões de texto
- **Análise de Padrões**: Detecção de características típicas de spam e emails corporativos
- **Sistema de Pontuação**: Avaliação quantitativa para determinar a classificação

## 📁 Estrutura do Projeto

```
backend/email-classifier/
├── src/
│   ├── models/
│   │   └── user.py                    # Modelos de dados
│   ├── routes/
│   │   ├── user.py                    # Rotas de usuário
│   │   ├── email_classifier.py        # Classificador com OpenAI
│   │   └── email_classifier_simple.py # Classificador simplificado
│   ├── static/
│   │   ├── index.html                 # Interface principal
│   │   ├── styles.css                 # Estilos CSS
│   │   └── script.js                  # Lógica JavaScript
│   ├── database/
│   │   └── app.db                     # Banco de dados SQLite
│   └── main.py                        # Arquivo principal da aplicação
├── venv/                              # Ambiente virtual Python
├── requirements.txt                   # Dependências Python
└── README.md                          # Documentação
```

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone ou baixe o projeto**
   ```bash
   # Se usando git
   git clone <url-do-repositorio>
   cd backend/email-classifier
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   python -m venv venv
   
   # No Linux/Mac
   source venv/bin/activate
   
   # No Windows
   venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python src/main.py
   ```

5. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## 💡 Como Usar

1. **Abra a aplicação** no navegador
2. **Cole o texto do email** na área de texto
3. **Clique em "Analisar Email"** para processar
4. **Visualize os resultados**:
   - Classificação (Produtivo/Improdutivo)
   - Nível de confiança
   - Sugestão de resposta

### Exemplos de Uso

**Email Produtivo:**
```
Assunto: Reunião de Planejamento Q1
De: gerente@empresa.com
Para: equipe@empresa.com

Prezada equipe,
Gostaria de agendar nossa reunião de planejamento...
```

**Email Improdutivo:**
```
Assunto: 🎉 PROMOÇÃO IMPERDÍVEL! 50% OFF
De: promocoes@loja.com

OFERTA LIMITADA! Clique aqui para aproveitar...
```

## 🧠 Como Funciona a IA

O sistema utiliza um algoritmo inteligente de classificação baseado em:

### Análise de Palavras-chave
- **Palavras Produtivas**: reunião, projeto, relatório, cronograma, cliente, etc.
- **Palavras Improdutivas**: promoção, desconto, grátis, clique aqui, urgente, etc.

### Detecção de Padrões
- **Emojis excessivos**: Indicativo de spam
- **Texto em maiúsculas**: Padrão promocional
- **Links suspeitos**: URLs de promoções
- **Percentuais**: Ofertas de desconto

### Sistema de Pontuação
- Cada palavra-chave e padrão recebe uma pontuação
- O sistema compara as pontuações para determinar a classificação
- O nível de confiança é baseado na diferença entre as pontuações

## 🎨 Design e Interface

### Características do Design
- **Gradiente Moderno**: Cores azul e roxo para visual profissional
- **Cards Flutuantes**: Elementos com sombras e bordas arredondadas
- **Animações Suaves**: Transições e efeitos hover
- **Responsivo**: Adaptável a diferentes tamanhos de tela
- **Tipografia Limpa**: Fonte Inter para legibilidade

### Elementos Visuais
- Ícones Font Awesome para melhor UX
- Contador de caracteres em tempo real
- Loading spinner durante processamento
- Modal de erro para feedback ao usuário
- Cores semânticas para resultados (verde/vermelho)

## 📊 API Endpoints

### POST /api/classify-email
Classifica um email baseado no seu conteúdo.

**Request Body:**
```json
{
  "email_text": "Conteúdo do email a ser analisado"
}
```

**Response:**
```json
{
  "success": true,
  "resultado": {
    "categoria": "Produtivo",
    "sugestao_resposta": "Email relacionado ao trabalho...",
    "confianca": "Alta"
  }
}
```

### GET /api/health
Verifica o status do serviço.

**Response:**
```json
{
  "status": "OK",
  "message": "Serviço de classificação de emails funcionando"
}
```

## 🔧 Configurações Avançadas

### Personalizando a Classificação
Para ajustar os critérios de classificação, edite o arquivo `src/routes/email_classifier_simple.py`:

```python
# Adicione novas palavras-chave
spam_keywords = ['nova_palavra', ...]
work_keywords = ['nova_palavra_trabalho', ...]

# Ajuste os pesos de pontuação
spam_score += 2  # Aumentar peso
work_score += 1  # Diminuir peso
```

### Integrando com OpenAI
Para usar a versão com OpenAI (mais precisa), configure as variáveis de ambiente:

```bash
export OPENAI_API_KEY="sua_chave_aqui"
export OPENAI_API_BASE="https://api.openai.com/v1"
```

E use o arquivo `email_classifier.py` no lugar do `email_classifier_simple.py`.

## 🚀 Deploy e Produção

### Opções de Hospedagem
- **Heroku**: Plataforma simples para deploy
- **Vercel**: Ideal para aplicações Flask
- **DigitalOcean**: VPS com mais controle
- **AWS/Google Cloud**: Soluções enterprise

### Configurações de Produção
1. Configure variáveis de ambiente
2. Use um servidor WSGI (Gunicorn)
3. Configure HTTPS
4. Implemente cache para melhor performance
5. Configure monitoramento e logs

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido como projeto de demonstração de aplicação web full-stack com IA.

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório do projeto.

---

**Nota**: Este é um projeto de demonstração. Para uso em produção, considere implementar autenticação, rate limiting, e outras medidas de segurança apropriadas.

