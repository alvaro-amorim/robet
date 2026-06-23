# ROBET_INTELLIGENCE_EVOLUTION_PLAN.md

# Robet — Plano de Evolução de Inteligência, Assertividade e Aprendizado Contínuo

## 1. Contexto Atual do Projeto

Este documento complementa o `PROJECT_CONSTITUTION.md` do Robet e registra as decisões estratégicas para aumentar a capacidade analítica, a qualidade das recomendações e o aprendizado contínuo do sistema.

O estado atual informado pelo Codex é positivo:

- O MVP mockado foi criado, validado, commitado e enviado.
- O ciclo de persistência foi implementado com PostgreSQL, SQLAlchemy e Alembic.
- Os dados mockados agora são persistidos: jogos, odds, recomendações, combinadas, pernas, rearranjos, banca, simulações e aprendizados.
- Foram criados endpoints de desenvolvimento para seed e reset.
- O dashboard foi atualizado para mostrar combinadas persistidas.
- O `.env` não foi commitado.
- `USE_MOCK_PROVIDERS=true` permanece ativo.
- Nenhuma API real foi chamada.
- Backend validado com `23 passed`.
- Frontend validado com `npm run build`.

## 2. Interpretação Técnica do Retorno do Codex

O retorno indica que o Robet saiu de um protótipo apenas visual/mockado e passou a ter uma base persistente. Isso é uma virada importante porque, a partir de agora, o sistema pode começar a formar memória histórica.

Antes da persistência, o Robet conseguia demonstrar o fluxo. Agora ele pode começar a acumular dados.

Isso abre caminho para:

- registrar odds reais ao longo do tempo;
- registrar recomendações feitas antes dos jogos;
- conferir acertos e erros;
- medir ROI simulado;
- medir calibração probabilística;
- comparar versões de estratégia;
- evoluir modelos;
- construir histórico próprio;
- auditar decisões;
- testar melhorias sem perder memória.

A decisão correta agora é não pular diretamente para “IA avançada decidindo apostas”. O caminho ideal é fortalecer a base de dados, o motor probabilístico e as métricas de avaliação.

## 3. Objetivo Deste Documento

Este documento define como o Robet deve evoluir para se tornar um sistema mais inteligente e mais assertivo, sem virar uma caixa-preta e sem depender de palpites de IA generativa.

O objetivo não é transformar o Robet em um bot que “adivinha resultados”.

O objetivo é transformá-lo em um laboratório de probabilidade que:

1. coleta dados;
2. salva tudo;
3. normaliza informações;
4. cria features;
5. estima probabilidades;
6. compara com o mercado;
7. mede valor esperado;
8. recomenda de forma simulada;
9. confere resultados;
10. aprende com erros;
11. testa versões novas;
12. promove apenas estratégias melhores.

## 4. Regra Central de Inteligência

A regra central do Robet deve ser:

> O Robet não deve buscar “acertar palpites”. Ele deve buscar estimar probabilidades melhor calibradas, encontrar valor esperado positivo e comprovar melhoria por dados históricos.

Taxa de acerto isolada não é suficiente.

Exemplo:

- Acertar 80% em odds 1.10 pode ser ruim.
- Acertar 45% em odds 2.50 pode ser excelente.
- Errar uma aposta pode ser aceitável se a decisão tinha valor esperado positivo.
- Acertar uma aposta pode ser ruim se a odd era mal precificada contra o usuário.

O Robet deve aprender a avaliar decisões, não apenas resultados.

## 5. Papel Correto do GPT-5.5 Thinking

O GPT-5.5 Thinking pode ser útil, mas não deve ser o cérebro decisor do Robet.

O papel correto é:

- analisar contexto textual;
- resumir atualidades;
- estruturar notícias em dados;
- identificar lesões e suspensões;
- extrair risco de escalação;
- detectar motivação;
- resumir aprendizados;
- compactar histórico;
- auditar erros;
- sugerir hipóteses para testes futuros.

O papel incorreto seria:

