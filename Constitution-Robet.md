# PROJECT_CONSTITUTION.md

# Sports Probability Lab — Constituição Técnica do Projeto

## 1. Identidade do Projeto

**Nome provisório:** Sports Probability Lab
**Domínio inicial:** Futebol
**Mercados iniciais:** Pré-jogo
**Mercados futuros:** Ao vivo, somente após validação do pré-jogo
**Natureza do projeto:** Laboratório de análise probabilística, simulação de banca e estudo de oportunidades em odds esportivas
**Status operacional inicial:** 100% simulado
**Uso com dinheiro real:** Fora do escopo inicial e bloqueado por padrão

---

## 2. Declaração de Missão

O objetivo deste projeto é construir um sistema inteligente para análise de futebol, focado inicialmente em **pré-jogo**, capaz de coletar dados esportivos, consultar odds, estimar probabilidades, identificar possíveis distorções de preço, simular decisões de apostas e registrar aprendizados.

O projeto não deve começar como um robô de apostas real.

O projeto deve começar como um **laboratório de inteligência esportiva**, onde cada análise, hipótese, decisão simulada e resultado seja registrado, auditável e explicável.

A proposta central é responder perguntas como:

* O que o sistema está vendo?
* Quais dados sustentam a análise?
* Qual odd foi observada?
* Qual probabilidade a odd implica?
* Qual probabilidade o modelo estima?
* Existe possível valor esperado positivo?
* Qual é o grau de confiança?
* Qual seria a stake simulada?
* O que aconteceu depois?
* O sistema estava certo ou errado?
* O que ele aprendeu com esse caso?

---

## 3. Filosofia Central

O sistema não deve tentar “adivinhar o resultado do jogo”.

O sistema deve estimar probabilidades.

A lógica correta não é:

> “O time A vai ganhar.”

A lógica correta é:

> “O modelo estima que a chance do evento é X%, enquanto a odd atual implica Y%. Se X for suficientemente maior que Y, pode existir valor esperado positivo, desde que o risco, a confiabilidade dos dados e a gestão de banca permitam.”

O sistema deve pensar sempre em termos de:

* probabilidade;
* incerteza;
* margem de erro;
* valor esperado;
* risco;
* confiabilidade da fonte;
* histórico de acerto;
* limite de exposição;
* aprendizado contínuo;
* explicabilidade.

---

## 4. Regra Absoluta de Evolução

O projeto seguirá obrigatoriamente esta ordem:

1. **Funciona**
2. **Funciona bem**
3. **Mede corretamente**
4. **Aprende com segurança**
5. **Escala**
6. **Fica mais inteligente**
7. **Só depois considera dinheiro real**

Nenhuma decisão de arquitetura deve sacrificar explicabilidade, segurança ou controle de custo em troca de complexidade prematura.

---

## 5. Escopo Inicial

### 5.1 O que entra no MVP inicial

O MVP inicial será focado em **futebol pré-jogo**.

Ele deve ser capaz de:

* listar jogos futuros;
* coletar odds pré-jogo;
* coletar dados históricos dos times;
* calcular probabilidade implícita das odds;
* estimar probabilidades próprias;
* comparar probabilidade estimada vs probabilidade implícita;
* calcular valor esperado;
* simular decisão de aposta;
* simular stake;
* registrar resultado;
* medir performance;
* explicar cada decisão;
* gerar relatório pós-jogo;
* gerar relatório diário/semanal;
* controlar custo de IA;
* funcionar sem automação em casas de aposta.

---

### 5.2 O que não entra no MVP inicial

Não entra no MVP inicial:

* aposta real;
* login automatizado em casas de aposta;
* scraping de casas de aposta;
* bypass de anti-bot;
* bypass de CAPTCHA;
* automação para “parecer humano”;
* live betting operacional;
* execução automática de apostas;
* múltiplos esportes;
* múltiplas estratégias complexas;
* reinforcement learning;
* modelo que altera suas próprias regras sem revisão;
* uso de IA generativa em toda atualização de dados.

---

## 6. Escopo Futuro

Após o pré-jogo estar estável, o projeto poderá evoluir para:

* acompanhamento ao vivo;
* odds ao vivo;
* eventos em tempo real;
* medição de delay;
* múltiplas fontes de dados;
* validação de divergências entre fontes;
* bloqueio por dados atrasados;
* bloqueio por mercado suspenso;
* simulação de apostas ao vivo;
* modelos por liga;
* modelos por mercado;
* ensemble de estratégias;
* aprendizado adaptativo;
* integração com exchange oficial;
* modo de sugestão manual;
* eventualmente, estudo de operação real com confirmação humana.

---

## 7. Aviso de Natureza Educacional e Risco

Este projeto não é recomendação financeira, recomendação de aposta ou promessa de lucro.

O sistema deve ser tratado como:

* ferramenta de estudo;
* laboratório de probabilidade;
* ambiente de simulação;
* sistema de pesquisa;
* produto técnico de aprendizado.

Qualquer uso com dinheiro real deve ser considerado uma fase futura, separada, revisada e bloqueada por critérios rígidos.

O projeto deve conter avisos claros de que apostas envolvem risco financeiro e podem causar perdas.

---

## 8. Princípios Não Negociáveis

### 8.1 Sem caixa-preta

Toda decisão precisa ter explicação.

Cada sinal deve registrar:

* dados usados;
* odds usadas;
* fonte da odd;
* horário da coleta;
* probabilidade implícita;
* probabilidade estimada;
* edge;
* valor esperado;
* confiança;
* risco;
* motivo da entrada;
* motivo para não entrar, quando aplicável;
* resultado;
* aprendizado.

---

### 8.2 Sem scraping não autorizado

O sistema não deve depender de scraping de casas de aposta, especialmente quando:

* houver login;
* houver proteção anti-bot;
* houver CAPTCHA;
* houver termos proibindo automação;
* houver tentativa de simular comportamento humano;
* houver intenção de contornar bloqueios.

Fontes permitidas:

* APIs oficiais;
* APIs agregadoras de odds;
* APIs de dados esportivos;
* exchanges com API oficial;
* feeds autorizados;
* entrada manual de odds;
* arquivos importados pelo usuário;
* dados públicos usados dentro dos termos permitidos.

---

### 8.3 IA generativa não decide sozinha

A IA generativa pode ajudar a:

* explicar análises;
* resumir dados;
* gerar relatórios;
* identificar padrões de erro;
* sugerir hipóteses;
* transformar dados técnicos em linguagem natural.

Mas a decisão operacional deve vir de:

* regras matemáticas;
* modelos estatísticos;
* motor de valor esperado;
* motor de risco;
* gestão de banca;
* validação de dados.

---

### 8.4 Controle de custo obrigatório

