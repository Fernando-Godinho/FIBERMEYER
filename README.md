# FIBERMEYER - Projeto Django

Este é um projeto Django para sistema de orçamentos FIBERMEYER.

## Configuração do Ambiente

1. **Ambiente Virtual**: Um ambiente virtual Python já foi configurado no diretório `.venv/`
2. **Django**: O Django foi instalado e configurado
3. **Banco de Dados**: SQLite (padrão) já configurado com migrações aplicadas

## Estrutura do Projeto (Limpa)

```
FIBERMEYER/
├── .venv/                 # Ambiente virtual Python
├── fibermeyer_project/    # Configurações principais do Django
│   ├── settings.py        # Configurações do projeto
│   ├── urls.py           # URLs principais
│   ├── wsgi.py           # Configuração WSGI
│   └── asgi.py           # Configuração ASGI
├── main/                  # Aplicação principal
│   ├── templates/        # Templates HTML
│   ├── migrations/       # Migrações do banco
│   ├── views.py          # Views da aplicação
│   ├── urls.py           # URLs da aplicação
│   ├── models.py         # Modelos de dados
│   ├── serializers.py    # Serializers para API
│   ├── admin.py          # Configuração do admin
│   └── tests.py          # Testes da aplicação
├── backup_arquivos_removidos/  # Arquivos de teste e apoio (movidos)
├── manage.py             # Script de gerenciamento Django
├── db.sqlite3            # Banco de dados
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

## Como Executar

1. **Ativar o ambiente virtual** (se necessário):
   ```bash
   .venv\Scripts\activate
   ```

2. **Executar o servidor de desenvolvimento**:
   ```bash
   python manage.py runserver
   ```

3. **Acessar a aplicação**:
   - Página inicial: http://127.0.0.1:8000/
   - Página sobre: http://127.0.0.1:8000/about/
   - Painel administrativo: http://127.0.0.1:8000/admin/

## Arquivos Removidos

Durante a limpeza do projeto, foram movidos **81 arquivos** de teste, debug e apoio para a pasta `backup_arquivos_removidos/`. Estes incluem:

- Arquivos de teste (`test_*.py`)
- Scripts de debug (`debug_*.py`)
- Arquivos de apoio e configuração temporária
- Documentação técnica de desenvolvimento
- Scripts de importação e migração de dados

Os arquivos removidos ainda estão disponíveis na pasta de backup caso precisem ser recuperados.

## Credenciais do Administrador

- **Usuário**: admin
- **Email**: admin@example.com
- **Senha**: admin123

## Próximos Passos

- Desenvolver modelos de dados na aplicação `main`
- Criar templates HTML para as views
- Configurar arquivos estáticos (CSS, JS, imagens)
- Implementar funcionalidades específicas do negócio
- Configurar banco de dados de produção (PostgreSQL, MySQL, etc.)

## Comandos Úteis

```bash
# Criar nova aplicação
python manage.py startapp nome_da_app

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar testes
python manage.py test
```