- decidir sozinho que uma aposta é boa;
- substituir o motor estatístico;
- gerar recomendações sem base numérica;
- alterar pesos automaticamente;
- funcionar a cada jogo sem controle de custo;
- transformar o Robet em caixa-preta.

Decisão:

> GPT-5.5 Thinking deve ser usado como camada de inteligência contextual e auditoria, não como motor principal de recomendação.

## 6. Arquitetura de Inteligência em Camadas

A evolução do Robet deve seguir uma arquitetura em camadas.

```text
1. Raw Data Layer
2. Normalization Layer
3. Feature Store
4. Market Intelligence Layer
5. Statistical Models Layer
6. Context Intelligence Layer
7. Ensemble Layer
8. Recommendation Engine
9. Learning Engine
10. Champion/Challenger Lab
```

Cada camada tem responsabilidade própria.

Nenhuma camada deve depender exclusivamente de IA generativa.

## 7. Camada 1 — Raw Data Layer

O Robet deve salvar tudo que recebe em formato bruto antes de transformar.

Dados brutos que devem ser salvos:

- resposta completa da API-Football;
- resposta completa da The Odds API;
- fixtures;
- odds por bookmaker;
- odds por mercado;
- odds por linha;
- timestamps;
- resultados;
- eventos;
- escalações;
- estatísticas;
- notícias;
- análises de contexto;
- recomendações;
- combinadas;
- rearranjos;
- resultados simulados.

Tabela sugerida:

```text
raw_api_payloads
- id
- provider
- endpoint
- request_params_json
- raw_payload_json
- payload_hash
- collected_at
- source_timestamp
- cost_estimate
- status
```

Motivo:

Se o Robet salvar apenas dados já resumidos, ele perde a chance de reprocessar o histórico com modelos melhores no futuro.

Regra:

> Todo dado externo importante deve ser salvo bruto antes de ser normalizado.

## 8. Camada 2 — Normalization Layer

O Robet precisa transformar dados externos em entidades internas consistentes.

Problemas esperados:

```text
Brazil
Brasil
BRA
Brazil National Team
Seleção Brasileira
```

Tudo precisa apontar para o mesmo `team_id`.

Entidades normalizadas:

```text
teams
competitions
matches
players
bookmakers
markets
market_selections
odds_snapshots
lineups
match_events
match_results
```

Decisão:

> Nenhum modelo deve usar nomes livres vindos diretamente das APIs. Sempre usar IDs internos normalizados.

## 9. Camada 3 — Feature Store

A Feature Store é a base de inteligência do Robet.

Ela deve registrar as variáveis usadas no momento exato da recomendação.

Exemplos de features pré-jogo:

```text
team_strength_home
team_strength_away
elo_home
elo_away
elo_difference
fifa_rank_home
fifa_rank_away
recent_form_home
recent_form_away
goals_for_avg_home
goals_against_avg_home
goals_for_avg_away
goals_against_avg_away
xg_for_avg_home
xg_against_avg_home
xg_for_avg_away
xg_against_avg_away
market_implied_home
market_implied_draw
market_implied_away
market_implied_over_2_5
best_odd
average_odd
market_margin
odds_dispersion
line_movement
days_rest_home
days_rest_away
motivation_score
injury_impact_score
lineup_uncertainty_score
news_sentiment_score
```

Tabela sugerida:

```text
match_feature_snapshots
- id
- match_id
- generated_at
- model_version
- features_json
- source_data_cutoff
```

Regra crítica:

> A Feature Store deve evitar lookahead bias. Nenhuma feature pode usar informação que não existia no momento da recomendação.

## 10. Camada 4 — Market Intelligence Layer

O mercado de odds deve ser tratado como uma fonte inteligente de probabilidade.

O Robet não deve ignorar o mercado. Ele deve entendê-lo.

Cálculos obrigatórios:

```text
best_odd
average_odd
median_odd
lowest_odd
market_spread
bookmaker_count
market_margin
raw_implied_probability
devig_probability
line_movement
opening_to_current_change
closing_line_value
```