O sistema deve medir e registrar:

* chamadas de API de odds;
* chamadas de API de futebol;
* chamadas de IA;
* tokens consumidos;
* custo estimado por análise;
* custo estimado por jogo;
* custo diário;
* custo mensal;
* cache utilizado;
* economia gerada por cache.

Nenhuma análise deve chamar IA de forma exagerada.

---

### 8.5 Pré-jogo antes do ao vivo

O projeto deve seguir obrigatoriamente esta ordem:

1. pré-jogo com dados históricos;
2. pré-jogo com odds reais;
3. pré-jogo com simulação de banca;
4. pré-jogo com relatório e aprendizado;
5. pré-jogo validado por métricas;
6. somente depois: ao vivo observacional;
7. depois: ao vivo com decisão simulada;
8. depois: estudo de integração autorizada.

---

## 9. Conceitos Fundamentais

### 9.1 Odd decimal

A odd decimal representa o retorno bruto por unidade apostada.

Exemplo:

```text
Odd 2.00
Stake simulada: R$ 10
Retorno bruto se vencer: R$ 20
Lucro líquido: R$ 10
```

---

### 9.2 Probabilidade implícita

A probabilidade implícita aproximada é:

```text
probabilidade_implicita = 1 / odd
```

Exemplo:

```text
Odd 2.00 = 1 / 2.00 = 0.50 = 50%
Odd 1.80 = 1 / 1.80 = 0.5555 = 55.55%
Odd 3.00 = 1 / 3.00 = 0.3333 = 33.33%
```

---

### 9.3 Margem da casa

Em mercados com múltiplas opções, a soma das probabilidades implícitas geralmente passa de 100%.

Essa diferença é a margem embutida da casa.

Exemplo:

```text
Time A: odd 2.00 = 50%
Empate: odd 3.40 = 29.41%
Time B: odd 3.60 = 27.77%

Soma = 107.18%
Margem aproximada = 7.18%
```

O sistema deve descontar ou considerar essa margem antes de afirmar que existe valor.

---

### 9.4 Probabilidade estimada

É a probabilidade calculada pelo modelo interno do sistema.

Ela pode ser baseada em:

* força dos times;
* mando de campo;
* forma recente;
* gols marcados;
* gols sofridos;
* xG, quando disponível;
* desfalques;
* odds de mercado;
* histórico da liga;
* modelo Poisson;
* Elo rating;
* regressão;
* machine learning futuro.

---

### 9.5 Edge

Edge é a diferença entre a probabilidade estimada e a probabilidade implícita ajustada.

Exemplo:

```text
Probabilidade estimada pelo modelo: 56%
Probabilidade implícita da odd: 49%
Edge bruto: +7 pontos percentuais
```

O sistema só deve considerar entrada simulada quando o edge passar de um limite mínimo.

---

### 9.6 Valor esperado

Valor esperado é a estimativa matemática de retorno médio de uma decisão ao longo de muitas ocorrências semelhantes.

Fórmula simplificada:

```text
EV = (probabilidade_de_acerto * lucro_liquido) - (probabilidade_de_erro * stake)
```

Exemplo:

```text
Stake: R$ 10
Odd: 2.10
Lucro líquido se vencer: R$ 11
Probabilidade estimada: 55%
Probabilidade de erro: 45%

EV = (0.55 * 11) - (0.45 * 10)
EV = 6.05 - 4.50
EV = R$ 1.55
```

Nesse exemplo, a decisão teria EV positivo de R$ 1,55 por R$ 10 simulados.

---

### 9.7 Confiança

Confiança não é a mesma coisa que probabilidade.

Probabilidade responde:

> Qual a chance do evento acontecer?

Confiança responde:

> O quanto o sistema confia na própria estimativa?

A confiança deve considerar:

* qualidade dos dados;
* quantidade de dados históricos;
* estabilidade da liga;
* disponibilidade de escalação;
* divergência entre fontes;
* histórico do modelo nesse mercado;
* histórico do modelo nessa liga;
* proximidade do jogo;
* variação brusca das odds;
* anomalias detectadas.

---

### 9.8 Stake

Stake é o valor da aposta simulada.

No MVP, stake deve ser conservadora e baseada em gestão de banca.

Exemplo:

```text
Banca simulada: R$ 1.000
Risco máximo por entrada: 1%
Stake máxima: R$ 10
```

O sistema não deve aumentar stake para recuperar perdas.

---

## 10. Mercados Iniciais

O projeto começará com poucos mercados.

### 10.1 Mercados do MVP

Mercados iniciais permitidos:

1. **Over 1.5 gols**
2. **Over 2.5 gols**
3. **Ambas marcam — Sim**
4. **Resultado final 1X2**

---

### 10.2 Mercados não prioritários no MVP

Não priorizar no início:

* handicaps asiáticos;
* cartões;
* escanteios;
* jogador para marcar;
* placar exato;
* múltiplas;
* cashout;
* mercado ao vivo;
* linhas alternativas em excesso.

Esses mercados podem ser adicionados depois que o motor principal estiver validado.

---

## 11. Ligas Iniciais

O sistema deve começar com poucas ligas, priorizando qualidade de dados.

Sugestão inicial:

* Brasileirão Série A;
* Premier League;
* La Liga;
* Champions League;
* Copa do Mundo ou torneios com alta disponibilidade de dados, quando aplicável.

A escolha final deve considerar:

* disponibilidade da API;
* volume histórico;
* confiabilidade dos dados;
* volume de odds;
* liquidez;
* número de jogos;
* estabilidade estatística.

---

## 12. Fontes de Dados

### 12.1 Categorias de fontes

O sistema precisará de três categorias principais:

1. **Dados esportivos**
2. **Odds**
3. **IA generativa**

Futuramente:

4. **Dados ao vivo**
5. **Exchange oficial**
6. **Fonte secundária de validação**

---

### 12.2 API de dados esportivos

Responsável por:

* jogos;
* calendário;
* times;
* ligas;
* tabelas;
* resultados;
* estatísticas históricas;
* forma recente;
* escalações, se disponível;
* eventos, futuramente;
* dados ao vivo, futuramente.

Exemplos de provedores a avaliar:

* API-Football;
* API-Sports;
* SportMonks;
* football-data.org;
* Sportradar, em fase avançada.

---

### 12.3 API de odds

Responsável por:

* odds pré-jogo;
* odds por bookmaker;
* mercados disponíveis;
* formato decimal;
* snapshots de odds;
* odds históricas, se disponível;
* odds ao vivo, futuramente;
* atualização de linhas.

Exemplos de provedores a avaliar:

* The Odds API;
* OpticOdds;
* OddsAPI.io;
* SportsDataIO;
* Sportradar Odds;
* Betfair Exchange API, se aplicável.

