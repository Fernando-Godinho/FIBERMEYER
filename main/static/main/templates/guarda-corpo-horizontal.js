/**
 * Template para Guarda Corpo Horizontal
 * Contém HTML e JavaScript necessários para o cálculo de guarda corpo horizontal
 */

// Configuração do template
const GUARDA_CORPO_HORIZONTAL_CONFIG = {
    id: 'guarda_corpo_horizontal_customizado',
    tipo: 'guarda_corpo_horizontal',
    titulo: 'Guarda Corpo - Horizontal',
    categoria: 'ESTRUTURAS',
    descricao: 'Cálculo de guarda corpo horizontal com colunas, barras intermediárias, tubos quadrados, perfis ômega e sapatas.'
};

// HTML do formulário
const GUARDA_CORPO_HORIZONTAL_HTML = `
    <div class="mb-3">
        <label for="gc_horiz_nome" class="form-label">Nome do Guarda Corpo *</label>
        <input type="text" class="form-control param-input" id="gc_horiz_nome" name="nome_guarda_corpo" required>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="mb-3">
                <label for="gc_horiz_larg_modulo" class="form-label">Largura (m) *</label>
                <input type="number" class="form-control param-input" id="gc_horiz_larg_modulo" name="larg_modulo" step="0.01" required>
            </div>
        </div>
        <div class="col-md-6">
            <div class="mb-3">
                <label for="gc_horiz_altura" class="form-label">Altura (m) *</label>
                <input type="number" class="form-control param-input" id="gc_horiz_altura" name="altura" step="0.01" required>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="mb-3">
                <label for="gc_horiz_n_colunas" class="form-label">Nº Colunas *</label>
                <input type="number" class="form-control param-input" id="gc_horiz_n_colunas" name="n_colunas" min="0.01" step="0.01" required>
            </div>
        </div>
        <div class="col-md-6">
            <div class="mb-3">
                <label for="gc_horiz_n_br_intermediaria" class="form-label">Nº Brr. Intermed.*</label>
                <input type="number" class="form-control param-input" id="gc_horiz_n_br_intermediaria" name="n_br_intermediaria" min="0" required>
            </div>
        </div>
    </div>
    
    <div class="mb-3">
        <label for="gc_horiz_tipo_tubo_quad" class="form-label">Tipo de Tubo Quadrado *</label>
        <select class="form-select param-input" id="gc_horiz_tipo_tubo_quad" name="tipo_tubo_quad" required>
            <option value="">Selecione o tipo de tubo quadrado...</option>
            <option value="Tubo Quadrado 50 #6mm">Tubo Quadrado 50 #6mm</option>
            <option value="Tubo Quadrado 50 #4mm">Tubo Quadrado 50 #4mm</option>
            <option value="Tubo Quadrado 50 #3mm">Tubo Quadrado 50 #3mm</option>
        </select>
    </div>
    
    <div class="mb-3">
        <label for="gc_horiz_tipo_omega" class="form-label">Tipo de Ômega *</label>
        <select class="form-select param-input" id="gc_horiz_tipo_omega" name="tipo_omega" required>
            <option value="">Selecione o tipo de ômega...</option>
            <option value="PERFIL OMEGA 45X20MM">PERFIL OMEGA 45X20MM</option>
            <option value="Perfil ômega 50mm">Perfil ômega 50mm</option>
        </select>
    </div>
    
    <div class="mb-3">
        <label for="gc_horiz_tipo_sapata" class="form-label">Tipo de Sapata *</label>
        <select class="form-select param-input" id="gc_horiz_tipo_sapata" name="tipo_sapata" required>
            <option value="">Selecione o tipo de sapata...</option>
            <option value="SAPATA LAMINADA">SAPATA LAMINADA</option>
            <option value="SAPATA INOX 150#3MM">SAPATA INOX 150#3MM</option>
        </select>
    </div>
    
    <!-- Seção de Mão de Obra -->
    <div class="card mb-3">
        <div class="card-header">
            <h6 class="mb-0">Mão de Obra</h6>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="gc_horiz_tempo_proc" class="form-label">Tempo Processamento (h)</label>
                        <input type="number" class="form-control param-input" id="gc_horiz_tempo_proc" name="tempo_proc" step="0.1" value="2.0">
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="mb-3">
                        <label for="gc_horiz_tempo_mtg" class="form-label">Tempo Montagem (h)</label>
                        <input type="number" class="form-control param-input" id="gc_horiz_tempo_mtg" name="tempo_mtg" step="0.1" value="3.0">
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="mb-3">
        <label for="gc_horiz_perda" class="form-label">Perda (%)</label>
        <input type="number" class="form-control param-input" id="gc_horiz_perda" name="percentual_perda" step="0.1" value="3.0" min="0">
    </div>
    
    <div class="mt-3 text-center">
        <button type="button" class="btn btn-success" onclick="calcularGuardaCorpoHorizontal()">
            <i class="fas fa-calculator"></i> Calcular Guarda Corpo
        </button>
    </div>
`;

// Função para carregar a interface
function carregarInterfaceGuardaCorpoHorizontal() {
    console.log('=== CARREGANDO INTERFACE GUARDA CORPO - HORIZONTAL ===');
    
    // Limpar estado anterior
    templateAtual = { 
        id: GUARDA_CORPO_HORIZONTAL_CONFIG.id, 
        tipo: GUARDA_CORPO_HORIZONTAL_CONFIG.tipo 
    };
    ultimoCalculo = null;
    
    // Configurar seletor e descrição
    document.getElementById('templateSelect').value = GUARDA_CORPO_HORIZONTAL_CONFIG.id;
    document.getElementById('templateDescription').innerHTML = `
        <h6 class="text-primary">${GUARDA_CORPO_HORIZONTAL_CONFIG.titulo}</h6>
        <small class="text-muted">Categoria: ${GUARDA_CORPO_HORIZONTAL_CONFIG.categoria}</small>
        <p class="mt-2 text-info small">
            ${GUARDA_CORPO_HORIZONTAL_CONFIG.descricao}
        </p>
    `;
    
    // Carregar HTML do formulário
    const parametrosContainer = document.getElementById('parametrosContainer');
    parametrosContainer.innerHTML = GUARDA_CORPO_HORIZONTAL_HTML;
    
    console.log('✅ Interface Guarda Corpo - Horizontal carregada com sucesso');
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.carregarInterfaceGuardaCorpoHorizontal = carregarInterfaceGuardaCorpoHorizontal;
    window.GUARDA_CORPO_HORIZONTAL_CONFIG = GUARDA_CORPO_HORIZONTAL_CONFIG;
}