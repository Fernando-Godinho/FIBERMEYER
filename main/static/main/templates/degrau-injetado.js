/**
 * Template para Degrau Injetado
 * Contém HTML e JavaScript necessários para o cálculo de degrau injetado
 */

// Configuração do template
const DEGRAU_INJETADO_CONFIG = {
    id: 'degrau_injetado_customizado',
    tipo: 'degrau_injetado',
    titulo: 'Degrau Injetado',
    categoria: 'ESTRUTURAS',
    descricao: 'Grade injetada com perfis E e F para estrutura de degrau'
};

// HTML do formulário (versão simplificada)
const DEGRAU_INJETADO_HTML = `
    <div class="mb-3">
        <label for="degrau_inj_nome" class="form-label">Nome do Degrau Injetado *</label>
        <input type="text" class="form-control param-input" id="degrau_inj_nome" name="nome_degrau" required>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="mb-3">
                <label for="degrau_inj_vao" class="form-label">Vão (mm) *</label>
                <input type="number" step="0.1" class="form-control param-input" id="degrau_inj_vao" name="vao" required min="0">
            </div>
        </div>
        <div class="col-md-6">
            <div class="mb-3">
                <label for="degrau_inj_comprimento" class="form-label">Comprimento (mm) *</label>
                <input type="number" step="0.1" class="form-control param-input" id="degrau_inj_comprimento" name="comprimento" required min="0">
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="mb-3">
                <label for="degrau_inj_tempo_proc" class="form-label">Tempo Processamento (h)</label>
                <input type="number" step="0.1" class="form-control param-input" id="degrau_inj_tempo_proc" name="tempo_proc" value="1.0" min="0">
            </div>
        </div>
        <div class="col-md-6">
            <div class="mb-3">
                <label for="degrau_inj_tempo_mtg" class="form-label">Tempo Montagem (h)</label>
                <input type="number" step="0.1" class="form-control param-input" id="degrau_inj_tempo_mtg" name="tempo_mtg" value="1.5" min="0">
            </div>
        </div>
    </div>
    
    <div class="mb-3">
        <label for="degrau_inj_perda" class="form-label">Perda (%)</label>
        <input type="number" step="0.1" class="form-control param-input" id="degrau_inj_perda" name="percentual_perda" value="3.0" min="0">
    </div>
    
    <div class="mt-3 text-center">
        <button type="button" class="btn btn-success" onclick="calcularDegrauInjetado()">
            <i class="fas fa-calculator"></i> Calcular Degrau Injetado
        </button>
    </div>
`;

// Função para carregar a interface
function carregarInterfaceDegrauInjetado() {
    console.log('=== CARREGANDO INTERFACE DEGRAU INJETADO ===');
    
    // Limpar estado anterior
    templateAtual = { 
        id: DEGRAU_INJETADO_CONFIG.id, 
        tipo: DEGRAU_INJETADO_CONFIG.tipo 
    };
    ultimoCalculo = null;
    
    // Configurar seletor e descrição
    document.getElementById('templateSelect').value = DEGRAU_INJETADO_CONFIG.id;
    document.getElementById('templateDescription').innerHTML = `
        <h6 class="text-primary">${DEGRAU_INJETADO_CONFIG.titulo}</h6>
        <small class="text-muted">Categoria: ${DEGRAU_INJETADO_CONFIG.categoria}</small>
        <p class="mt-2 text-info small">
            ${DEGRAU_INJETADO_CONFIG.descricao}
        </p>
    `;
    
    // Carregar HTML do formulário
    const parametrosContainer = document.getElementById('parametrosContainer');
    parametrosContainer.innerHTML = DEGRAU_INJETADO_HTML;
    
    console.log('✅ Interface Degrau Injetado carregada com sucesso');
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.carregarInterfaceDegrauInjetado = carregarInterfaceDegrauInjetado;
    window.DEGRAU_INJETADO_CONFIG = DEGRAU_INJETADO_CONFIG;
}