---

### 12.4 Entrada manual de odds

Quando uma casa onde o usuário possui conta não disponibilizar API autorizada, o sistema poderá aceitar entrada manual.

Exemplo:

```json
{
  "match": "Time A vs Time B",
  "market": "Over 2.5",
  "bookmaker": "Casa informada manualmente",
  "odd": 2.05,
  "observed_at": "2026-06-23T14:30:00-03:00"
}
```

O sistema poderá calcular se aquela odd teria valor.

Isso permite uso prático sem automação proibida.

---

### 12.5 Fontes proibidas

O sistema não deve usar:

* scraping de sites protegidos;
* scraping de conta logada;
* bypass de CAPTCHA;
* bypass de fingerprint;
* simulação de comportamento humano para enganar anti-bot;
* automação invisível em casa de aposta;
* engenharia reversa de APIs privadas;
* qualquer método que viole termos de uso.

---

## 13. Arquitetura Geral

### 13.1 Visão macro

```text
[Football Data APIs]
        ↓
[Odds APIs]
        ↓
[Data Ingestion Layer]
        ↓
[Normalization Layer]
        ↓
[Match Intelligence Store]
        ↓
[Pre-Match Analysis Engine]
        ↓
[Probability Engine]
        ↓
[Expected Value Engine]
        ↓
[Risk & Bankroll Engine]
        ↓
[Decision Simulator]
        ↓
[Explanation Engine]
        ↓
[Learning Engine]
        ↓
[Dashboard]
```

---

### 13.2 Arquitetura futura para ao vivo

```text
[Live Match Data Source A]
        ↓
[Live Match Data Source B]
        ↓
[Live Odds Source]
        ↓
[Real-Time Ingestion]
        ↓
[Event Normalizer]
        ↓
[Multi-Source Validator]
        ↓
[Match State Engine]
        ↓
[Live Probability Engine]
        ↓
[Live EV Engine]
        ↓
[Live Risk Gate]
        ↓
[Simulated Live Decision]
        ↓
[Audit Log]
        ↓
[Dashboard Tempo Real]
```

---

## 14. Stack Tecnológica Recomendada

### 14.1 Backend

Recomendação:

```text
Python + FastAPI
```

Motivos:

* excelente ecossistema de dados;
* fácil integração com modelos;
* bom suporte para APIs;
* bom suporte para jobs assíncronos;
* compatível com scikit-learn, pandas, NumPy, LightGBM, XGBoost;
* bom para o Codex desenvolver em etapas.

---

### 14.2 Frontend

Recomendação:

```text
React ou Next.js
```

Motivos:

* bom para dashboard;
* gráficos interativos;
* componentes reutilizáveis;
* boa experiência visual;
* integração fácil com API backend.

---

### 14.3 Banco de dados

Recomendação inicial:

```text
PostgreSQL
```

Motivos:

* confiável;
* relacional;
* bom para auditoria;
* bom para consultas;
* escalável o suficiente para o MVP;
* aceita JSONB para dados flexíveis.

Para pesquisa local ou análises pesadas:

```text
DuckDB
```

pode ser usado futuramente em notebooks ou pipelines analíticos.

---

### 14.4 Cache e filas

MVP:

```text
Redis opcional
```

Futuro:

```text
Redis Streams
```

ou, se o projeto crescer muito:

```text
Kafka
```

No início, evitar Kafka.

---

### 14.5 IA e modelos

Para cálculo:

```text
Python
pandas
NumPy
scikit-learn
statsmodels
```

Futuro:

```text
XGBoost
LightGBM
PyTorch
```

Para IA generativa:

```text
OpenAI API ou provedor equivalente
```

Uso controlado por política de custo.

---

## 15. Módulos do Sistema

## 15.1 Data Ingestion Layer

Responsável por coletar dados externos.

Funções:

* buscar jogos;
* buscar ligas;
* buscar times;
* buscar estatísticas;
* buscar odds;
* buscar resultados;
* armazenar snapshots;
* respeitar rate limit;
* registrar falhas;
* registrar custo estimado;
* controlar cache.

Requisitos:

* toda chamada externa deve ser logada;
* toda resposta deve ter timestamp;
* toda fonte deve ter identificador;
* toda coleta deve registrar status;
* toda falha deve ser rastreável.

---

## 15.2 Normalization Layer

Responsável por transformar dados de diferentes fontes em formato interno único.

Problema que resolve:

* uma API chama o time de “Flamengo”;
* outra chama “CR Flamengo”;
* outra usa ID próprio;
* outra retorna nomes em inglês;
* outra retorna campos diferentes.

O sistema deve criar identidade interna.

Entidades normalizadas:

* `team`;
* `competition`;
* `season`;
* `match`;
* `market`;
* `bookmaker`;
* `odds_snapshot`;
* `stat_snapshot`.

---

## 15.3 Match Catalog

Responsável por manter catálogo único de partidas.

Campos principais:

* ID interno do jogo;
* IDs externos por fonte;
* mandante;
* visitante;
* liga;
* temporada;
* data;
* status;
* placar final;
* status de análise;
* status de resultado.

---

## 15.4 Pre-Match Analysis Engine

Responsável por gerar análise antes do jogo.

Deve considerar:

* força do mandante;
* força do visitante;
* forma recente;
* gols pró;
* gols contra;
* mando de campo;
* média da liga;
* odds de abertura;
* odds atuais;
* variação das odds;
* margem de mercado;
* dados incompletos;
* confiança dos dados.

Saída esperada:

```json
{
  "match_id": "internal_match_123",
  "market": "over_2_5",
  "model_probability": 0.54,
  "implied_probability": 0.47,
  "edge": 0.07,
  "expected_value": 0.12,
  "confidence": 0.68,
  "decision": "SIMULATE_ENTRY",
  "risk_level": "MEDIUM",
  "explanation": "O modelo estima valor moderado em Over 2.5 porque..."
}
```

---

## 15.5 Probability Engine

Responsável por estimar probabilidades.

### Versão inicial

Começar simples, com:

* médias de gols;
* ataque vs defesa;
* mando de campo;
* média da liga;
* modelo Poisson;
* ajuste por forma recente;
* ajuste por odds de mercado.

### Versões futuras

Adicionar:

* Elo rating;
* xG;
* regressão logística;
* gradient boosting;
* calibração de probabilidades;
* ensemble;
* modelo por liga;
* modelo por mercado.

---

## 15.6 Expected Value Engine

Responsável por calcular:

* probabilidade implícita;
* margem da casa;
* edge;
* valor esperado;
* EV por R$ 1;
* EV por stake;
* retorno potencial;
* risco de perda;
* qualidade da oportunidade.

Regra:

O sistema nunca deve sugerir entrada simulada apenas porque “acha que vai acontecer”.

Precisa haver:

* odd;
* probabilidade estimada;
* probabilidade implícita;
* edge mínimo;
* EV positivo;
* confiança mínima;
* risco permitido.

---

## 15.7 Risk & Bankroll Engine

Responsável por proteger a banca simulada.

Configuração inicial recomendada:

```yaml
initial_bankroll: 1000.00
max_stake_per_bet_percent: 1.0
max_daily_loss_percent: 3.0
max_open_exposure_percent: 5.0
max_bets_per_day: 10
stop_after_consecutive_losses: 3
allow_martingale: false
allow_loss_recovery_mode: false
```

Regras absolutas:

* não usar martingale;
* não aumentar stake para recuperar prejuízo;
* não entrar se o limite diário foi atingido;
* não entrar se a confiança dos dados for baixa;
* não entrar se o edge for pequeno;
* não entrar se o mercado não tiver histórico suficiente;
* não entrar se a odd estiver fora do range permitido;
* registrar motivo de bloqueio.

---

## 15.8 Decision Simulator

Responsável por simular decisões.

Decisões possíveis:

```text
SIMULATE_ENTRY
WAIT
IGNORE
BLOCKED_BY_RISK
BLOCKED_BY_LOW_CONFIDENCE
BLOCKED_BY_DATA_QUALITY
BLOCKED_BY_COST_LIMIT
```

Cada decisão deve ter:

* motivo;
* regras aplicadas;
* mercado;
* odd;
* stake simulada;
* resultado esperado;
* risco;
* confiança;
* explicação.

---

## 15.9 Simulated Bookmaker

Responsável por simular apostas.

Funções:

* registrar entrada;
* registrar odd;
* registrar stake;
* registrar resultado;
* calcular lucro/prejuízo;
* atualizar banca;
* calcular ROI;
* calcular yield;
* calcular drawdown;
* calcular sequência de vitórias/perdas.

---

## 15.10 Explanation Engine

Responsável por transformar dados em explicação.

A explicação deve ter duas versões:

### Resumo curto

Exemplo:

```text
Entrada simulada em Over 2.5. O modelo estima 54% de chance, enquanto a odd implica 47%. Edge positivo de 7 p.p., confiança média e stake limitada a 1% da banca.
```

### Explicação detalhada

Exemplo:

```text
O sistema identificou possível valor em Over 2.5 porque ambas as equipes apresentam média ofensiva acima da média da liga, sofrem gols com frequência e o mercado oferece odd acima da probabilidade estimada pelo modelo. A confiança foi classificada como média porque as escalações ainda não foram confirmadas e a variação recente da odd foi relevante.
```

---

## 15.11 Learning Engine

Responsável por analisar resultados.

Aprendizados possíveis:

* modelo superestima favoritos;
* modelo subestima mandantes;
* Over 2.5 está ruim em determinada liga;
* ambas marcam performa melhor em ligas específicas;
* odds muito baixas têm baixa rentabilidade;
* edge pequeno não compensa;
* jogos com dados incompletos performam pior;
* decisões com confiança baixa devem ser bloqueadas;
* determinada fonte de odds tem atualização ruim;
* determinada liga tem alto ruído.

O aprendizado inicial não deve alterar regras automaticamente.

Ele deve gerar sugestões versionadas.

---

## 15.12 Cost Control Engine

Responsável por controlar custos.

Deve registrar:

* provider;
* endpoint;
* horário;
* tokens;
* créditos;
* custo estimado;
* cache hit/miss;
* usuário/processo que chamou;
* motivo da chamada;
* resultado.

Políticas:

* IA não deve ser chamada em toda atualização de odd;
* IA deve ser chamada apenas em eventos relevantes;
* relatórios devem usar cache;
* análises repetidas devem reutilizar dados;
* chamadas caras devem exigir autorização lógica;
* limite mensal deve ser configurável.

---

## 16. Uso de IA Generativa

## 16.1 Onde usar IA

Usar IA para:

* explicar decisão;
* gerar relatório pós-jogo;
* resumir aprendizados;
* detectar padrões nos erros;
* comparar análises antigas;
* sugerir melhorias de estratégia;
* organizar documentação;
* gerar texto para dashboard.

---

## 16.2 Onde não usar IA

Não usar IA generativa para:

* coletar odds;
* calcular probabilidade diretamente sem modelo;
* tomar decisão sozinha;
* fazer scraping;
* burlar anti-bot;
* substituir motor matemático;
* alterar estratégia automaticamente em produção;
* rodar a cada pequena mudança de dado.

---

## 16.3 Política de chamadas de IA

Chamar IA somente quando:

* um sinal relevante for gerado;
* uma análise pré-jogo for finalizada;
* um jogo terminar;
* um relatório diário for gerado;
* uma auditoria semanal for solicitada;
* o usuário pedir explicação detalhada.

Não chamar IA quando:

* odds mudarem levemente;
* dados forem atualizados sem novo sinal;
* análise já estiver em cache;
* jogo não cumprir critérios mínimos;
* custo diário estiver próximo do limite.

---

## 16.4 Níveis de IA

### Nível 1 — Sem IA

Usado para:

* cálculos;
* odds;
* EV;
* stake;
* risco;
* filtros.

### Nível 2 — IA barata

Usada para:

* explicação curta;
* resumo de decisão;
* relatório simples.

### Nível 3 — IA avançada

Usada para:

* auditoria semanal;
* revisão profunda;
* análise de padrões;
* planejamento de evolução.

---

## 17. Banco de Dados

## 17.1 Tabelas principais

### providers

Armazena provedores externos.

Campos:

```text
id
name
type
base_url
is_active
rate_limit
cost_model
created_at
updated_at
```

Tipos:

```text
football_data
odds
ai
exchange
manual
```

---

### competitions

```text
id
provider_id
external_id
name
country
tier
is_active
created_at
updated_at
```

---

### teams

```text
id
name
normalized_name
country
created_at
updated_at
```

---

### team_external_ids

```text
id
team_id
provider_id
external_id
external_name
created_at
updated_at
```

---

### matches

```text
id
competition_id
season
home_team_id
away_team_id
start_time
status
home_score
away_score
created_at
updated_at
```

Status possíveis:

```text
scheduled
pre_match_analysis_ready
in_play
finished
cancelled
postponed
unknown
```

---

### odds_snapshots

```text
id
match_id
provider_id
bookmaker
market
selection
odd_decimal
implied_probability
captured_at
source_timestamp
is_live
raw_payload
created_at
```

---

### match_stat_snapshots

```text
id
match_id
provider_id
snapshot_type
captured_at
raw_payload
normalized_payload
created_at
```

---

