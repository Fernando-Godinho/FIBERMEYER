/**
 * Template para Tampa Injetada
 * Contém HTML e JavaScript necessários para o cálculo de tampa injetada
 */

// Configuração do template
const TAMPA_INJETADA_CONFIG = {
    id: 'tampa_injetada_customizado',
    tipo: 'tampa_injetada',
    titulo: 'Tampa Injetada',
    categoria: 'TAMPAS',
    descricao: 'Grade injetada com preço por m² fixo'
};

// HTML do formulário
const TAMPA_INJETADA_HTML = `
    <div class="mb-3">
        <label for="tampa_inj_nome" class="form-label">Nome da Tampa Injetada *</label>
        <input type="text" class="form-control param-input" id="tampa_inj_nome" name="nome_tampa" required>
    </div>
    
    <div class="mb-3">
        <label for="tampa_inj_vao" class="form-label">Vão (mm) *</label>
        <input type="number" step="0.1" class="form-control param-input" id="tampa_inj_vao" name="vao" required min="0">
        <div class="form-text">Distância entre apoios em milímetros</div>
    </div>
    
    <div class="mb-3">
        <label for="tampa_inj_comprimento" class="form-label">Comprimento (mm) *</label>
        <input type="number" step="0.1" class="form-control param-input" id="tampa_inj_comprimento" name="comprimento" required min="0">
        <div class="form-text">Comprimento total da tampa em milímetros</div>
    </div>
    
    <div class="mb-3">
        <label for="tampa_inj_grade" class="form-label">Selecione a Grade Injetada *</label>
        <select class="form-select param-input" id="tampa_inj_grade" name="grade_id" required>
            <option value="">Carregando grades injetadas...</option>
        </select>
        <div class="form-text">Grade injetada que será utilizada</div>
    </div>
    
    <div class="mb-3">
        <label for="tampa_inj_perda" class="form-label">Perda (%)</label>
        <input type="number" step="0.1" class="form-control param-input" id="tampa_inj_perda" name="perda" value="5" min="0" max="100">
        <div class="form-text">Percentual de perda do material (padrão: 5%)</div>
    </div>
    
    <!-- Opções Adicionais -->
    <div class="card mb-3">
        <div class="card-header">
            <h6 class="mb-0"><i class="fas fa-cogs"></i> Opções Adicionais</h6>
        </div>
        <div class="card-body">
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="tampa_inj_quadro_u4" name="quadro_u4">
                <label class="form-check-label" for="tampa_inj_quadro_u4">
                    Quadro U4" (2 unidades)
                </label>
            </div>
            
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="tampa_inj_alca" name="alca">
                <label class="form-check-label" for="tampa_inj_alca">
                    Alça Metálica (2 unidades)
                </label>
            </div>
            
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="tampa_inj_chapa_ev" name="chapa_ev">
                <label class="form-check-label" for="tampa_inj_chapa_ev">
                    Chapa EV (R$ 277,50 fixo)
                </label>
            </div>
        </div>
    </div>
    
    <!-- Seção de Mão de Obra -->
    <div class="card mb-3">
        <div class="card-header">
            <h6 class="mb-0"><i class="fas fa-tools"></i> Mão de Obra</h6>
        </div>
        <div class="card-body">
            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="tampa_inj_tempo_proc" class="form-label">Tempo PROC (h)</label>
                    <input type="number" step="0.1" class="form-control param-input" id="tampa_inj_tempo_proc" name="tempo_proc" value="0.7" min="0">
                    <div class="form-text">Tempo de processamento em horas</div>
                </div>
                <div class="col-md-6 mb-3">
                    <label for="tampa_inj_tempo_mtg" class="form-label">Tempo MTG (h)</label>
                    <input type="number" step="0.1" class="form-control param-input" id="tampa_inj_tempo_mtg" name="tempo_mtg" value="0.3" min="0">
                    <div class="form-text">Tempo de montagem em horas</div>
                </div>
            </div>
            <div class="alert alert-info">
                <small><i class="fas fa-info-circle"></i> Mão de Obra: Processamento/Montagem - R$ 65,79/hora</small>
            </div>
        </div>
    </div>
    
    <div class="mt-3 text-center">
        <button type="button" class="btn btn-primary" onclick="calcularTampaInjetada()" id="calcularTampaInjetadaBtn">
            <i class="fas fa-calculator"></i> Calcular Tampa Injetada
        </button>
    </div>
`;

