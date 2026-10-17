
# TicketDesk — Front-end Next.js

Front-end inicial para o projeto de tickets, usando Next.js App Router, TypeScript e CSS próprio. O Next.js funciona como BFF: o navegador chama rotas internas `/api/...`, e o servidor Next consulta o FastAPI.

## Requisitos

- Node.js 20.9+
- FastAPI executando localmente em `http://127.0.0.1:8000`

## Executar

```bash
npm install
cp .env.example .env.local
npm run dev
```

No Windows PowerShell, se preferir criar o arquivo manualmente:

```powershell
Copy-Item .env.example .env.local
```

Acesse `http://localhost:3000`.

Configure `FASTAPI_BASE_URL` em `.env.local` para o endereço que o processo Node consegue acessar. Não use `localhost` como endereço do navegador para chamar o FastAPI: o navegador chama apenas o Next.js.

## Fluxo de autenticação

- `POST /api/auth/login` chama `POST /auth/login` no FastAPI.
- O token de acesso é armazenado em cookie `HttpOnly`.
- O token nunca é enviado ao código JavaScript do navegador.
- `POST /api/auth/logout` limpa os cookies.
- `GET /api/auth/me` entrega os dados não secretos do usuário à interface.
- `app/api/backend/[...path]` encaminha métodos GET, POST, PATCH e DELETE para o FastAPI, acrescentando `Authorization: Bearer <token>`.

O cookie de usuário existe para apresentar nome e perfil na interface; ele não deve ser tratado como fonte definitiva de autorização. O FastAPI continua responsável por validar permissões. Para produção, revise também proteção CSRF, expiração/renovação de sessão, HTTPS, limites de tamanho de requisição e política de cookies.

## Endpoints esperados

- `POST /auth/login`
- `GET /tickets`, `GET /tickets/{id}`, `PATCH /tickets/{id}`, `POST /tickets/create`
- `GET /customer`, `GET /customer/{id}`, `PATCH /customer/{id}`, `POST /customer/create`
- `GET /user/all_users`, `GET /user/{id}`, `PATCH /user/{id}`, `POST /user/create`

Os tickets são esperados com os objetos opcionais `customer` e `assigned_user`, conforme a integração planejada. Se a API ainda retornar apenas IDs, ajuste os tipos/representação depois que o back-end for atualizado.

## Pontos de integração a conferir

1. O schema de login deve aceitar `{ "email": "...", "password": "..." }`.
2. O retorno de login esperado é `{ "tokens": { "token": "..." }, "id": 1, "nome": "...", "email": "...", "profileType": "admin" }`.
3. O corpo de PATCH de ticket usa `status` e `priority`.
4. O corpo de PATCH de customer usa `name`, `email` e `phone`.
5. O corpo de PATCH de usuário usa `name`, `email`, `password` (opcional) e, para admin, `role` e `is_active`.
6. O corpo de criação de ticket usa `customer_id`, `assigned_user_id`, `channel`, `subject`, `priority` e `status: "open"`. Ajuste caso o schema do FastAPI defina defaults diferentes.
7. Se os endpoints retornarem envelope como `{ "data": [...] }` em vez de arrays/objetos diretamente, adapte os pontos que leem a resposta.

## Tratamento de erros

O BFF repassa o status HTTP e detalhes da API, e a interface apresenta mensagens amigáveis em formulários e páginas. Em produção, evite mostrar detalhes internos do FastAPI; os detalhes técnicos devem ficar nos logs do servidor.

## Limitações conhecidas desta primeira versão

- O modal de criação de ticket precisa carregar também a lista de usuários; o código inicial aceita essa lista como propriedade, mas a página de tickets ainda precisa buscá-la antes de abrir o modal.
- O estado do usuário é carregado no `AuthProvider` para elementos client-side; as verificações de páginas protegidas também ocorrem no servidor.
- A autenticação inicial não implementa refresh token, conforme solicitado.
- Não há paginação nem pesquisa textual nesta primeira versão.