### Remoção de margem da casa

Para mercado 1X2:

```text
p_home_raw = 1 / odd_home
p_draw_raw = 1 / odd_draw
p_away_raw = 1 / odd_away

sum_raw = p_home_raw + p_draw_raw + p_away_raw

p_home_fair = p_home_raw / sum_raw
p_draw_fair = p_draw_raw / sum_raw
p_away_fair = p_away_raw / sum_raw
```

Isso gera a probabilidade justa implícita do mercado.

Decisão:

> Antes de qualquer modelo avançado, o Robet deve implementar de-vig, margem de mercado, melhor odd, média de odds e dispersão entre bookmakers.

## 11. Camada 5 — Modelos Estatísticos Próprios

O Robet deve evoluir em modelos graduais.

### 11.1 Modelo baseline de mercado

Primeiro baseline:

```text
probabilidade_base = probabilidade_devig_do_mercado
```

Esse baseline é obrigatório.

O Robet só pode afirmar que está melhorando quando superar benchmarks simples.

### 11.2 Modelo Poisson para gols

Usado para:

- Over 1.5;
- Over 2.5;
- Under 2.5;
- ambas marcam;
- placares prováveis;
- total de gols esperado.

Inputs:

```text
attack_strength_home
defense_strength_home
attack_strength_away
defense_strength_away
league_average_goals
home_advantage
recent_form_adjustment
```

Outputs:

```text
expected_goals_home
expected_goals_away
prob_over_1_5
prob_over_2_5
prob_under_2_5
prob_btts_yes
scoreline_distribution
```

### 11.3 Modelo Elo

Especialmente relevante para Copa do Mundo.

Inputs:

```text
elo_home
elo_away
elo_difference
fifa_rank_difference
recent_international_form
continental_strength_adjustment
tournament_stage_weight
```

Outputs:

```text
home_win_probability
draw_probability
away_win_probability
team_strength_confidence
```

### 11.4 Modelos ML futuros

Somente após haver base histórica suficiente:

```text
logistic_regression
random_forest
xgboost
lightgbm
catboost
```

Targets possíveis:

```text
home_win
draw
away_win
over_2_5
under_2_5
btts_yes
favorite_win
favorite_not_lose
```

Decisão:

> O Robet deve começar com modelos interpretáveis e só depois adicionar ML mais complexo.

## 12. Camada 6 — Context Intelligence Layer com GPT

Essa camada usa GPT-5.5 Thinking ou modelos menores para transformar atualidades em dados estruturados.

Exemplos de entrada:

```text
notícias recentes
escalações prováveis
lesões
suspensões
entrevistas
situação do grupo
necessidade de resultado
motivação
viagem
descanso
clima
pressão externa
```

A saída deve ser sempre estruturada:

```json
{
  "match_context": {
    "home_motivation": 0.82,
    "away_motivation": 0.64,
    "home_injury_impact": 0.15,
    "away_injury_impact": 0.35,
    "home_lineup_uncertainty": 0.20,
    "away_lineup_uncertainty": 0.55,
    "rotation_risk": 0.40,
    "tactical_volatility": 0.62,
    "context_confidence": 0.71
  },
  "evidence": [
    {
      "claim": "Possível rotação no time visitante",
      "source_url": "https://...",
      "confidence": 0.66
    }
  ],
  "warnings": [
    "Escalação ainda não confirmada"
  ]
}
```

Regra:

> GPT nunca deve retornar apenas texto livre para o motor de recomendação. Ele deve retornar JSON validável.

## 13. Política de Uso de IA

A IA deve ser acionada por gatilhos, não constantemente.

### Usar IA quando:

```text
jogo importante
mudança grande de odds
notícia relevante nova
escalação provável divulgada
modelo e mercado discordam muito
Robet encontrou oportunidade relevante
fim do dia para resumir aprendizados
auditoria semanal
```

### Não usar IA quando:

```text
jogo sem oportunidade
odds pouco alteradas
dados já analisados
notícia duplicada
não há benefício incremental
custo do dia foi atingido
```

### Camadas de modelos

```text
Modelo barato:
- resumir notícias
- transformar texto em JSON
- compactar contexto

GPT-5.5 Thinking:
- auditorias profundas
- jogos de alta relevância
- revisão de erros importantes
- investigação de divergência entre modelo e mercado
```

Decisão:

> GPT-5.5 Thinking deve ser reservado para análises de alto valor, não para uso contínuo em todos os jogos.

## 14. Camada 7 — Ensemble Probabilístico

O Robet deve combinar múltiplas fontes de probabilidade.

Exemplo:

```text
Mercado devig: 52%
Poisson: 56%
Elo: 51%
ML histórico: 54%
Contexto GPT: ajuste +2%
```

O ensemble calcula uma probabilidade final:

```text
prob_final = soma_pesada(modelos)
```

Pesos iniciais sugeridos:

```text
market_weight = 0.45
poisson_weight = 0.20
elo_weight = 0.15
ml_weight = 0.15
context_weight = 0.05
```

No começo, o mercado deve ter peso alto.

Com o tempo, o Robet pode ajustar pesos por mercado, desde que isso seja validado fora da amostra.

Regra:

> Pesos do ensemble não devem ser alterados automaticamente em produção. Mudanças devem ser testadas como challenger.

## 15. Camada 8 — Recommendation Engine

O motor de recomendação deve gerar saídas ranqueadas, não ordens de aposta.

Cada recomendação deve conter:

```text
market
selection
bookmaker
odd
model_probability
market_probability
edge
expected_value
confidence
risk_label
quality_score
reason
blocking_reason
model_version
strategy_version
```

Classificações:

```text
STRONG_OPPORTUNITY
GOOD_OPPORTUNITY
WATCH
AVOID
INSUFFICIENT_DATA
HIGH_RISK
```

O texto de interface deve evitar linguagem de certeza.

Usar:

```text
Boa oportunidade simulada
```

Evitar:

```text
Aposte nisso
```

## 16. Camada 9 — Learning Engine

O Robet deve aprender com cada recomendação feita.

Salvar:

```text
match_id
recommendation_id
model_version
strategy_version
features_snapshot
market_snapshot
context_snapshot
probability_by_model
final_probability
odd_taken
best_available_odd
closing_odd
result
profit_loss_simulated
brier_component
log_loss_component
clv
post_match_notes
```

Aprendizados possíveis:

```text
Robet superestima favoritos com odds abaixo de 1.35
Over 2.5 está performando melhor em jogos com dispersão baixa de odds
Combinadas com mais de 4 pernas estão ruins
Mercados de cartões têm baixa confiança sem dados de árbitro
Modelo Poisson está superestimando gols em jogos de mata-mata
```

Regra:

> O aprendizado inicial deve gerar insights e sugestões. Não deve alterar estratégia automaticamente.

## 17. Champion/Challenger Lab

Para o Robet evoluir de verdade, ele deve comparar versões.

### Champion

Modelo atual aprovado.

### Challenger

Nova versão em teste.

Fluxo:

```text
1. Criar nova hipótese
2. Rodar backtest
3. Comparar com champion
4. Validar fora da amostra
5. Medir Brier, Log Loss, CLV, ROI e Yield
6. Promover somente se vencer de forma consistente
```

Tabela sugerida:

```text
model_versions
- id
- name
- version
- config_json
- status
- created_at
```

```text
model_evaluations
- id
- model_version_id
- evaluation_period_start
- evaluation_period_end
- brier_score
- log_loss
- roi
- yield
- clv
- total_recommendations
- promoted
```

Decisão:

> O Robet só deve promover uma estratégia nova após comparação objetiva contra a versão atual.

## 18. Métricas Obrigatórias

### 18.1 Brier Score

Mede calibração probabilística.

