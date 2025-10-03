/**
 * Template para Tampa Montada
 * Contém HTML e JavaScript necessários para o cálculo de tampa montada
 */

// Configuração do template
const TAMPA_MONTADA_CONFIG = {
    id: 'tampa_montada_customizado',
    tipo: 'tampa_montada',
    titulo: 'Tampa Montada',
    categoria: 'PRODUTO_FINAL',
    descricao: 'Tampa com perfis, chapa, alças e opções adicionais'
};

// HTML do formulário
const TAMPA_MONTADA_HTML = `
    <div class="mb-3">
        <label for="tampa_nome" class="form-label">Nome da Tampa *</label>
        <input type="text" class="form-control param-input" id="tampa_nome" name="nome_tampa" required>
    </div>
    
    <div class="mb-3">
        <label for="tampa_vao" class="form-label">Vão (mm) *</label>
        <input type="number" step="0.1" class="form-control param-input" id="tampa_vao" name="vao" required min="0">
        <div class="form-text">Vão da tampa em milímetros</div>
    </div>
    
    <div class="mb-3">
        <label for="tampa_comprimento" class="form-label">Comprimento (mm) *</label>
        <input type="number" step="0.1" class="form-control param-input" id="tampa_comprimento" name="comprimento" required min="0">
        <div class="form-text">Comprimento total da tampa em milímetros</div>
    </div>
    
    <div class="mb-3">
        <label for="tampa_eixo_i" class="form-label">Eixo I (mm) *</label>
        <input type="number" step="0.1" class="form-control param-input" id="tampa_eixo_i" name="eixo_i" required min="0">
        <div class="form-text">Distância entre perfis em milímetros</div>
    </div>
    
    <div class="mb-3">
        <label for="tampa_perfil" class="form-label">Selecione o Perfil *</label>
        <select class="form-select param-input" id="tampa_perfil" name="perfil_id" required>
            <option value="">Carregando perfis...</option>
        </select>
    </div>
    
    <div class="mb-3">
        <label for="tampa_perda" class="form-label">Perda (%)</label>
        <input type="number" step="0.1" class="form-control param-input" id="tampa_perda" name="perda" value="3" min="0" max="100">
        <div class="form-text">Percentual de perda dos materiais (padrão: 3%)</div>
    </div>
    
    <div class="row">
        <div class="col-md-6">
            <div class="mb-3">
                <label for="tampa_tempo_proc" class="form-label">Tempo Processamento (h)</label>
                <input type="number" step="0.1" class="form-control param-input" id="tampa_tempo_proc" name="tempo_proc" value="1.5" min="0">
                <div class="form-text">Tempo de processamento em horas</div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="mb-3">
                <label for="tampa_tempo_mtg" class="form-label">Tempo Montagem (h)</label>
                <input type="number" step="0.1" class="form-control param-input" id="tampa_tempo_mtg" name="tempo_mtg" value="0.5" min="0">
                <div class="form-text">Tempo de montagem em horas</div>
            </div>
        </div>
    </div>
    
    <div class="card mb-3">
        <div class="card-header">
            <h6 class="mb-0"><i class="fas fa-cogs"></i> Opções Adicionais</h6>
        </div>
        <div class="card-body">
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="tampa_quadro_u4" name="quadro_u4">
                <label class="form-check-label" for="tampa_quadro_u4">
                    Incluir Quadro U4" (2 unidades)
                </label>
            </div>
            
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="tampa_alca" name="alca">
                <label class="form-check-label" for="tampa_alca">
                    Incluir Alças (2 unidades)
                </label>
            </div>
            
            <div class="form-check mb-2">
                <input class="form-check-input" type="checkbox" id="tampa_chapa_ev" name="chapa_ev">
                <label class="form-check-label" for="tampa_chapa_ev">
                    Incluir Chapa EV
                </label>
            </div>
        </div>
    </div>
    
    <div class="d-grid gap-2">
        <button type="button" class="btn btn-primary" onclick="calcularTampaMontada()" id="calcularTampaBtn">
            <i class="fas fa-calculator"></i> Calcular Tampa Montada
        </button>
    </div>
`;