// Função para carregar grades injetadas
function carregarGradesInjetadas() {
    console.log('=== CARREGANDO GRADES INJETADAS ===');
    
    const selectGrade = document.getElementById('tampa_inj_grade');
    if (!selectGrade) {
        console.warn('Select de grade injetada não encontrado');
        return;
    }
    
    // Buscar grades injetadas via API
    fetch('/api/produtos/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(produtos => {
            console.log(`✅ ${produtos.length} produtos carregados, filtrando grades injetadas...`);
            
            // Filtrar grades injetadas
            const gradesInjetadas = produtos.filter(produto => {
                const desc = produto.descricao.toLowerCase();
                return desc.includes('grade') && desc.includes('injetada');
            });
            
            console.log(`📊 ${gradesInjetadas.length} grades injetadas encontradas`);
            
            // Limpar opções atuais
            selectGrade.innerHTML = '<option value="">Selecione uma grade injetada...</option>';
            
            // Ordenar por descrição
            gradesInjetadas.sort((a, b) => a.descricao.localeCompare(b.descricao));
            
            // Adicionar opções das grades
            gradesInjetadas.forEach(grade => {
                const option = document.createElement('option');
                option.value = grade.id;
                option.textContent = `${grade.descricao} - R$ ${(grade.custo_centavos/100).toFixed(2)}/m²`;
                selectGrade.appendChild(option);
                
                console.log(`   • ${grade.descricao}: R$ ${(grade.custo_centavos/100).toFixed(2)}/m²`);
            });
            
            if (gradesInjetadas.length === 0) {
                selectGrade.innerHTML = '<option value="">Nenhuma grade injetada encontrada</option>';
                console.warn('⚠️ Nenhuma grade injetada encontrada');
            }
            
        })
        .catch(error => {
            console.error('❌ Erro ao carregar grades injetadas:', error);
            selectGrade.innerHTML = '<option value="">Erro ao carregar</option>';
        });
}

// Função para carregar a interface
function carregarInterfaceTampaInjetada() {
    console.log('=== CARREGANDO INTERFACE TAMPA INJETADA ===');
    
    // Limpar estado anterior
    templateAtual = { 
        id: TAMPA_INJETADA_CONFIG.id, 
        tipo: TAMPA_INJETADA_CONFIG.tipo 
    };
    ultimoCalculo = null;
    
    // Configurar seletor e descrição
    document.getElementById('templateSelect').value = TAMPA_INJETADA_CONFIG.id;
    document.getElementById('templateDescription').innerHTML = `
        <h6 class="text-primary">${TAMPA_INJETADA_CONFIG.titulo}</h6>
        <small class="text-muted">Categoria: ${TAMPA_INJETADA_CONFIG.categoria}</small>
        <p class="mt-2 text-info small">
            <strong>Fórmula:</strong> ${TAMPA_INJETADA_CONFIG.descricao}
        </p>
    `;
    
    // Carregar HTML do formulário
    const parametrosContainer = document.getElementById('parametrosContainer');
    parametrosContainer.innerHTML = TAMPA_INJETADA_HTML;
    
    // Carregar grades injetadas disponíveis
    carregarGradesInjetadas();
    
    console.log('✅ Interface Tampa Injetada carregada com sucesso');
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.carregarInterfaceTampaInjetada = carregarInterfaceTampaInjetada;
    window.carregarGradesInjetadas = carregarGradesInjetadas;
    window.TAMPA_INJETADA_CONFIG = TAMPA_INJETADA_CONFIG;
}