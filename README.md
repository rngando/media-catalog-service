# 🎬 Movie & Series Scraper API

Uma API robusta desenvolvida para automatizar a coleta, limpeza e disponibilização de dados sobre filmes e séries. O projeto utiliza técnicas avançadas de Web Scraping para transformar HTML bruto em uma interface JSON organizada e pronta para consumo.

## 📌 Sobre o Projeto

Este projeto nasceu da necessidade de centralizar informações de catálogos externos. Ele não apenas extrai os dados, mas os submete a um rigoroso processo de normalização para garantir que datas, ratings e links estejam sempre no formato correto.

## 🏗️ Estrutura do Repositório

A arquitetura foi desenhada seguindo as melhores práticas de escalabilidade para FastAPI:

```
.
├── app/
│   ├── api/              # Endpoints versionados (v1) e dependências
│   ├── core/             # Configurações de sistema e variáveis de ambiente
│   ├── db/               # Migrações e setup do banco de dados (SQLAlchemy)
│   ├── models/           # Definição das tabelas de Filmes e Séries
│   ├── schemas/          # Modelos Pydantic (Validação de entrada/saída)
│   ├── scraping/         # O Motor do projeto:
│   │   ├── client.py     # Gestão de requisições HTTP
│   │   ├── parsers.py    # Lógica de extração com BS4
│   │   ├── normalizer.py # Limpeza e padronização de dados
│   │   └── jobs.py       # Tarefas agendadas de atualização
│   ├── services/         # Lógica de negócio
│   ├── utils/            # Funções utilitárias
│   └── main.py           # Arquivo principal e inicialização
├── tests/                # Suíte de testes
├── .env                  # Variáveis de ambiente (não incluído no git)
├── .gitignore           # Arquivos ignorados pelo git
├── requirements.txt     # Dependências do projeto
└── README               # Este arquivo
```

## 🚀 Como Configurar

### Pré-requisitos

- Python 3.10 ou superior
- Pip (Gerenciador de pacotes)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/rngando/media-catalog-service
cd movies_api
```

2. Crie um ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o .env com suas configurações
```

5. Inicie a aplicação:
```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa em: **http://127.0.0.1:8000/docs**

## 🔄 Fluxo de Dados (Scraping Pipeline)

1. **Client** (`client.py`): Realiza o fetch do HTML utilizando requests com tratamento de timeouts.

2. **Parser** (`parsers.py`): Utiliza BeautifulSoup para localizar as tags de título, descrição, imagem e metadados.

3. **Normalizer** (`normalizer.py`): Remove espaços em branco, converte strings de rating em floats e limpa formatos de data.

4. **Jobs** (`jobs.py`): Orquestra o processo completo de scraping e atualização de dados.

5. **API** (`api/`): Expõe os dados higienizados através de rotas RESTful.

## 📦 Dependências

As principais dependências do projeto estão em `requirements.txt`:

- **FastAPI** (0.135.0): Framework web de alto desempenho
- **Uvicorn** (0.41.0): Servidor ASGI
- **BeautifulSoup4** (4.14.3): Parsing de HTML
- **Requests** (2.32.5): Requisições HTTP
- **Python-dotenv** (1.2.1): Gerenciamento de variáveis de ambiente

## 📝 Roadmap

- [x] Estruturação modular da aplicação
- [x] Parser básico de filmes e séries
- [x] Normalização de metadados (Ano/Rating)
- [ ] Implementação de Cache com Redis
- [ ] Containerização com Docker
- [ ] Sistema de autenticação
- [ ] Testes unitários e de integração

## 🛠️ Desenvolvimento

Para contribuir com o projeto:

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**Desenvolvido por Ramiro** 🚀