### model_predictions

```text
id
match_id
strategy_version_id
market
selection
model_probability
confidence
features_used
created_at
```

---

### value_assessments

```text
id
match_id
prediction_id
odds_snapshot_id
implied_probability
adjusted_implied_probability
edge
expected_value
quality_score
created_at
```

---

### decisions

```text
id
match_id
value_assessment_id
decision_type
reason
confidence
risk_level
created_at
```

Decision types:

```text
SIMULATE_ENTRY
WAIT
IGNORE
BLOCKED_BY_RISK
BLOCKED_BY_LOW_EDGE
BLOCKED_BY_LOW_CONFIDENCE
BLOCKED_BY_DATA_QUALITY
BLOCKED_BY_COST_LIMIT
```

---

### simulated_bets

```text
id
decision_id
match_id
market
selection
odd_decimal
stake
status
result
profit_loss
bankroll_before
bankroll_after
placed_at
settled_at
created_at
updated_at
```

Status:

```text
open
won
lost
void
cancelled
pending
```

---

### bankroll_snapshots

```text
id
bankroll
available_balance
open_exposure
daily_profit_loss
max_drawdown
created_at
```

---

### strategy_versions

```text
id
name
version
description
config
is_active
created_at
updated_at
```

---

### explanations

```text
id
decision_id
short_explanation
detailed_explanation
ai_model
ai_cost_estimate
created_at
```

---

### learning_insights

```text
id
scope
insight_type
description
evidence
confidence
suggested_action
status
created_at
updated_at
```

Status:

```text
new
reviewed
accepted
rejected
implemented
```

---

### api_usage_logs

```text
id
provider_id
endpoint
request_type
tokens_input
tokens_output
credits_used
estimated_cost
cache_hit
status
created_at
```

---

### source_health_logs

```text
id
provider_id
status
latency_ms
last_success_at
last_error
confidence_score
created_at
```

---

## 18. Fluxo Pré-Jogo

## 18.1 Pipeline

```text
1. Buscar jogos futuros
2. Normalizar times e ligas
3. Buscar odds pré-jogo
4. Calcular probabilidade implícita
5. Buscar estatísticas históricas
6. Gerar features
7. Rodar modelo probabilístico
8. Comparar modelo vs mercado
9. Calcular edge
10. Calcular EV
11. Aplicar regras de risco
12. Simular ou bloquear entrada
13. Gerar explicação
14. Registrar decisão
15. Aguardar resultado
16. Liquidar simulação
17. Atualizar métricas
18. Gerar aprendizado
```

---

## 18.2 Exemplo de análise pré-jogo

```json
{
  "match": "Time A vs Time B",
  "market": "Over 2.5",
  "bookmaker": "Provider Odds",
  "odd": 2.05,
  "implied_probability": 0.4878,
  "model_probability": 0.5420,
  "edge": 0.0542,
  "expected_value": 0.1111,
  "confidence": 0.67,
  "decision": "SIMULATE_ENTRY",
  "stake": 10.00,
  "bankroll": 1000.00,
  "risk_level": "MEDIUM"
}
```

---

## 19. Futuro Fluxo Ao Vivo

O ao vivo não será implementado antes do pré-jogo estar validado.

Quando for implementado, o fluxo será:

```text
1. Receber eventos ao vivo
2. Receber odds ao vivo
3. Medir delay
4. Validar fontes
5. Atualizar estado do jogo
6. Detectar eventos críticos
7. Bloquear decisões se mercado suspenso
8. Bloquear decisões se dados divergentes
9. Atualizar probabilidades
10. Calcular EV ao vivo
11. Aplicar risco
12. Simular decisão
13. Registrar tudo
```

---

## 20. Controle de Delay no Ao Vivo

O sistema futuro deve medir:

* horário informado pela fonte;
* horário recebido pelo sistema;
* tempo desde o último update;
* divergência entre fontes;
* mercado suspenso;
* evento crítico não confirmado.

Regras futuras:

```text
Se dados do jogo estão atrasados, bloquear entrada.
Se odds estão atrasadas, bloquear entrada.
Se fontes divergem em gol, pênalti ou cartão vermelho, bloquear entrada.
Se mercado está suspenso, bloquear entrada.
Se evento crítico ocorreu há poucos segundos, aguardar estabilização.
```

---

## 21. Multi-Fonte no Ao Vivo

No futuro, o sistema poderá usar três fontes:

### Fonte A — eventos rápidos

Responsável por capturar eventos do jogo.

### Fonte B — validação

Responsável por confirmar eventos críticos.

### Fonte C — odds

Responsável por mostrar preço de mercado.

O sistema deve tratar fontes como sensores.

Cada fonte terá:

* confiabilidade;
* atraso médio;
* frequência de erro;
* cobertura;
* custo;
* prioridade.

---

## 22. Dashboard

## 22.1 Tela principal

Deve mostrar:

* jogos do dia;
* horário;
* liga;
* mercado analisado;
* odd;
* probabilidade implícita;
* probabilidade estimada;
* edge;
* EV;
* confiança;
* decisão;
* status da simulação.

---

## 22.2 Tela de análise detalhada

Para cada jogo:

* dados dos times;
* estatísticas recentes;
* odds capturadas;
* variação das odds;
* features usadas;
* probabilidade do modelo;
* comparação com mercado;
* explicação curta;
* explicação detalhada;
* decisão simulada;
* risco;
* banca simulada;
* resultado após o jogo.

---

## 22.3 Tela de banca simulada

Mostrar:

* banca inicial;
* banca atual;
* lucro/prejuízo;
* ROI;
* yield;
* drawdown;
* sequência de perdas;
* exposição aberta;
* stake média;
* maior perda;
* maior ganho;
* performance por mercado;
* performance por liga.

---

## 22.4 Tela de aprendizado

Mostrar:

* padrões de erro;
* melhores mercados;
* piores mercados;
* melhores ligas;
* piores ligas;
* sugestões de ajuste;
* comparação entre versões de estratégia;
* métricas de calibração;
* evolução da banca simulada.

---

## 22.5 Tela de custos

Mostrar:

* custo diário;
* custo mensal;
* chamadas por API;
* chamadas de IA;
* tokens;
* cache hit rate;
* custo por jogo analisado;
* custo por relatório;
* alertas de limite.

---

## 23. Métricas de Performance

Métricas obrigatórias:

* número de análises;
* número de entradas simuladas;
* taxa de acerto;
* ROI;
* yield;
* lucro/prejuízo;
* drawdown máximo;
* odds média;
* stake média;
* EV médio;
* edge médio;
* performance por mercado;
* performance por liga;
* performance por faixa de odd;
* performance por nível de confiança;
* performance por versão de estratégia.

---

