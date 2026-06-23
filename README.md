# Robet

Robet e um laboratorio local de analise probabilistica para futebol. O MVP comeca pela Copa do Mundo em modo pre-jogo, usando dados mockados para listar partidas, carregar odds, calcular probabilidade implicita, probabilidade interna inicial, edge, valor esperado, recomendacoes ranqueadas, combinadas manuais, simulacao de banca, historico persistido e aprendizados simples.

O Robet nao faz apostas reais, nao automatiza casas de aposta, nao faz scraping, nao burla anti-bot/CAPTCHA, nao implementa live betting neste ciclo e nao usa IA para decidir recomendacoes.

## Stack

- Backend: Python, FastAPI, Pydantic, SQLAlchemy, Alembic e pytest.
- Banco: PostgreSQL via Docker Compose.
- Frontend: React, TypeScript e Vite.
- Modo atual: `USE_MOCK_PROVIDERS=true`.

## Ambiente

Copie o exemplo de ambiente:

```powershell
Copy-Item .env.example .env
```

O `.env` real nunca deve ser commitado. Ele ja esta ignorado pelo `.gitignore`.

Mantenha este ciclo com mocks e seguranca ativa:

```env
USE_MOCK_PROVIDERS=true
AI_ENABLED=false
ENABLE_REAL_MONEY_MODE=false
ENABLE_AUTO_BETTING=false
ENABLE_BOOKMAKER_SCRAPING=false
ENABLE_ANTIBOT_BYPASS=false
ENABLE_LOGGED_BOOKMAKER_AUTOMATION=false
ENABLE_LIVE_MODE=false
```

Nao altere para `USE_MOCK_PROVIDERS=false` ate o fluxo persistido mockado estar validado.

## PostgreSQL

Suba o banco local:

```powershell
docker compose up -d postgres
```

O backend usa `DATABASE_URL` do `.env`, por padrao:

```env
DATABASE_URL=postgresql+psycopg://robet:robet_password@localhost:5432/robet
```

## Backend

Instale dependencias e rode migrations:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
alembic upgrade head
```

Rode a API:

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Com a API rodando, popule os dados mockados persistidos:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/dev/seed
```

Para resetar dados locais de desenvolvimento:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/dev/reset
```

`/dev/seed` e `/dev/reset` so funcionam quando `APP_ENV=development`.

## Frontend

Em outro terminal:

```powershell
cd frontend
npm install
npm run dev
```

Acesse `http://127.0.0.1:3000`.

## Endpoints

- `GET /health`
- `GET /matches`
- `GET /matches/world-cup`
- `GET /recommendations`
- `POST /recommendations/run-mock`
- `GET /bet-builder/history`
- `POST /bet-builder/evaluate`
- `POST /bet-builder/rearrange`
- `GET /bankroll`
- `GET /learning/insights`
- `GET /settings`
- `POST /dev/seed`
- `POST /dev/reset`

## Testes

```powershell
cd backend
python -m pytest
```

Os testes cobrem calculos probabilisticos, EV, stake, combinadas, flags proibidas, endpoints principais, criacao das entidades persistidas, seed idempotente, reset em desenvolvimento e bloqueio de seed/reset fora de desenvolvimento.

## Mocks

O ciclo atual usa jogos mockados da Copa, incluindo:

- Scotland x Brazil
- Morocco x Haiti
- Czech Republic x Mexico
- South Africa x South Korea
- Canada x Switzerland

Tambem existem odds mockadas para `h2h`, `totals`, escanteios e cartoes. A logica principal e estatistica simples e extensivel, sem decisao por IA.

## APIs reais

APIs reais continuam desativadas neste ciclo. Nao chame API-Football, The Odds API, OpenAI, casas de aposta ou sites externos. A futura ativacao exige o fluxo mockado persistido validado, tratamento de erro de API, cache/logs de chamada e entrada manual preservada.
