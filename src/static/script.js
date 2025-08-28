// Elementos DOM
const emailTextarea = document.getElementById('emailText');
const analyzeBtn = document.getElementById('analyzeBtn');
const clearBtn = document.getElementById('clearBtn');
const resultsSection = document.getElementById('resultsSection');
const resultsContent = document.getElementById('resultsContent');
const charCount = document.querySelector('.char-count');
const errorModal = document.getElementById('errorModal');
const errorMessage = document.getElementById('errorMessage');
const closeModal = document.getElementById('closeModal');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Contador de caracteres
    emailTextarea.addEventListener('input', updateCharCount);
    
    // Botão de análise
    analyzeBtn.addEventListener('click', analyzeEmail);
    
    // Botão de limpar
    clearBtn.addEventListener('click', clearText);
    
    // Modal de erro
    closeModal.addEventListener('click', hideErrorModal);
    errorModal.addEventListener('click', function(e) {
        if (e.target === errorModal) {
            hideErrorModal();
        }
    });
    
    // Tecla Enter no textarea (Ctrl+Enter para analisar)
    emailTextarea.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            analyzeEmail();
        }
    });
    
    // Inicializar contador
    updateCharCount();
});

// Atualizar contador de caracteres
function updateCharCount() {
    const count = emailTextarea.value.length;
    charCount.textContent = `${count} caracteres`;
    
    // Habilitar/desabilitar botão baseado no conteúdo
    const hasContent = emailTextarea.value.trim().length > 0;
    analyzeBtn.disabled = !hasContent;
    clearBtn.style.opacity = hasContent ? '1' : '0.5';
}

// Limpar texto
function clearText() {
    emailTextarea.value = '';
    updateCharCount();
    hideResults();
    emailTextarea.focus();
}

// Analisar email
async function analyzeEmail() {
    const emailText = emailTextarea.value.trim();
    
    if (!emailText) {
        showError('Por favor, insira o texto do email antes de analisar.');
        return;
    }
    
    // Mostrar loading
    setLoadingState(true);
    hideResults();
    
    try {
        const response = await fetch('/api/classify-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email_text: emailText
            })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `Erro HTTP: ${response.status}`);
        }
        
        if (data.success && data.resultado) {
            showResults(data.resultado);
        } else {
            throw new Error('Resposta inválida do servidor');
        }
        
    } catch (error) {
        console.error('Erro na análise:', error);
        showError(`Erro ao analisar o email: ${error.message}`);
    } finally {
        setLoadingState(false);
    }
}

// Definir estado de loading
function setLoadingState(loading) {
    if (loading) {
        analyzeBtn.classList.add('loading');
        analyzeBtn.disabled = true;
    } else {
        analyzeBtn.classList.remove('loading');
        analyzeBtn.disabled = emailTextarea.value.trim().length === 0;
    }
}

// Mostrar resultados
function showResults(resultado) {
    const { categoria, sugestao_resposta, confianca } = resultado;
    
    resultsContent.innerHTML = `
        <div class="result-card">
            <div class="result-item">
                <div class="result-label">
                    <i class="fas fa-tag"></i>
                    Classificação
                </div>
                <div class="result-value category-${categoria.toLowerCase()}">
                    ${categoria}
                </div>
            </div>
            
            <div class="result-item">
                <div class="result-label">
                    <i class="fas fa-chart-bar"></i>
                    Nível de Confiança
                </div>
                <div class="result-value confidence-${confianca.toLowerCase()}">
                    ${confianca}
                </div>
            </div>
            
            <div class="result-item">
                <div class="result-label">
                    <i class="fas fa-reply"></i>
                    Sugestão de Resposta
                </div>
                <div class="result-value">
                    ${sugestao_resposta}
                </div>
            </div>
        </div>
        
        <div style="margin-top: 20px; padding: 15px; background: #e8f4fd; border-radius: 10px; border-left: 4px solid #3498db;">
            <p style="margin: 0; color: #2c3e50; font-size: 0.9rem;">
                <i class="fas fa-info-circle" style="color: #3498db; margin-right: 8px;"></i>
                <strong>Dica:</strong> Esta análise foi gerada por IA e deve ser usada como referência. 
                Sempre use seu julgamento profissional para decisões importantes.
            </p>
        </div>
    `;
    
    resultsSection.classList.add('show');
    
    // Scroll suave para os resultados
    setTimeout(() => {
        resultsSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }, 100);
}

// Esconder resultados
function hideResults() {
    resultsSection.classList.remove('show');
}

// Mostrar erro
function showError(message) {
    errorMessage.textContent = message;
    errorModal.style.display = 'block';
}

// Esconder modal de erro
function hideErrorModal() {
    errorModal.style.display = 'none';
}

// Função para testar a conexão com o backend
async function testConnection() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('Conexão com backend:', data);
        return true;
    } catch (error) {
        console.error('Erro de conexão com backend:', error);
        return false;
    }
}

// Testar conexão ao carregar a página
testConnection();

// Adicionar algumas animações e efeitos visuais
document.addEventListener('DOMContentLoaded', function() {
    // Efeito de digitação no placeholder
    const originalPlaceholder = emailTextarea.placeholder;
    
    emailTextarea.addEventListener('focus', function() {
        if (this.value === '') {
            this.placeholder = 'Digite ou cole o texto do email aqui...';
        }
    });
    
    emailTextarea.addEventListener('blur', function() {
        if (this.value === '') {
            this.placeholder = originalPlaceholder;
        }
    });
    
    // Efeito de hover nos cards de resultado
    document.addEventListener('mouseover', function(e) {
        if (e.target.closest('.result-card')) {
            e.target.closest('.result-card').style.transform = 'translateX(5px)';
        }
    });
    
    document.addEventListener('mouseout', function(e) {
        if (e.target.closest('.result-card')) {
            e.target.closest('.result-card').style.transform = 'translateX(0)';
        }
    });
});