## 24. Métricas de Calibração

O sistema deve medir se suas probabilidades são bem calibradas.

Exemplo:

Se o modelo diz 60% de chance em 100 eventos semelhantes, aproximadamente 60 deveriam acontecer ao longo de grande amostra.

Métricas futuras:

* Brier Score;
* Log Loss;
* curva de calibração;
* comparação por buckets de probabilidade;
* comparação contra mercado.

---

## 25. Benchmarks Obrigatórios

O sistema deve ser comparado contra estratégias simples.

Benchmarks iniciais:

1. apostar sempre no favorito;
2. apostar sempre em Over 1.5;
3. apostar sempre em Over 2.5;
4. seguir probabilidade implícita do mercado;
5. estratégia aleatória controlada;
6. não apostar.

Objetivo:

Evitar que o sistema pareça bom sem realmente superar alternativas simples.

---

## 26. Modelos Iniciais

## 26.1 Modelo base — Poisson simples

Para mercados de gols, começar com modelo Poisson.

Inputs:

* média de gols do mandante;
* média de gols do visitante;
* média de gols sofridos;
* média da liga;
* fator casa;
* forma recente.

Outputs:

* probabilidade de 0, 1, 2, 3+ gols;
* probabilidade de Over 1.5;
* probabilidade de Over 2.5;
* probabilidade de ambas marcam.

---

## 26.2 Modelo com odds como referência

O mercado pode ser usado como referência, mas não como verdade absoluta.

A odd pode entrar como:

* baseline;
* feature;
* comparação;
* filtro de anomalia.

O sistema não deve simplesmente copiar o mercado.

---

## 26.3 Modelos futuros

Após validação:

* Elo;
* regressão logística;
* random forest;
* gradient boosting;
* LightGBM;
* XGBoost;
* ensemble;
* modelos por liga;
* modelos por mercado;
* calibração com isotonic regression;
* calibração com Platt scaling.

---

## 27. Gestão de Banca

Configuração inicial recomendada:

```yaml
initial_bankroll: 1000.00
currency: BRL
max_stake_per_bet_percent: 1.0
max_daily_loss_percent: 3.0
max_open_exposure_percent: 5.0
max_bets_per_day: 10
max_bets_per_match: 1
stop_after_consecutive_losses: 3
min_edge: 0.04
min_expected_value: 0.02
min_confidence: 0.60
```

---

## 28. Regras de Bloqueio

Bloquear entrada simulada quando:

* edge abaixo do mínimo;
* EV negativo;
* confiança baixa;
* odd muito baixa;
* odd muito alta sem histórico;
* liga sem dados suficientes;
* fonte com falha;
* dados desatualizados;
* limite de banca atingido;
* limite diário atingido;
* estratégia em modo de teste;
* custo de análise excedido.

---

## 29. Estrutura de Diretórios

```text
sports-probability-lab/
├── README.md
├── PROJECT_CONSTITUTION.md
├── .env.example
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config/
│   │   │   ├── settings.py
│   │   │   └── logging.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── matches.py
│   │   │   │   ├── odds.py
│   │   │   │   ├── analyses.py
│   │   │   │   ├── decisions.py
│   │   │   │   ├── bankroll.py
│   │   │   │   ├── learning.py
│   │   │   │   └── costs.py
│   │   │   └── dependencies.py
│   │   ├── domain/
│   │   │   ├── matches/
│   │   │   ├── odds/
│   │   │   ├── probabilities/
│   │   │   ├── expected_value/
│   │   │   ├── risk/
│   │   │   ├── simulation/
│   │   │   ├── explanations/
│   │   │   └── learning/
│   │   ├── services/
│   │   │   ├── football_data_service.py
│   │   │   ├── odds_service.py
│   │   │   ├── ai_explanation_service.py
│   │   │   ├── cost_control_service.py
│   │   │   └── report_service.py
│   │   ├── providers/
│   │   │   ├── football/
│   │   │   ├── odds/
│   │   │   └── ai/
│   │   ├── models/
│   │   │   ├── database_models.py
│   │   │   └── schemas.py
│   │   ├── repositories/
│   │   ├── jobs/
│   │   │   ├── collect_matches.py
│   │   │   ├── collect_odds.py
│   │   │   ├── run_pre_match_analysis.py
│   │   │   ├── settle_simulated_bets.py
│   │   │   └── generate_reports.py
│   │   └── utils/
│   ├── tests/
│   ├── migrations/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── styles/
│   └── package.json
├── notebooks/
│   ├── research/
│   ├── model_experiments/
│   └── calibration/
├── docs/
│   ├── architecture.md
│   ├── api_contracts.md
│   ├── data_model.md
│   ├── risk_policy.md
│   ├── ai_cost_policy.md
│   └── roadmap.md
└── scripts/
    ├── seed_database.py
    ├── import_historical_data.py
    └── export_reports.py
```

---

## 30. APIs Internas

## 30.1 Matches

```text
GET /matches/upcoming
GET /matches/{match_id}
GET /matches/{match_id}/analysis
GET /matches/{match_id}/odds
```

---

## 30.2 Odds

```text
POST /odds/collect
GET /odds/snapshots
POST /odds/manual
```

---

## 30.3 Analysis

```text
POST /analysis/pre-match/{match_id}
GET /analysis/pre-match/{match_id}
GET /analysis/signals
```

---

## 30.4 Decisions

```text
GET /decisions
GET /decisions/{decision_id}
POST /decisions/{decision_id}/explain
```

---

## 30.5 Bankroll

```text
GET /bankroll
GET /bankroll/history
GET /bankroll/performance
```

---

## 30.6 Learning

```text
GET /learning/insights
POST /learning/review/{insight_id}
GET /learning/strategy-versions
```

---

## 30.7 Costs

```text
GET /costs/today
GET /costs/month
GET /costs/providers
GET /costs/ai
```

---

## 31. Variáveis de Ambiente

```env
APP_ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/sports_lab
REDIS_URL=redis://localhost:6379

FOOTBALL_API_PROVIDER=api_football
FOOTBALL_API_KEY=replace_me

ODDS_API_PROVIDER=the_odds_api
ODDS_API_KEY=replace_me

OPENAI_API_KEY=replace_me
AI_DAILY_COST_LIMIT=2.00
AI_MONTHLY_COST_LIMIT=30.00

DEFAULT_BANKROLL=1000.00
MAX_STAKE_PER_BET_PERCENT=1.0
MAX_DAILY_LOSS_PERCENT=3.0
MIN_EDGE=0.04
MIN_CONFIDENCE=0.60
```

---

## 32. Roadmap

## Fase 0 — Fundação

Objetivo:

Criar base do projeto.

Entregas:

