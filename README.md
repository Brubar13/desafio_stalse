# Desafio Técnico — Stalse

Projeto desenvolvido como parte do processo seletivo para a vaga na **Stalse**, seguindo as especificações descritas no [documento do desafio técnico](https://docs.google.com/document/d/1slRuo2AJeNQTN3tXe7IWgIF-Y3OPUfz8lsA2kWrZsDM/edit?tab=t.0).

A aplicação permite gerenciar tickets, clientes e usuários, além de disponibilizar métricas geradas a partir de um conjunto de avaliações de produtos da Amazon.

## 📋 Sumário

- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração e execução](#-configuração-e-execução)
- [Configuração do dataset](#-configuração-do-dataset)
- [Back-end](#-back-end)
- [Front-end](#-front-end)
- [Análise de dados](#-análise-de-dados)
- [Workflow n8n](#-workflow-n8n)
- [Screenshots](#-screenshots)

## 🛠️ Tecnologias utilizadas

- **Back-end:** Python, FastAPI e JWT para autenticação.
- **Banco de dados:** SQLite e SQLAlchemy.
- **Front-end:** Next.js, React e TypeScript.
- **Análise de dados:** Pandas e processamento de dados em JSON.
- **Automação:** n8n com workflow baseado em webhook.

## 📁 Estrutura do projeto

```text
/
├── backend/       # API, autenticação e acesso ao banco de dados
├── frontend/      # Aplicação web desenvolvida com Next.js
├── data/          # ETL e arquivos utilizados na análise de dados
│   ├── raw/       # Dataset original
│   ├── processed/ # Métricas processadas
│   └── etl.py     # Script de processamento dos dados
├── n8n/           # Workflow exportado em JSON
└── README.md
```

Os arquivos de dados brutos e as métricas geradas não são versionados no Git. Por isso, o dataset precisa ser baixado separadamente para reproduzir a análise.

## 📌 Pré-requisitos

Antes de executar o projeto, instale:

- [Python](https://www.python.org/downloads/) — necessário para o back-end e o processamento de dados.
- [Node.js](https://nodejs.org/en/download) — necessário para o front-end e para utilizar o npm.
- [Git](https://git-scm.com/downloads) — necessário para clonar o repositório.

Recomenda-se utilizar uma versão do Python e do Node.js compatível com as dependências do projeto.

## 🚀 Configuração e execução

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd NOME_DO_REPOSITORIO
```

Substitua `URL_DO_REPOSITORIO` e `NOME_DO_REPOSITORIO` pelos dados do repositório.

### 2. Configurar o back-end

Acesse a pasta do back-end:

```bash
cd backend
```

#### Criar o ambiente virtual Python

```bash
python -m venv venv_stalse_backend
```

No Windows, caso o comando `python` não funcione, tente `py`.

#### Ativar o ambiente virtual

**Windows — Prompt de Comando (CMD):**

```bat
venv_stalse_backend\Scripts\activate.bat
```

**Windows — PowerShell:**

```powershell
.\venv_stalse_backend\Scripts\Activate.ps1
```

**Git Bash ou ambiente Linux/macOS:**

```bash
source venv_stalse_backend/Scripts/activate
```

No Linux/macOS, caso a estrutura de diretórios seja diferente, utilize:

```bash
source venv_stalse_backend/bin/activate
```

#### Instalar as dependências

Com o ambiente virtual ativado, execute:

```bash
python -m pip install -r requirements.txt
```

#### Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz da pasta `backend`, utilizando o exemplo abaixo:

```env
SECRET_KEY=SUBSTITUA_POR_UMA_CHAVE_SECRETA
ALGORITHM=HS256
EXPIRE_IN_MINUTES=10080
EXPIRE_REFRESH_IN_MINUTES=11520
```

- `SECRET_KEY`: chave utilizada para assinar e validar os tokens JWT. Gere uma chave aleatória e mantenha-a em segredo.
- `ALGORITHM`: algoritmo de assinatura dos tokens.
- `EXPIRE_IN_MINUTES`: tempo de expiração do token de acesso, em minutos. O valor de `10080` corresponde a 7 dias.
- `EXPIRE_REFRESH_IN_MINUTES`: tempo de expiração do refresh token, em minutos. O valor de `11520` corresponde a 8 dias.

**Importante:** não compartilhe o arquivo `.env` nem envie segredos reais ao GitHub.

#### Iniciar o servidor

Na raiz da pasta `backend`, execute:

```bash
uvicorn main:app --reload
```

Por padrão, a API ficará disponível em:

- API: `http://127.0.0.1:8000`
- Documentação interativa: `http://127.0.0.1:8000/docs`

Mantenha esse terminal aberto enquanto utilizar a aplicação.

### 3. Configurar o front-end

Abra outro terminal e acesse a pasta do front-end, a partir da raiz do repositório:

```bash
cd frontend
```

#### Instalar as dependências

```bash
npm install
```

#### Configurar as variáveis de ambiente

Crie um arquivo `.env.local` na raiz da pasta `frontend`:

```env
FASTAPI_BASE_URL=http://127.0.0.1:8000
NODE_ENV=development
```

- `FASTAPI_BASE_URL`: endereço do servidor FastAPI utilizado pelo front-end/BFF. Ajuste a porta caso o back-end esteja executando em outra.
- `NODE_ENV`: indica o ambiente de execução do Node.js.

#### Iniciar o servidor

```bash
npm run dev
```

O terminal informará o endereço em que o front-end estará disponível. Com a configuração padrão do Next.js, acesse:

`http://localhost:3000`

Com o back-end e o front-end em execução, será possível acessar a aplicação e realizar o login utilizando uma das contas de demonstração, caso a seed esteja habilitada.

## 📊 Configuração do dataset

A análise de dados utiliza o conjunto de avaliações de produtos **Amazon Reviews — Cell Phones and Accessories**.

**Fonte:** [Amazon Reviews — Kaggle](https://www.kaggle.com/datasets/abdallahwagih/amazon-reviews/data)

O arquivo original não está incluído no repositório devido ao seu tamanho. Para executar a análise, siga os passos abaixo:

1. Acesse o [dataset no Kaggle](https://www.kaggle.com/datasets/abdallahwagih/amazon-reviews/data).
2. Clique no botão **Download**.
3. Baixe o conjunto de dados em formato `.zip`.
4. Extraia o conteúdo do arquivo ZIP.
5. Localize o arquivo `Cell_Phones_and_Accessories_5.json`.
6. Coloque esse arquivo dentro da pasta `data/raw/` do projeto.

A estrutura esperada é:

```text
data/
├── raw/
│   └── Cell_Phones_and_Accessories_5.json
├── processed/
│   └── metrics.json
└── etl.py
```

Caso as pastas `raw` e `processed` não estejam presentes após clonar o repositório, crie-as manualmente.

**Não é necessário executar o `etl.py` manualmente.** Quando a rota `GET /metrics` é acessada, o back-end verifica se o arquivo `data/processed/metrics.json` existe. Caso não exista, a API executa o processamento dos dados e retorna as métricas geradas.

Para que esse processo funcione, o dataset deve estar no caminho indicado acima.

## 🔌 Back-end

O back-end foi desenvolvido com FastAPI e disponibiliza endpoints para autenticação, gerenciamento de tickets, usuários e clientes, além da consulta das métricas de análise de dados.

### Autenticação

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/auth/login` | Autentica o usuário e retorna os tokens JWT. |
| `POST` | `/auth/refreshToken` | Utiliza um refresh token para renovar a autenticação. |

### Tickets

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/tickets` | Retorna os tickets, permitindo filtragem por `customer_id`, `assigned_user_id` e `status`. |
| `GET` | `/tickets/{ticket_id}` | Retorna os detalhes de um ticket específico. |
| `PATCH` | `/tickets/{ticket_id}` | Atualiza o status ou a prioridade de um ticket. |
| `POST` | `/tickets/create` | Cria um novo ticket. |

Apenas usuários administradores podem criar tickets.

Para atualizar um ticket, o usuário deve ser administrador ou o responsável pelo ticket, identificado pelo campo `assigned_user_id`.

### Usuários

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/user/all_users` | Retorna todos os usuários. Acesso exclusivo para administradores. |
| `GET` | `/user/{user_id}` | Retorna os dados de um usuário específico. Acesso permitido ao administrador ou ao próprio usuário. |
| `POST` | `/user/create` | Cria um novo usuário. Acesso exclusivo para administradores. |
| `PATCH` | `/user/{user_id}` | Atualiza os dados cadastrais de um usuário. |

Os administradores podem consultar e atualizar os dados dos usuários, incluindo o perfil de acesso e o estado de ativação.

Um usuário comum pode consultar e atualizar apenas seu próprio cadastro, podendo alterar nome, e-mail e senha. Ele não pode alterar seu perfil de acesso (`role`) nem seu estado de ativação (`is_active`).

### Clientes (Customers)

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/customer` | Retorna a lista de clientes cadastrados. |
| `GET` | `/customer/{customer_id}` | Retorna os dados de um cliente específico. |
| `POST` | `/customer/create` | Cria um novo cliente. Acesso exclusivo para administradores. |
| `PATCH` | `/customer/{customer_id}` | Atualiza os dados de um cliente. Acesso exclusivo para administradores. |

### Métricas

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/metrics` | Retorna as métricas geradas pelo ETL. |

Atualmente, a análise retorna:

- Os 10 melhores reviewers, classificados pela relação entre avaliações positivas recebidas e o total de votos de feedback sobre suas avaliações.
- Os 10 melhores produtos, conforme os critérios definidos no processamento dos dados.

O processamento é realizado pelo script `data/etl.py`, e o resultado é armazenado em `data/processed/metrics.json`.

### Autenticação e documentação da API

Todas as rotas do back-end exigem autenticação por token de acesso, com exceção de `POST /auth/login` e `GET /metrics`.

A documentação interativa da API pode ser acessada enquanto o servidor estiver em execução:

`http://127.0.0.1:8000/docs`

### Banco de dados e dados de demonstração

Na primeira execução do back-end, o banco de dados SQLite é criado e preenchido com dados iniciais (*seed*).

A carga inicial contém:

- 4 usuários, sendo 3 ativos e 1 inativo.
- 20 tickets.
- 1 cliente, chamado **Stalse**.

Dos usuários ativos, 1 possui perfil de administrador e 2 possuem perfil de usuário comum.

#### Credenciais de demonstração

| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | `admin@admin.com.br` | `1234` |
| Usuário comum | `cleiton@gmail.com.br` | `123456` |
| Usuário comum | `admin@gmail.com.br` | `123456` |
| Usuário inativo | `marcos@gmail.com.br` | `123456` |

O último usuário está com `is_active = False` e não deve conseguir autenticar-se. Ele foi incluído para permitir testes das regras de ativação de usuários.

**Segurança:** essas credenciais são destinadas exclusivamente ao ambiente de demonstração. Não utilize essas senhas em ambientes reais.

## 🖥️ Front-end

O front-end foi desenvolvido com Next.js, React e TypeScript. Ele permite interagir com a API por meio de páginas de consulta, formulários e filtros, respeitando as permissões de cada perfil.

### Páginas da aplicação

| Rota | Descrição |
|---|---|
| `/` | Página inicial com o modal de login. |
| `/tickets` | Lista os tickets e permite filtrá-los por cliente, status e responsável. |
| `/tickets/{id}` | Exibe os detalhes de um ticket e permite sua atualização conforme as permissões do usuário. |
| `/customers` | Lista os clientes e permite criar novos registros para administradores. |
| `/customers/{id}` | Exibe os dados de um cliente e permite sua edição para administradores. |
| `/users` | Lista os usuários e permite criar novos usuários. Acesso exclusivo para administradores. |
| `/users/{id}` | Exibe e permite atualizar os dados cadastrais de um usuário, respeitando as permissões de acesso. |

### Tickets

A página `/tickets` apresenta os tickets cadastrados em formato de cards, com opções de filtragem por cliente e status, além de um filtro para visualizar somente os tickets atribuídos ao usuário autenticado.

Administradores também podem criar novos tickets por meio de um modal.

Cada card permite acessar a página de detalhes do respectivo ticket.

Na página `/tickets/{id}`, administradores e responsáveis pelo ticket podem alterar seu status e sua prioridade.

### Clientes

A página `/customers` apresenta os clientes cadastrados em cards e permite acessar os detalhes de cada registro.

Administradores podem criar novos clientes e atualizar os dados cadastrais existentes.

Usuários comuns possuem permissão somente de consulta.

### Usuários

A página `/users` é exclusiva para administradores. Ela apresenta os usuários cadastrados e permite acessar seus dados ou criar novos registros.

A página `/users/{id}` permite consultar e atualizar os dados cadastrais conforme as permissões do usuário autenticado.

Usuários comuns podem alterar somente seu próprio nome, e-mail e senha. Administradores também podem alterar o perfil de acesso (`role`) e o estado de ativação (`is_active`).

Quando um usuário comum tenta acessar a listagem administrativa ou o cadastro de outro usuário, a aplicação o redireciona para `/tickets`.

### Navegação e sessão

O menu do cabeçalho permite acessar as páginas de clientes e, para administradores, a listagem de usuários.

A opção **Alterar meus dados** direciona o usuário para sua própria página de cadastro, enquanto a opção **Sair** encerra sua sessão na aplicação.

## 📈 Análise de dados

A etapa de análise utiliza Pandas para processar o dataset de avaliações de produtos da Amazon.

O processamento é implementado em `data/etl.py`, e os resultados são disponibilizados pela API em formato JSON.

Para consultar as métricas, basta iniciar o back-end e acessar:

`GET http://127.0.0.1:8000/metrics`

O arquivo `metrics.json` é gerado automaticamente quando necessário, desde que o dataset tenha sido baixado e colocado no diretório correto.

## 🔄 Workflow n8n

A pasta `n8n/` contém o arquivo JSON exportado do workflow desenvolvido no n8n.

Esse arquivo permite importar o workflow em uma instância do n8n para reproduzir a automação implementada no desafio.

Após importar o arquivo, confira a configuração do webhook e das integrações necessárias antes de executar o fluxo.

## 📸 Screenshots

A pasta `Screenshots/` contém capturas de tela da aplicação front-end e do workflow n8n em funcionamento.

Essas imagens ilustram as principais telas do sistema e a execução da automação implementada.

---

Desenvolvido como parte do desafio técnico para a **Stalse**.
