# Robet

Robet é um laboratório local de análise probabilística para futebol. O MVP começa pela Copa do Mundo em modo pré-jogo, usando dados mockados para listar partidas, carregar odds, calcular probabilidade implícita, probabilidade interna inicial, edge, valor esperado, recomendações ranqueadas, combinadas manuais, simulação de banca e aprendizados simples.

O Robet não faz apostas reais, não automatiza casas de aposta, não faz scraping, não burla anti-bot/CAPTCHA, não implementa live betting neste ciclo e não usa IA para decidir recomendações.

## Stack

- Backend: Python, FastAPI, Pydantic, SQLAlchemy, pytest.
- Banco: PostgreSQL via Docker Compose.
- Frontend: React, TypeScript, Vite.
- Modo atual: `USE_MOCK_PROVIDERS=true`.

## Configuração

1. Copie o exemplo de ambiente:

```powershell
Copy-Item .env.example .env
```

2. Mantenha o primeiro ciclo com mocks:

```env
USE_MOCK_PROVIDERS=true
ENABLE_REAL_MONEY_MODE=false
ENABLE_AUTO_BETTING=false
ENABLE_BOOKMAKER_SCRAPING=false
ENABLE_ANTIBOT_BYPASS=false
ENABLE_LOGGED_BOOKMAKER_AUTOMATION=false
ENABLE_LIVE_MODE=false
```

3. Suba o PostgreSQL:

```powershell
docker compose up -d postgres
```

O MVP mockado não depende de dados persistidos para funcionar, mas o PostgreSQL já fica previsto para a evolução de rastreabilidade.

## Backend

Instale as dependências e rode a API:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Endpoints principais:

- `GET /health`
- `GET /matches`
- `GET /matches/world-cup`
- `GET /recommendations`
- `POST /recommendations/run-mock`
- `POST /bet-builder/evaluate`
- `POST /bet-builder/rearrange`
- `GET /bankroll`
- `GET /learning/insights`
- `GET /settings`

## Frontend

Em outro terminal:

```powershell
cd frontend
npm install
npm run dev
```

Acesse `http://127.0.0.1:3000`.

## Testes

```powershell
cd backend
python -m pytest
```

Os testes cobrem probabilidade implícita, EV, stake, probabilidade conjunta, penalidade de correlação, avaliação de combinada, rearranjo, flags proibidas e recomendações ranqueadas.

## Mocks

O ciclo atual usa jogos mockados da Copa, incluindo:

- Scotland x Brazil
- Morocco x Haiti
- Czech Republic x Mexico
- South Africa x South Korea
- Canada x Switzerland

Também existem odds mockadas para `h2h`, `totals`, escanteios e cartões. A lógica principal é estatística simples e extensível, sem decisão por IA.

## Futuras APIs reais

Só altere para `USE_MOCK_PROVIDERS=false` depois do fluxo mockado estar validado. Quando isso acontecer, preencha `FOOTBALL_API_KEY`, `ODDS_API_KEY` e mantenha entrada manual como fallback para mercados não cobertos pelas APIs.