* repositório;
* estrutura de diretórios;
* Docker Compose;
* FastAPI;
* PostgreSQL;
* frontend inicial;
* documentação;
* `.env.example`;
* modelos iniciais de banco;
* migrations.

Critério de pronto:

* app sobe localmente;
* banco conecta;
* health check funciona.

---

## Fase 1 — Coleta pré-jogo

Objetivo:

Listar jogos e odds.

Entregas:

* integração com API de futebol;
* integração com API de odds;
* normalização de times;
* cadastro de partidas;
* snapshots de odds;
* tela de jogos.

Critério de pronto:

* sistema lista jogos futuros;
* sistema mostra odds;
* sistema armazena snapshots.

---

## Fase 2 — Probabilidade e EV

Objetivo:

Criar motor inicial de análise.

Entregas:

* cálculo de probabilidade implícita;
* modelo Poisson simples;
* cálculo de edge;
* cálculo de EV;
* decisão simulada básica;
* logs de decisão.

Critério de pronto:

* cada jogo tem análise;
* cada mercado tem probabilidade;
* cada decisão tem motivo.

---

## Fase 3 — Banca simulada

Objetivo:

Simular apostas e resultados.

Entregas:

* banca simulada;
* stake;
* liquidação de apostas;
* ROI;
* yield;
* drawdown;
* histórico;
* relatório básico.

Critério de pronto:

* sistema simula entradas;
* sistema liquida após resultado;
* sistema atualiza banca.

---

## Fase 4 — Explicabilidade com IA controlada

Objetivo:

Gerar explicações sem estourar custo.

Entregas:

* explicação curta;
* explicação detalhada;
* cache de explicações;
* logs de custo;
* limites de IA;
* relatório pós-jogo.

Critério de pronto:

* explicações são geradas apenas quando necessário;
* custo é registrado;
* cache funciona.

---

## Fase 5 — Aprendizado

Objetivo:

Identificar padrões de erro.

Entregas:

* análise por mercado;
* análise por liga;
* análise por faixa de odd;
* análise por confiança;
* sugestões versionadas;
* comparação entre estratégias.

Critério de pronto:

* sistema gera insights;
* insights não alteram estratégia automaticamente;
* usuário pode revisar insights.

---

## Fase 6 — Pré-jogo robusto

Objetivo:

Validar pré-jogo antes do live.

Entregas:

* backtest;
* calibração;
* benchmarks;
* métricas de performance;
* dashboard completo;
* relatório semanal;
* critérios de aprovação.

Critério de pronto:

* sistema tem histórico suficiente;
* métricas são confiáveis;
* estratégia é comparada contra benchmarks;
* pré-jogo é considerado estável.

---

## Fase 7 — Ao vivo observacional

Objetivo:

Acompanhar jogos ao vivo sem decisão operacional.

Entregas:

* API live;
* eventos;
* odds live;
* medição de delay;
* saúde das fontes;
* dashboard tempo real;
* logs de divergência.

Critério de pronto:

* sistema acompanha jogos;
* mede delay;
* detecta divergências;
* não toma decisão ainda.

---

## Fase 8 — Ao vivo com decisão simulada

Objetivo:

Simular entradas ao vivo.

Entregas:

* estado do jogo;
* probabilidade ao vivo;
* EV ao vivo;
* risk gate;
* bloqueio por delay;
* bloqueio por mercado suspenso;
* simulação live.

Critério de pronto:

* sistema simula live;
* bloqueia em dados ruins;
* registra tudo.

---

## 33. Testes

## 33.1 Testes unitários

Cobrir:

* cálculo de probabilidade implícita;
* cálculo de margem;
* cálculo de EV;
* cálculo de stake;
* regras de risco;
* liquidação de aposta;
* normalização de odds;
* normalização de times.

---

## 33.2 Testes de integração

Cobrir:

* conexão com banco;
* integração com API de futebol;
* integração com API de odds;
* gravação de snapshots;
* geração de análise;
* geração de decisão.

---

## 33.3 Testes de simulação

Cobrir:

* banca inicial;
* múltiplas apostas;
* vitórias;
* derrotas;
* void;
* sequência de perdas;
* limite diário;
* drawdown;
* bloqueio por risco.

---

## 33.4 Testes de custo

Cobrir:

* chamadas de IA;
* cache;
* limite diário;
* limite mensal;
* logs de custo;
* falha ao exceder limite.

---

## 33.5 Testes de qualidade de dados

Cobrir:

* odds ausente;
* time não normalizado;
* jogo duplicado;
* liga desconhecida;
* mercado inválido;
* odd absurda;
* data incorreta;
* fonte fora do ar.

---

## 34. Critérios Para Considerar Pré-Jogo Estável

O pré-jogo só será considerado estável quando:

* coletar jogos sem erro relevante;
* coletar odds de forma confiável;
* normalizar times corretamente;
* registrar snapshots;
* simular decisões;
* liquidar resultados;
* gerar métricas;
* explicar decisões;
* controlar custos;
* comparar benchmarks;
* ter histórico suficiente;
* não depender de intervenção manual constante.

---

## 35. Critérios Para Iniciar Ao Vivo

O ao vivo só poderá começar quando:

* pré-jogo estiver estável;
* banco estiver robusto;
* dashboard estiver funcional;
* motor de risco estiver implementado;
* simulação estiver validada;
* logs forem auditáveis;
* custo estiver controlado;
* houver API live escolhida;
* houver política de delay definida;
* houver regra de bloqueio por dado ruim.

---

## 36. Critérios Para Considerar Dinheiro Real no Futuro

Dinheiro real está fora do escopo inicial.

Só poderá ser estudado se:

* houver longo período de simulação;
* houver expectativa positiva;
* houver drawdown controlado;
* houver comparação contra benchmarks;
* houver auditoria dos logs;
* houver validação jurídica/termos de uso;
* houver integração autorizada;
* houver confirmação manual;
* houver limite financeiro baixo;
* houver kill switch;
* houver bloqueio contra comportamento compulsivo;
* houver revisão humana.

Mesmo assim, a primeira fase real, se existir, deve ser:

```text
IA sugere → usuário revisa → usuário decide manualmente
```

Nunca começar com execução automática.

---

## 37. Regras Para Codex

O Codex deve seguir este documento como fonte da verdade.

Antes de implementar qualquer funcionalidade, deve verificar:

* isso respeita o escopo atual?
* isso pertence ao pré-jogo ou ao vivo?
* isso viola a regra anti-scraping?
* isso aumenta custo de IA sem necessidade?
* isso é explicável?
* isso registra logs?
* isso respeita gestão de risco?
* isso é testável?
* isso evita complexidade prematura?

---

## 38. Ordem Recomendada de Implementação Para Codex

