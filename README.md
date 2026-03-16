# 🤖 Crawler Univap API

API desenvolvida em FastAPI para automatizar a coleta de avisos diários do Portal Univap. Este projeto funciona como um "braço" do **H-Zap**, um AI Agent criado no n8n que organiza a rotina dos alunos.

## 📋 Sobre o Projeto

Este crawler simula a sessão de um aluno no Portal Univap, realiza o login automaticamente e busca os avisos publicados no dia atual. Os dados são disponibilizados através de uma API REST simples e segura, permitindo que o H-Zap acesse as informações de forma programática.

### Contexto

Este projeto faz parte de um ecossistema maior:
- **H-Zap**: AI Agent principal (n8n) que organiza a rotina da sala
- **Crawler Univap API**: Este projeto - responsável por coletar avisos do portal

## 🚀 Funcionalidades

- ✅ Autenticação automática no Portal Univap
- ✅ Coleta de avisos publicados no dia atual
- ✅ API REST com autenticação via Bearer Token
- ✅ Filtragem de comunicados por data
- ✅ Retorno estruturado em JSON

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **FastAPI** - Framework web moderno e rápido
- **Requests** - Requisições HTTP
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **Uvicorn** - Servidor ASGI

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/crawler_univap.git
cd crawler_univap
```

### 2. Crie um ambiente virtual
```bash
python -m venv env
```

### 3. Ative o ambiente virtual
```bash
# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```env
UNIVAP_USERNAME=seu_usuario
UNIVAP_PASSWORD=sua_senha
```

## ▶️ Como Usar

### Executar a API

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

### Endpoint Disponível

**GET** `/crawler_univap/`

**Headers:**
```
Authorization: Bearer seu_token_aqui
```

**Resposta de Sucesso (200):**
```json
{
  "status": true,
  "comunicados": [
    {
      "comunicado": "Título do aviso",
      "data": "18/12/2025"
    }
  ]
}
```

**Exemplo de uso:**
```bash
curl -H "Authorization: Bearer seu_token_aqui" \
     http://localhost:8000/crawler_univap/
```

## 📁 Estrutura do Projeto

```
crawler_univap/
├── controllers/
│   ├── __init__.py
│   └── univap_controller.py    # Lógica do crawler e rotas
├── env/                         # Ambiente virtual (não versionado)
├── .env                         # Credenciais (não versionado)
├── .env.example                 # Template de variáveis de ambiente
├── .gitignore                   # Arquivos ignorados pelo Git
├── main.py                      # Ponto de entrada da aplicação
├── requirements.txt             # Dependências do projeto
└── README.md                    # Este arquivo
```

## 🔒 Segurança

- ✅ Credenciais armazenadas em variáveis de ambiente
- ✅ Arquivo `.env` não versionado no Git
- ✅ Autenticação via Bearer Token na API
- ⚠️ **Importante**: Troque a chave de API (`KEY`) em produção

## ⚠️ Notas Importantes

1. Este projeto foi desenvolvido especificamente para o Portal Univap
2. Alterações na estrutura do portal podem quebrar o funcionamento
3. Use com responsabilidade e respeite os termos de uso do portal
4. Mantenha suas credenciais seguras e nunca as compartilhe

## 📝 Licença

Este projeto é de uso pessoal/educacional.

---

**Desenvolvido para integração com o H-Zap AI Agent** 🤖