Se o Robet diz 70% muitas vezes, o evento precisa acontecer perto de 70% no longo prazo.

### 18.2 Log Loss

Penaliza excesso de confiança errado.

Se o Robet disser 95% e errar, deve ser penalizado fortemente.

### 18.3 Calibration Curve

Agrupa previsões por faixa:

```text
50–60%
60–70%
70–80%
80–90%
```

E mede frequência real.

### 18.4 Closing Line Value

Compara a odd recomendada com a odd de fechamento.

Se o Robet recomenda 2.10 e o mercado fecha 1.85, isso é um bom sinal, mesmo que a aposta isolada perca.

### 18.5 ROI simulado

Lucro/prejuízo em relação à banca simulada.

### 18.6 Yield

Lucro/prejuízo dividido pelo total simulado apostado.

### 18.7 Performance segmentada

Separar por:

```text
mercado
competição
faixa de odd
bookmaker
tipo de recomendação
nível de confiança
modelo
estratégia
número de pernas da combinada
```

## 19. Apostas Combinadas — Estratégia de Evolução

As combinadas devem ser tratadas como risco superior.

Problemas:

- acumulam margem da casa;
- aumentam variância;
- escondem correlações;
- parecem seguras por usarem odds individuais baixas;
- são difíceis de modelar corretamente.

### MVP atual

Usar:

```text
p_conjunta_ingênua = p1 * p2 * p3
p_conjunta_ajustada = p_conjunta_ingênua * penalidade_de_correlação
```

### Evolução futura

Usar probabilidades condicionais:

```text
P(A)
P(B | A)
P(C | A,B)
```

Exemplo:

```text
P(Time A vence)
P(+7 escanteios | Time A domina)
P(Menos de 5 cartões | árbitro + estilo + contexto)
```

O Robet deve aprender quais pernas derrubam qualidade da combinada.

Aprendizados úteis:

```text
perna de cartão reduz confiança
perna de escanteio sem histórico aumenta risco
combinação vitória favorita + over pode ser correlacionada
combinações com odds muito infladas têm baixa taxa de conversão
```

## 20. Base de Dados em Quatro Níveis

O Robet deve evoluir para arquitetura de dados em quatro níveis.

### Bronze — bruto

```text
raw_api_payloads
raw_news_documents
raw_odds_snapshots
```

### Silver — normalizado

```text
matches
teams
players
bookmakers
markets
odds_snapshots
lineups
events
results
```

### Gold — features

```text
match_features
market_features
team_features
context_features
bet_builder_features
```

### Platinum — aprendizado

```text
predictions
recommendations
simulation_results
model_versions
strategy_versions
learning_insights
model_evaluations
```

Decisão:

> O Robet deve separar armazenamento bruto, dados limpos, features e aprendizado.

## 21. Roadmap Recomendado a Partir do Estado Atual

### Ciclo 3 — Integração real API-Football

Objetivo:

- buscar jogos reais da Copa;
- salvar fixtures;
- salvar resultados;
- manter mocks como fallback;
- não gerar recomendações reais ainda sem validação.

Entregas:

```text
football_provider_real
raw_api_payloads
fixture_sync
result_sync
team_normalization
competition_normalization
```

### Ciclo 4 — Integração real The Odds API

Objetivo:

- coletar odds reais da Copa;
- salvar snapshots;
- calcular margem;
- calcular de-vig;
- identificar melhor odd;
- medir dispersão entre casas.

Entregas:

```text
odds_provider_real
odds_snapshots
bookmaker_normalization
market_normalization
best_price_engine
market_margin_engine
```

### Ciclo 5 — Market Intelligence

Objetivo:

- transformar odds em inteligência de mercado.

Entregas:

```text
de-vig probabilities
best price
average price
median price
market margin
bookmaker count
odds dispersion
line movement
closing line value
```

### Ciclo 6 — Modelo Poisson + Elo

Objetivo:

- gerar probabilidades próprias interpretáveis.

Entregas:

```text
poisson_goal_model
elo_strength_model
probability_by_market
baseline_vs_model_comparison
```

### Ciclo 7 — Avaliação real pós-jogo

Objetivo:

- conferir recomendações com resultados reais.

Entregas:

```text
settlement_engine
simulation_results
brier_score
log_loss
roi
yield
performance_by_market
```

### Ciclo 8 — Learning Dashboard

Objetivo:

- mostrar se o Robet está evoluindo.

Entregas:

```text
calibration_dashboard
model_evaluation_dashboard
learning_insights
strategy_comparison
```

### Ciclo 9 — Context Intelligence com GPT

Objetivo:

- transformar notícias e atualidades em features estruturadas.

Entregas:

```text
news_collector
context_analyzer
structured_context_json
context_feature_snapshot
cost_control
```

### Ciclo 10 — Ensemble + Champion/Challenger

Objetivo:

- comparar versões e promover melhorias com segurança.

Entregas:

```text
ensemble_engine
model_versions
strategy_versions
challenger_backtests
promotion_rules
```

## 22. Novas Tabelas Sugeridas Para Ciclos Futuros

```text
raw_api_payloads
teams
team_aliases
competitions
bookmakers
markets
market_selections
odds_market_summaries
match_feature_snapshots
context_analyses
model_versions
strategy_versions
model_predictions
model_evaluations
recommendation_evaluations
closing_line_snapshots
calibration_buckets
```

## 23. Novos Endpoints Sugeridos Para Ciclos Futuros

```text
POST /sync/football/fixtures
POST /sync/football/results
POST /sync/odds/world-cup
GET /market-intelligence/matches/{match_id}
GET /models/versions
GET /models/evaluations
GET /learning/calibration
GET /learning/clv
GET /learning/performance-by-market
POST /context/analyze-match
GET /context/matches/{match_id}
POST /lab/run-backtest
POST /lab/create-challenger
POST /lab/promote-challenger
```

Todos os endpoints de sincronização real devem respeitar limites de custo e rate limit.

## 24. Regras de Segurança Mantidas

Mesmo com evolução de inteligência, continuam proibidos:

```text
aposta real automática
login automatizado em casa de aposta
scraping de casas
bypass de anti-bot
bypass de CAPTCHA
uso de IA para decidir sem motor estatístico
mudança automática de estratégia em produção
uso de dados futuros em backtest
```

## 25. Decisão Final de Arquitetura

O Robet deve evoluir como laboratório científico de probabilidade, não como robô de palpite.

A arquitetura ideal é:

```text
Dados brutos
↓
Normalização
↓
Features
↓
Mercado como baseline
↓
Modelos estatísticos
↓
Contexto estruturado por IA
↓
Ensemble
↓
EV e risco
↓
Recomendação simulada
↓
Resultado
↓
Métrica
↓
Aprendizado
↓
Champion/Challenger
```

A IA generativa deve ampliar visão contextual e ajudar no aprendizado, mas o coração do sistema deve continuar sendo:

```text
dados
probabilidade
odds
valor esperado
calibração
backtest
validação temporal
controle de risco
```

## 26. Resumo Executivo

O Codex concluiu uma etapa essencial: o Robet agora tem persistência real em PostgreSQL. Isso permite construir uma base histórica própria.

A próxima fase não deve ser apostar, nem usar GPT como oráculo.

A próxima fase deve ser transformar dados reais em inteligência:

1. buscar jogos reais;
2. salvar odds reais;
3. calcular probabilidades implícitas;
4. remover margem das casas;
5. criar features;
6. rodar modelos estatísticos;
7. comparar com mercado;
8. simular recomendações;
9. conferir resultados;
10. medir calibração;
11. gerar aprendizados;
12. testar estratégias novas com champion/challenger.

O GPT-5.5 Thinking entra depois como analista de contexto e auditor, com custo controlado e saída estruturada em JSON.

Essa abordagem aumenta a chance de o Robet realmente evoluir sem virar caixa-preta e sem depender de superstição algorítmica.