1. Criar estrutura base do projeto.
2. Criar banco e migrations.
3. Criar entidades principais.
4. Criar API de health check.
5. Criar integração mock de jogos.
6. Criar integração mock de odds.
7. Criar normalização.
8. Criar cálculo de probabilidade implícita.
9. Criar cálculo de EV.
10. Criar simulação de decisão.
11. Criar banca simulada.
12. Criar dashboard simples.
13. Criar logs.
14. Criar integração real com uma API.
15. Criar relatórios.
16. Criar explicação com IA controlada.
17. Criar aprendizado básico.
18. Criar benchmarks.
19. Só depois estudar live.

---

## 39. Decisões Técnicas Já Tomadas

* Esporte inicial: futebol.
* Primeiro modo: pré-jogo.
* Modo ao vivo: fase futura.
* Dinheiro real: bloqueado.
* Apostas reais automáticas: fora do escopo.
* Scraping de casas: proibido.
* Odds: via API, exchange oficial ou entrada manual.
* IA: controlada e explicativa.
* Cálculo principal: estatístico/matemático.
* Banco: PostgreSQL.
* Backend: Python + FastAPI.
* Frontend: React/Next.js.
* Gestão de banca: obrigatória.
* Logs: obrigatórios.
* Aprendizado automático alterando regras: proibido no início.

---

## 40. Decisões Ainda Abertas

Responder antes da implementação avançada:

1. Qual API de futebol será usada primeiro?
2. Qual API de odds será usada primeiro?
3. Qual liga será priorizada?
4. Qual banca simulada inicial?
5. Quais mercados entram no primeiro teste?
6. Qual limite mensal de custo?
7. Qual modelo de IA será usado para explicação?
8. Qual visual desejado para o dashboard?
9. Quais métricas serão exibidas primeiro?
10. Quantos jogos por dia serão analisados?
11. Qual histórico mínimo para considerar uma liga válida?
12. Qual edge mínimo definitivo?
13. Qual confiança mínima definitiva?

---

## 41. Configuração Inicial Recomendada

```yaml
project:
  name: Sports Probability Lab
  sport: football
  initial_mode: pre_match
  live_mode_enabled: false
  real_money_enabled: false

bankroll:
  initial: 1000.00
  currency: BRL
  max_stake_per_bet_percent: 1.0
  max_daily_loss_percent: 3.0
  max_open_exposure_percent: 5.0
  max_bets_per_day: 10
  stop_after_consecutive_losses: 3

markets:
  - over_1_5
  - over_2_5
  - both_teams_to_score_yes
  - full_time_result_1x2

decision_rules:
  min_edge: 0.04
  min_expected_value: 0.02
  min_confidence: 0.60
  allow_martingale: false
  allow_loss_recovery: false

ai:
  enabled: true
  use_for_decision: false
  use_for_explanation: true
  use_for_reports: true
  daily_cost_limit: 2.00
  monthly_cost_limit: 30.00
  cache_enabled: true

data_policy:
  allow_authorized_apis: true
  allow_manual_odds: true
  allow_scraping_bookmakers: false
  allow_antibot_bypass: false
  allow_logged_account_automation: false
```

---

## 42. Exemplo de Decisão Simulada Completa

```json
{
  "decision_id": "decision_001",
  "match": "Time A vs Time B",
  "competition": "Liga Exemplo",
  "market": "Over 2.5",
  "selection": "Over",
  "bookmaker": "Odds Provider",
  "odd": 2.05,
  "captured_at": "2026-06-23T12:00:00-03:00",
  "implied_probability": 0.4878,
  "model_probability": 0.5420,
  "edge": 0.0542,
  "expected_value": 0.1111,
  "confidence": 0.67,
  "risk_level": "MEDIUM",
  "bankroll_before": 1000.00,
  "stake": 10.00,
  "decision": "SIMULATE_ENTRY",
  "short_explanation": "Entrada simulada em Over 2.5 por edge positivo e EV favorável.",
  "detailed_explanation": "O modelo identificou probabilidade estimada de 54,2% para Over 2.5, enquanto a odd atual implica 48,78%. A diferença sugere possível valor. A confiança é média porque os dados históricos são suficientes, mas escalações ainda não foram consideradas.",
  "status": "open"
}
```

---

## 43. Exemplo de Aprendizado Pós-Jogo

```json
{
  "match": "Time A vs Time B",
  "market": "Over 2.5",
  "decision": "SIMULATE_ENTRY",
  "result": "LOST",
  "profit_loss": -10.00,
  "learning": {
    "insight": "O modelo superestimou jogos de Over 2.5 nesta liga quando o visitante tinha baixa produção ofensiva fora de casa.",
    "confidence": 0.58,
    "suggested_action": "Adicionar peso maior para desempenho ofensivo do visitante fora de casa antes de simular Over 2.5."
  }
}
```

---

## 44. Glossário

### Odd

Preço oferecido para um evento.

### Probabilidade implícita

Probabilidade derivada da odd.

### Probabilidade estimada

Probabilidade calculada pelo modelo.

### Edge

Diferença entre probabilidade estimada e probabilidade implícita.

### EV

Valor esperado da decisão.

### Stake

Valor da entrada simulada.

### Yield

Retorno sobre o total apostado.

### ROI

Retorno sobre investimento.

### Drawdown

Queda máxima da banca em relação ao pico.

### Banca simulada

Saldo fictício usado para testes.

### Pré-jogo

Análise feita antes da partida começar.

### Ao vivo

Análise feita durante a partida.

### Fonte de dados

API ou origem de informação.

### Delay

Atraso entre evento real e chegada do dado ao sistema.

### Mercado suspenso

Momento em que odds ficam indisponíveis por evento crítico.

### Caixa-preta

Sistema que decide sem explicar.

---

## 45. Resumo Executivo Final

O Sports Probability Lab será um laboratório de inteligência para futebol, começando obrigatoriamente pelo pré-jogo.

O sistema deverá coletar dados, consultar odds autorizadas, calcular probabilidades, comparar com o mercado, identificar possível valor esperado, simular decisões, registrar resultados, explicar raciocínios, controlar banca, medir custos e aprender com o histórico.

O projeto não deve apostar dinheiro real no início.

O projeto não deve usar scraping ou bypass de casas de aposta.

O projeto deve ser modular, explicável, auditável e evolutivo.

A prioridade é construir um sistema que funcione, seja confiável e ensine algo real sobre probabilidades, odds e risco.

Somente depois de um pré-jogo robusto, validado e mensurado, o projeto poderá evoluir para acompanhamento ao vivo.

A ambição final é criar um sistema complexo, inteligente e transparente, mas seguindo sempre a ordem:

```text
Funciona → Funciona bem → Mede → Aprende → Escala → Evolui
```

---