// Função para carregar perfis
function carregarPerfisTampa() {
    console.log('=== CARREGANDO PERFIS PARA TAMPA MONTADA ===');
    
    const selectPerfil = document.getElementById('tampa_perfil');
    if (!selectPerfil) {
        console.warn('Select de perfil não encontrado');
        return;
    }
    
    // Buscar perfis via API
    fetch('/api/produtos/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(produtos => {
            console.log(`✅ ${produtos.length} produtos carregados, filtrando perfis...`);
            
            // Filtrar perfis (produtos que contêm "perfil" na descrição)
            const perfis = produtos.filter(produto => {
                const desc = produto.descricao.toLowerCase();
                return desc.includes('perfil') && !desc.includes('grade');
            });
            
            console.log(`📊 ${perfis.length} perfis encontrados`);
            
            // Limpar opções atuais
            selectPerfil.innerHTML = '<option value="">Selecione um perfil...</option>';
            
            // Ordenar por descrição
            perfis.sort((a, b) => a.descricao.localeCompare(b.descricao));
            
            // Adicionar opções dos perfis
            perfis.forEach(perfil => {
                const option = document.createElement('option');
                option.value = perfil.id;
                option.textContent = `${perfil.descricao} - R$ ${(perfil.custo_centavos/100).toFixed(2)}/m`;
                selectPerfil.appendChild(option);
                
                console.log(`   • ${perfil.descricao}: R$ ${(perfil.custo_centavos/100).toFixed(2)}/m`);
            });
            
            if (perfis.length === 0) {
                selectPerfil.innerHTML = '<option value="">Nenhum perfil encontrado</option>';
                console.warn('⚠️ Nenhum perfil encontrado');
            }
            
        })
        .catch(error => {
            console.error('❌ Erro ao carregar perfis:', error);
            selectPerfil.innerHTML = '<option value="">Erro ao carregar</option>';
        });
}

// Função para carregar a interface
function carregarInterfaceTampaMontada() {
    console.log('=== CARREGANDO INTERFACE TAMPA MONTADA ===');
    
    // Limpar estado anterior
    templateAtual = { 
        id: TAMPA_MONTADA_CONFIG.id, 
        tipo: TAMPA_MONTADA_CONFIG.tipo 
    };
    ultimoCalculo = null;
    
    // Configurar seletor e descrição
    document.getElementById('templateSelect').value = TAMPA_MONTADA_CONFIG.id;
    document.getElementById('templateDescription').innerHTML = `
        <h6 class="text-primary">${TAMPA_MONTADA_CONFIG.titulo}</h6>
        <small class="text-muted">Categoria: ${TAMPA_MONTADA_CONFIG.categoria}</small>
        <p class="mt-2 text-info small">
            ${TAMPA_MONTADA_CONFIG.descricao}
        </p>
    `;
    
    // Carregar HTML do formulário
    const parametrosContainer = document.getElementById('parametrosContainer');
    parametrosContainer.innerHTML = TAMPA_MONTADA_HTML;
    
    // Habilitar botão calcular
    const calcularBtn = document.getElementById('calcularBtn');
    if (calcularBtn) {
        calcularBtn.disabled = false;
    }
    
    // Carregar perfis disponíveis
    carregarPerfisTampa();
    
    console.log('✅ Interface Tampa Montada carregada com sucesso');
}

// Exportar para uso global
if (typeof window !== 'undefined') {
    window.carregarInterfaceTampaMontada = carregarInterfaceTampaMontada;
    window.carregarPerfisTampa = carregarPerfisTampa;
    window.TAMPA_MONTADA_CONFIG = TAMPA_MONTADA_CONFIG;
}