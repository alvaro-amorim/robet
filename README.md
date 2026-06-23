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
- `GET /matches/real/world-cup`
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
- `GET /sync/football/status`
- `POST /sync/football/competitions`
- `POST /sync/football/world-cup-fixtures`
- `POST /sync/football/results`
- `GET /sync/odds/status`
- `POST /sync/odds/world-cup`
- `GET /odds/real/world-cup`
- `GET /market-intelligence/odds-events`
- `GET /market-intelligence/odds-events/{odds_event_id}`

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

O padrao do app continua mockado com `USE_MOCK_PROVIDERS=true`. O dashboard e os endpoints principais nao chamam API real automaticamente.

### Dados reais - API-Football

Este ciclo adiciona somente a fundacao de dados reais de futebol via API-Football:

- busca manual de competicoes;
- busca manual de fixtures da Copa;
- sync manual de resultados/status;
- salvamento de payload bruto em `raw_api_payloads`;
- normalizacao basica de competicoes, times, aliases e partidas;
- endpoint separado para listar fixtures reais persistidas.

Nao chama The Odds API, OpenAI, casas de aposta, scraping, login, automacao externa ou live mode.

Configure no `.env` real, sem commitar a chave:

```env
FOOTBALL_API_KEY=sua_chave_local
FOOTBALL_REAL_SYNC_ENABLED=false
FOOTBALL_SYNC_MAX_REQUESTS_PER_RUN=10
FOOTBALL_API_DAILY_REQUEST_LIMIT=100
FOOTBALL_DEFAULT_SEASON=2026
FOOTBALL_WORLD_CUP_SEARCH_TERMS=world cup,fifa world cup,copa do mundo
```

Para ativar sync real manualmente em desenvolvimento, escolha uma das opcoes:

```env
FOOTBALL_REAL_SYNC_ENABLED=true
```

Ou mantenha a flag desligada e use confirmacao explicita por request:

```powershell
Invoke-RestMethod -Method Post "http://127.0.0.1:8000/sync/football/competitions?confirm_real_sync=true"
Invoke-RestMethod -Method Post "http://127.0.0.1:8000/sync/football/world-cup-fixtures?confirm_real_sync=true"
Invoke-RestMethod -Method Post "http://127.0.0.1:8000/sync/football/results?confirm_real_sync=true"
```

Status de sync:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/sync/football/status
```

Listar fixtures reais persistidas:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/matches/real/world-cup
```

Esses endpoints so funcionam em `APP_ENV=development` neste ciclo e consomem quota da API-Football. Cada resposta real e salva bruta sem headers sensiveis e sem chave de API nos parametros persistidos.

Antes de sincronizar dados reais, rode migrations:

```powershell
cd backend
alembic upgrade head
```

### Dados reais - The Odds API

O Robet tambem pode sincronizar odds reais da Copa via The Odds API, mas isso continua sendo manual e separado do fluxo mockado padrao. Odds reais ainda nao geram recomendacoes reais neste ciclo.

Configure no `.env` real, sem commitar a chave:

```env
ODDS_API_KEY=sua_chave_local
ODDS_API_BASE_URL=https://api.the-odds-api.com/v4
ODDS_PRIMARY_SPORT_KEY=soccer_fifa_world_cup
ODDS_API_REGIONS=eu
ODDS_API_MARKETS=h2h,totals
ODDS_API_ODDS_FORMAT=decimal
ODDS_API_DATE_FORMAT=iso
ODDS_API_TIMEOUT_SECONDS=20
ODDS_API_CACHE_TTL_SECONDS=900
```

Status da configuracao:

```powershell
Invoke-RestMethod -Method Get "http://127.0.0.1:8000/sync/odds/status"
```

Sincronizar odds reais uma vez, consumindo credito da API:

```powershell
Invoke-RestMethod -Method Post "http://127.0.0.1:8000/sync/odds/world-cup?confirm_real_sync=true"
```

Listar eventos e inteligencia basica de mercado persistida:

```powershell
Invoke-RestMethod -Method Get "http://127.0.0.1:8000/odds/real/world-cup"
Invoke-RestMethod -Method Get "http://127.0.0.1:8000/market-intelligence/odds-events"
```

As odds reais podem ficar sem vinculo com partidas da API-Football enquanto a API-Football nao liberar fixtures da Copa 2026 no plano atual. Isso nao e erro: os eventos de odds sao persistidos de forma independente com `linked_match_id` nulo. O app continua com `USE_MOCK_PROVIDERS=true` e nao chama odds automaticamente ao abrir o dashboard.
