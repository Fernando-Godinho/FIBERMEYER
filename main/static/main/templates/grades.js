/**
 * Template para Grades
 * Contém HTML e JavaScript necessários para o cálculo de grades
 */

// Configuração do template
const GRADES_CONFIG = {
    id: 'grades_customizado',
    tipo: 'grades',
    titulo: 'Grades',
    categoria: 'ESTRUTURAS',
    descricao: 'Cálculo de grades com perfis estruturais',
    formula: '(((comprimento/eixo i)*vão/1000)* peso do perfil)'
};

// HTML do formulário
const GRADES_HTML = `
    <div class="mb-3">
        <label for="grade_nome" class="form-label">Nome da Grade *</label>
        <input type="text" class="form-control param-input" id="grade_nome" name="nome_grade" required>
    </div>
    
    <div class="mb-3">
        <label for="grade_vao" class="form-label">Vão (mm) *</label>
        <input type="number" step="0.1" class="form-control param-input" id="grade_vao" name="vao" required min="0">
        <div class="form-text">Distância entre apoios em milímetros</div>
    </div>
    
    <div class="mb-3">
        <label for="grade_comprimento" class="form-label">Comprimento (mm) *</label>
        <input type="number" step="0.1" class="form-control param-input" id="grade_comprimento" name="comprimento" required min="0">
        <div class="form-text">Comprimento total da grade em milímetros</div>
    </div>
    
    <div class="mb-3">
        <label for="grade_eixo_i" class="form-label">Eixo I (mm) *</label>
        <input type="number" step="0.1" class="form-control param-input" id="grade_eixo_i" name="eixo_i" required min="0">
        <div class="form-text">Espaçamento entre perfis em milímetros</div>
    </div>
    
    <div class="mb-3">
        <label for="grade_perfil" class="form-label">Selecione o Perfil *</label>
        <select class="form-select param-input" id="grade_perfil" name="perfil_id" required>
            <option value="">Carregando perfis...</option>
        </select>
        <div class="form-text">Perfil que será utilizado na estrutura</div>
    </div>
    
    <div class="mb-3">
        <label for="grade_perda" class="form-label">Perda (%)</label>
        <input type="number" step="0.1" class="form-control param-input" id="grade_perda" name="perda" value="10" min="0" max="100">
        <div class="form-text">Percentual de perda do material (padrão: 5%)</div>
    </div>
    
    <!-- Seção de Mão de Obra -->
    <div class="card mb-3">
        <div class="card-header">
            <h6 class="mb-0"><i class="fas fa-tools"></i> Mão de Obra</h6>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="grade_tempo_proc" class="form-label">Tempo PROC (h)</label>
                    <input type="number" step="0.1" class="form-control param-input" id="grade_tempo_proc" name="tempo_proc" value="0.7" min="0">
                    <div class="form-text">Tempo de processamento em horas</div>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="grade_tempo_mtg" class="form-label">Tempo MTG (h)</label>
                    <input type="number" step="0.1" class="form-control param-input" id="grade_tempo_mtg" name="tempo_mtg" value="0.3" min="0">
                    <div class="form-text">Tempo de montagem em horas</div>
                </div>
            </div>
            <div class="alert alert-info">
                <small><i class="fas fa-info-circle"></i> Mão de Obra: Processamento/Montagem - R$ 65,79/hora</small>
            </div>
        </div>
    </div>
    
    <div class="mt-3 text-center">
        <button type="button" class="btn btn-primary" onclick="calcularGrade()" id="calcularGradeBtn">
            <i class="fas fa-calculator"></i> Calcular Grade
        </button>
    </div>
`;

// Função para carregar a interface
function carregarInterfaceGrades() {
    console.log('=== CARREGANDO INTERFACE GRADES ===');
    
    // Limpar estado anterior
    templateAtual = { 
        id: GRADES_CONFIG.id, 
        tipo: GRADES_CONFIG.tipo 
    };
    ultimoCalculo = null;
    
    // Configurar seletor e descrição
    document.getElementById('templateSelect').value = GRADES_CONFIG.id;
    document.getElementById('templateDescription').innerHTML = `
        <h6 class="text-primary">${GRADES_CONFIG.titulo}</h6>
        <small class="text-muted">Categoria: ${GRADES_CONFIG.categoria}</small>
        <p class="mt-2 text-info small">
            <strong>Fórmula:</strong> ${GRADES_CONFIG.formula}
        </p>
    `;
    
    // Carregar HTML do formulário
    const parametrosContainer = document.getElementById('parametrosContainer');
    parametrosContainer.innerHTML = GRADES_HTML;
    
    // Carregar perfis disponíveis
    carregarPerfisGrade();
    
    console.log('✅ Interface Grades carregada com sucesso');
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.carregarInterfaceGrades = carregarInterfaceGrades;
    window.GRADES_CONFIG = GRADES_CONFIG;
}