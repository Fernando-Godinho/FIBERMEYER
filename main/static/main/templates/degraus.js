/**
 * Template para Degraus
 * Contém HTML e JavaScript necessários para o cálculo de degraus
 */

// Configuração do template
const DEGRAUS_CONFIG = {
    id: 'degraus_customizado',
    tipo: 'degraus',
    titulo: 'Degraus',
    categoria: 'ESTRUTURAS',
    descricao: 'Perfis I25/I38, Travessas, Reforços F4"/E, Tubos, Parafusos, Cola'
};

// HTML do formulário (versão simplificada)
const DEGRAUS_HTML = `
    <div class="mb-3">
        <label for="degraus_nome" class="form-label">Nome do Degrau *</label>
        <input type="text" class="form-control param-input" id="degraus_nome" name="nome_degrau" required>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="mb-3">
                <label for="degraus_vao" class="form-label">Vão (mm) *</label>
                <input type="number" step="0.1" class="form-control param-input" id="degraus_vao" name="vao" required min="0">
            </div>
        </div>
        <div class="col-md-6">
            <div class="mb-3">
                <label for="degraus_comprimento" class="form-label">Comprimento (mm) *</label>
                <input type="number" step="0.1" class="form-control param-input" id="degraus_comprimento" name="comprimento" required min="0">
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="mb-3">
                <label for="degraus_tempo_proc" class="form-label">Tempo Processamento (h)</label>
                <input type="number" step="0.1" class="form-control param-input" id="degraus_tempo_proc" name="tempo_proc" value="1.0" min="0">
            </div>
        </div>
        <div class="col-md-6">
            <div class="mb-3">
                <label for="degraus_tempo_mtg" class="form-label">Tempo Montagem (h)</label>
                <input type="number" step="0.1" class="form-control param-input" id="degraus_tempo_mtg" name="tempo_mtg" value="1.5" min="0">
            </div>
        </div>
    </div>
    
    <div class="mb-3">
        <label for="degraus_perda" class="form-label">Perda (%)</label>
        <input type="number" step="0.1" class="form-control param-input" id="degraus_perda" name="percentual_perda" value="3.0" min="0">
    </div>
    
    <div class="mt-3 text-center">
        <button type="button" class="btn btn-success" onclick="calcularDegraus()">
            <i class="fas fa-calculator"></i> Calcular Degraus
        </button>
    </div>
`;

// Função para carregar a interface
function carregarInterfaceDegraus() {
    console.log('=== CARREGANDO INTERFACE DEGRAUS ===');
    
    // Limpar estado anterior
    templateAtual = { 
        id: DEGRAUS_CONFIG.id, 
        tipo: DEGRAUS_CONFIG.tipo 
    };
    ultimoCalculo = null;
    
    // Configurar seletor e descrição
    document.getElementById('templateSelect').value = DEGRAUS_CONFIG.id;
    document.getElementById('templateDescription').innerHTML = `
        <h6 class="text-primary">${DEGRAUS_CONFIG.titulo}</h6>
        <small class="text-muted">Categoria: ${DEGRAUS_CONFIG.categoria}</small>
        <p class="mt-2 text-info small">
            <strong>Componentes:</strong> ${DEGRAUS_CONFIG.descricao}
        </p>
    `;
    
    // Carregar HTML do formulário
    const parametrosContainer = document.getElementById('parametrosContainer');
    parametrosContainer.innerHTML = DEGRAUS_HTML;
    
    console.log('✅ Interface Degraus carregada com sucesso');
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.carregarInterfaceDegraus = carregarInterfaceDegraus;
    window.DEGRAUS_CONFIG = DEGRAUS_CONFIG;
}