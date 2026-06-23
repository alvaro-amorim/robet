# PROJECT_CONSTITUTION.md

# Robet — Constituição Técnica e de Produto

## 1. Identidade do Projeto

**Nome do app:** Robet  
**Descrição curta:** Laboratório inteligente de análise probabilística para futebol.  
**Esporte inicial:** Futebol.  
**Competição inicial:** Copa do Mundo.  
**Competição secundária futura:** Brasileirão Série A.  
**Modo inicial:** Pré-jogo.  
**Modo futuro:** Ao vivo, somente depois do pré-jogo estar validado.  
**Operação real:** Fora do escopo inicial.  
**Aposta automática:** Proibida no MVP.  
**Tipo de produto:** Recomendador, simulador, avaliador e sistema de aprendizado.

O Robet não nasce como um bot que aposta sozinho. Ele nasce como um sistema que analisa jogos, identifica possíveis oportunidades, recomenda apostas simuladas, avalia apostas informadas manualmente, confere depois se teria acertado ou errado e usa esse histórico para melhorar sua lógica.

---

## 2. Missão

Criar um sistema robusto para analisar futebol com foco em probabilidade, valor esperado, simulação e aprendizado.

O sistema deve responder, para cada jogo:

- O que está sendo analisado?
- Quais dados sustentam a análise?
- Quais mercados parecem interessantes?
- Qual é a probabilidade estimada?
- Qual é a probabilidade implícita das odds?
- Existe possível valor esperado positivo?
- Qual é o grau de confiança?
- Qual é o risco?
- A recomendação é boa, ruim ou incerta?
- O que aconteceu depois?
- A recomendação acertou ou errou?
- O que o sistema aprendeu?

O objetivo não é prever resultados com certeza. O objetivo é construir um laboratório que aprenda a avaliar oportunidades com base em dados.

---

## 3. Definição Correta do Robet

O Robet deve ser entendido como:

```text
analista probabilístico + simulador + avaliador de apostas + memória de aprendizado
```

Ele não deve ser entendido como:

```text
robô de aposta automática + scraper de casa de aposta + promessa de lucro
```

---

## 4. Filosofia do Projeto

O Robet deve pensar em termos de:

- cenários;
- probabilidades;
- odds;
- valor esperado;
- risco;
- confiança;
- histórico;
- aprendizado;
- incerteza.

Ele nunca deve tratar uma previsão como certeza.

A frase correta não é:

> “Esse jogo vai ter mais de 2.5 gols.”

A frase correta é:

> “Com os dados disponíveis, o modelo estima uma probabilidade maior do que a probabilidade implícita da odd. A oportunidade parece positiva, mas a confiança é moderada e deve ser tratada como simulação.”

---

## 5. Regra Absoluta de Evolução

O desenvolvimento deve seguir esta ordem:

```text
1. Funciona com dados mockados
2. Funciona com dados reais pré-jogo
3. Mede e registra tudo
4. Recomenda e simula
5. Confere acertos e erros
6. Aprende com histórico
7. Melhora a lógica
8. Só depois pensa em ao vivo
9. Só muito depois considera uso real/manual
```

Nenhuma fase futura pode atropelar a validação da fase atual.

---

## 6. Escopo Atual do MVP

O MVP inicial será focado em **Copa do Mundo pré-jogo**.

O sistema deve:

- listar jogos da Copa do Mundo;
- analisar todos os jogos disponíveis;
- gerar recomendações ranqueadas por jogo;
- avaliar mercados simples;
- avaliar apostas combinadas informadas manualmente;
- sugerir rearranjos de combinadas para melhorar chance/risco;
- simular recomendações;
- registrar resultados;
- classificar acerto/erro;
- gerar aprendizados estruturados;
- exibir tudo em dashboard;
- funcionar primeiro com dados mockados;
- depois integrar APIs reais.

---

## 7. Fora do Escopo Atual

Não implementar no MVP:

- aposta real;
- execução automática;
- login em casa de aposta;
- scraping de casa de aposta;
- bypass de anti-bot;
- bypass de CAPTCHA;
- tentativa de simular usuário humano;
- modo ao vivo;
- integração com conta de aposta;
- uso de IA para decidir recomendações;
- reinforcement learning;
- alteração automática de estratégia sem revisão;
- múltiplos esportes.

---

## 8. Regra Anti-Scraping e Anti-Bot

O Robet não deve depender de capturar odds diretamente de sites de casas de aposta com conta logada, proteção anti-bot ou restrições de automação.

Fontes permitidas:

- APIs oficiais;
- APIs agregadoras de odds;
- APIs esportivas;
- exchanges com API oficial, em fase futura;
- entrada manual de odds;
- arquivos importados pelo usuário;
- dados públicos dentro dos termos permitidos.

Fontes proibidas:

- scraping de casas de aposta protegidas;
- automação de login;
- contorno de CAPTCHA;
- contorno de fingerprint;
- engenharia reversa de API privada;
- Playwright/Selenium para enganar site de aposta;
- qualquer técnica cujo objetivo seja burlar bloqueio.

---

## 9. Papel da IA no Projeto

A IA generativa não é o cérebro decisor do Robet.

A lógica principal deve ser baseada em:

- estatística;
- probabilidade;
- regras;
- valor esperado;
- histórico;
- tentativa e erro;
- simulação;
- aprendizado estruturado.

A IA pode ser usada apenas para:

- resumir aprendizados;
- compactar contexto histórico;
- gerar relatórios textuais;
- organizar insights;
- explicar em linguagem natural resultados já calculados;
- apoiar auditoria manual.

A IA não deve:

- escolher aposta sozinha;
- substituir cálculo estatístico;
- rodar em toda análise;
- rodar em toda mudança de odd;
- alterar pesos automaticamente;
- ser requisito para o app funcionar.

O Robet deve funcionar mesmo com `AI_ENABLED=false`.

---

## 10. Modo Inicial: Copa do Mundo Pré-Jogo

A competição inicial será a Copa do Mundo porque há jogos frequentes e grande interesse de análise.

O sistema deve tentar descobrir automaticamente os identificadores da competição nas APIs, usando termos como:

```text
world cup
fifa world cup
copa do mundo
```

Se a API de odds não retornar diretamente a Copa do Mundo, o sistema deve:

1. continuar usando a API de futebol para listar jogos;
2. permitir odds manuais;
3. registrar que a fonte de odds foi manual;
4. ainda assim calcular probabilidade implícita, EV, risco e recomendação.

---

## 11. Mercados Simples

O MVP deve começar com mercados simples, quando existirem nas APIs ou forem informados manualmente.

Mercados iniciais:

- vencedor do jogo / 1X2;
- empate;
- over/under gols;
- ambas marcam;
- total de escanteios;
- total de cartões;
- time vence;
- time não perde;
- mercado manual genérico.

O sistema deve tratar cada mercado como uma entidade avaliável, mesmo quando a fonte for manual.

---

## 12. Apostas Combinadas / Bet Builder

O Robet deve ter desde o MVP um avaliador de apostas combinadas manuais.

Exemplo de aposta combinada:

```text
Brasil vence
+ mais de 7 escanteios
+ menos de 5 cartões
```

Com odds individuais:

```text
1.20 / 1.10 / 1.30
```

E odd combinada oferecida:

```text
2.20
```

O sistema deve avaliar:

- pernas da aposta;
- odds individuais;
- odd combinada informada;
- probabilidade implícita de cada perna;
- probabilidade estimada de cada perna;
- probabilidade conjunta aproximada;
- risco de correlação;
- penalidade conservadora por incerteza;
- valor esperado aproximado;
- score de qualidade;
- recomendação final;
- possíveis rearranjos.

---

## 13. Rearranjo de Combinadas

Quando o usuário inserir uma combinada, o Robet deve poder sugerir rearranjos.

Exemplos:

- remover uma perna muito arriscada;
- trocar linha agressiva por linha conservadora;
- separar uma combinada em duas apostas simples simuladas;
- reduzir número de pernas;
- indicar que a odd maior não compensa a queda de probabilidade;
- indicar que a combinada está muito correlacionada;
- indicar que falta dado para avaliar com confiança.

A resposta deve ser explicável:

```text
A perna “menos de 5 cartões” reduz muito a confiança porque o sistema ainda não possui dados suficientes sobre árbitro, estilo das seleções e contexto disciplinar. Uma versão mais segura seria manter apenas Brasil vence + over escanteios, ou transformar cartões em observação sem simular entrada.
```

---

## 14. Correlação em Combinadas

O sistema não deve assumir automaticamente que as pernas de uma combinada são independentes.

Eventos do mesmo jogo podem ser correlacionados.

Exemplos:

- time favorito vencer pode estar relacionado a mais escanteios;
- jogo nervoso pode aumentar cartões e alterar ritmo;
- gol cedo pode mudar volume ofensivo;
- domínio territorial pode aumentar escanteios e chance de vitória;
- expulsão pode invalidar leituras anteriores.

No MVP, o Robet usará uma penalidade conservadora por correlação e incerteza.

Modelo inicial:

```text
probabilidade_conjunta_aproximada = produto_das_probabilidades_estimadas
probabilidade_ajustada = probabilidade_conjunta_aproximada * (1 - penalidade_de_correlação)
```

A penalidade inicial pode ser configurada, por exemplo:

```text
15%
```

Futuramente, a penalidade deve ser aprendida com histórico real de acertos e erros.

---

## 15. Recomendações por Jogo

O Robet deve gerar recomendações ranqueadas por jogo.

Não haverá limite rígido inicial de recomendações porque o app não aposta dinheiro real.

Mesmo assim, o sistema deve classificar por qualidade, para evitar poluição visual.

Categorias sugeridas:

```text
FORTE
BOA
MODERADA
INCERTA
RUIM
BLOQUEADA
```

Cada recomendação deve conter:

- jogo;
- mercado;
- seleção;
- odd;
- probabilidade implícita;
- probabilidade estimada;
- edge;
- valor esperado;
- confiança;
- risco;
- motivo;
- status da simulação;
- resultado posterior;
- aprendizado.

---

## 16. Simulação de Banca

A banca simulada inicial será:

```text
R$ 1.000,00
```

Stake máxima inicial:

```text
1% da banca simulada por recomendação
```

Como o app não aposta dinheiro real, não haverá bloqueio rígido de perda diária no começo.

Mas o sistema deve continuar registrando:

- perda diária simulada;
- lucro diário simulado;
- drawdown;
- exposição;
- sequência de erros;
- mercados que mais erram;
- mercados que mais acertam;
- impacto de combinadas.

Mesmo em simulação, o Robet não deve usar martingale nem lógica de recuperação de prejuízo.

---

## 17. Métricas Principais

Métricas obrigatórias:

- total de jogos analisados;
- total de recomendações geradas;
- recomendações por jogo;
- taxa de acerto;
- ROI simulado;
- yield simulado;
- lucro/prejuízo simulado;
- drawdown;
- acerto por mercado;
- erro por mercado;
- acerto por competição;
- performance de apostas simples;
- performance de combinadas;
- performance por faixa de odd;
- performance por nível de confiança;
- performance por score de qualidade;
- EV médio;
- edge médio.

---

## 18. Aprendizado

O aprendizado inicial será estruturado, não autônomo.

O Robet deve registrar:

- recomendações boas que deram certo;
- recomendações boas que deram errado;
- recomendações ruins que o sistema bloqueou;
- combinadas que falharam por uma perna;
- mercados com baixa previsibilidade;
- mercados superestimados;
- padrões por seleção;
- padrões por tipo de jogo;
- padrões por odd;
- padrões por confiança.

O sistema pode sugerir ajustes, mas não deve alterar automaticamente sua própria estratégia no MVP.

---

## 19. Compactação de Aprendizado com IA

A IA pode ser usada para transformar logs extensos em aprendizados compactos.

Exemplo:

```text
Nos últimos 12 jogos, o modelo teve desempenho ruim em combinadas com cartões. A principal causa foi baixa qualidade dos dados disciplinares. Recomenda-se reduzir confiança automática em mercados de cartões até que dados de árbitro sejam adicionados.
```

Esse resumo pode ser salvo como insight, mas não pode alterar regras sozinho.

---

## 20. Fontes de Dados

### 20.1 API de futebol

Uso:

- jogos da Copa;
- seleções;
- calendário;
- resultados;
- placares;
- estatísticas quando disponíveis;
- eventos futuros;
- conferência de acertos e erros.

Provedor inicial recomendado:

```text
API-Football / API-Sports
```

### 20.2 API de odds

Uso:

- odds pré-jogo;
- mercados disponíveis;
- comparação de odds;
- cálculo de probabilidade implícita.

Provedor inicial recomendado:

```text
The Odds API
```

### 20.3 Entrada manual

Uso:

- odds que a API não possui;
- apostas combinadas;
- mercados de escanteios;
- mercados de cartões;
- mercados específicos de casas;
- avaliação de uma aposta que o usuário viu manualmente.

A entrada manual é parte central do MVP.

---

## 21. Stack Técnica

### Backend

```text
Python + FastAPI
```

### Banco

```text
PostgreSQL
```

### Frontend

```text
Next.js ou React
```

### Cache opcional

```text
Redis
```

No primeiro ciclo, Redis deve ser opcional e pode ficar desligado.

### IA

```text
OpenAI API ou outro provedor compatível
```

IA deve ser opcional.

---

## 22. Arquitetura Geral

```text
[Football Data Provider]
        ↓
[Odds Provider]
        ↓
[Manual Odds / Bet Builder Input]
        ↓
[Data Normalization]
        ↓
[Match Analysis Engine]
        ↓
[Probability Engine]
        ↓
[Expected Value Engine]
        ↓
[Recommendation Engine]
        ↓
[Combined Bet Evaluator]
        ↓
[Simulation Engine]
        ↓
[Result Checker]
        ↓
[Learning Engine]
        ↓
[Dashboard]
```

---

## 23. Módulos Obrigatórios

### 23.1 Match Collector

Coleta jogos da Copa.

### 23.2 Odds Collector

Coleta odds quando disponíveis.

### 23.3 Manual Odds Module

Permite cadastrar odds manualmente.

### 23.4 Probability Engine

Calcula probabilidades estimadas.

### 23.5 Implied Probability Engine

Calcula probabilidade implícita:

```text
probabilidade_implicita = 1 / odd
```

### 23.6 Expected Value Engine

Calcula valor esperado.

### 23.7 Recommendation Engine

Ranqueia oportunidades.

### 23.8 Bet Builder Evaluator

Avalia combinadas.

### 23.9 Rearrangement Engine

Sugere mudanças em combinadas.

### 23.10 Simulation Engine

Simula recomendações.

### 23.11 Result Checker

Confere acertos e erros após os jogos.

### 23.12 Learning Engine

Gera aprendizados estruturados.

### 23.13 AI Summary Engine

Resume aprendizados, quando ativado.

---

## 24. Fluxo do MVP Mockado

O primeiro ciclo do Codex deve funcionar sem chaves reais.

Fluxo obrigatório:

```text
1. Carregar jogos mockados da Copa
2. Carregar odds mockadas
3. Gerar probabilidades estimadas mockadas/regras simples
4. Calcular probabilidade implícita
5. Calcular edge
6. Calcular EV
7. Gerar recomendações ranqueadas
8. Permitir avaliar uma combinada manual
9. Sugerir rearranjos
10. Simular recomendações
11. Registrar resultado mockado
12. Gerar aprendizado básico
13. Exibir no dashboard
```

---

## 25. Fluxo com APIs Reais

Depois do mock funcionar:

```text
1. Conectar API-Football
2. Descobrir competição Copa do Mundo
3. Listar jogos reais
4. Conectar The Odds API
5. Descobrir sport keys disponíveis
6. Buscar odds pré-jogo disponíveis
7. Permitir odds manuais onde a API não cobrir
8. Rodar análise
9. Simular recomendações
10. Conferir resultados reais
```

---

## 26. Dados Obrigatórios de uma Recomendação

```json
{
  "match_id": "string",
  "competition": "World Cup",
  "market": "over_2_5",
  "selection": "over",
  "source": "api_or_manual",
  "odd": 2.1,
  "implied_probability": 0.4762,
  "estimated_probability": 0.54,
  "edge": 0.0638,
  "expected_value": 0.134,
  "confidence": 0.67,
  "risk_level": "medium",
  "quality_label": "boa",
  "recommendation": "simulate",
  "explanation": "texto curto e claro"
}
```

---

## 27. Dados Obrigatórios de uma Combinada

```json
{
  "match_id": "string",
  "combined_odd": 2.2,
  "legs": [
    {
      "market": "team_to_win",
      "selection": "Team A",
      "individual_odd": 1.2,
      "estimated_probability": 0.78
    },
    {
      "market": "corners_over",
      "selection": "over_7_corners",
      "individual_odd": 1.1,
      "estimated_probability": 0.74
    },
    {
      "market": "cards_under",
      "selection": "under_5_cards",
      "individual_odd": 1.3,
      "estimated_probability": 0.62
    }
  ],
  "correlation_penalty": 0.15,
  "adjusted_probability": 0.304,
  "implied_probability": 0.4545,
  "expected_value": -0.331,
  "quality_label": "ruim",
  "suggested_rearrangements": []
}
```

---

## 28. Banco de Dados — Entidades Iniciais

Entidades iniciais:

- providers;
- competitions;
- teams;
- matches;
- odds_snapshots;
- manual_odds;
- recommendations;
- recommendation_results;
- combined_bets;
- combined_bet_legs;
- simulations;
- bankroll_snapshots;
- learning_insights;
- ai_summaries;
- api_usage_logs.

O banco deve priorizar rastreabilidade.

---

## 29. Endpoints Mínimos

```text
GET /health
GET /matches
GET /matches/world-cup
GET /recommendations
POST /recommendations/run-mock
POST /recommendations/run
POST /bet-builder/evaluate
POST /bet-builder/rearrange
GET /bankroll
GET /learning/insights
GET /settings
```

---

## 30. Dashboard Inicial

A interface deve ser em português.

O código pode ser em inglês.

Telas mínimas:

### 30.1 Jogos da Copa

- lista de jogos;
- horário;
- seleções;
- status;
- botão analisar.

### 30.2 Recomendações

- todas as recomendações ranqueadas;
- filtros por jogo;
- filtros por mercado;
- score de qualidade;
- probabilidade;
- odd;
- EV;
- confiança.

### 30.3 Avaliador de Combinadas

- formulário manual;
- adicionar/remover pernas;
- odd individual;
- odd combinada;
- análise final;
- sugestões de rearranjo.

### 30.4 Simulação

- banca simulada;
- recomendações simuladas;
- resultado;
- lucro/prejuízo simulado.

### 30.5 Aprendizado

- acertos;
- erros;
- padrões;
- insights;
- resumos de IA quando ativados.

---

## 31. Configuração Inicial do Produto

```yaml
app:
  name: Robet
  language: pt-BR
  initial_competition: world_cup
  future_competition: brazil_serie_a
  mode: pre_match
  live_enabled: false
  real_money_enabled: false
  auto_betting_enabled: false

simulation:
  bankroll: 1000.00
  currency: BRL
  max_stake_percent: 1.0
  hard_daily_loss_limit_enabled: false

recommendations:
  mode: ranked_all
  require_positive_ev: true
  min_edge: 0.04
  min_confidence: 0.60

combined_bets:
  enabled: true
  manual_input: true
  max_legs: 6
  correlation_mode: conservative_penalty
  default_correlation_penalty: 0.15

ai:
  enabled: false_by_default_possible
  use_for_decision: false
  use_for_recommendation: false
  use_for_learning_summary: true
```

---

## 32. Testes Obrigatórios

Testes unitários:

- probabilidade implícita;
- odd combinada;
- EV;
- edge;
- classificação de qualidade;
- penalidade de correlação;
- stake simulada;
- avaliação de combinadas;
- sugestão de rearranjo;
- registro de resultado;
- geração de insight.

Testes de integração:

- fluxo mockado completo;
- criação de recomendação;
- avaliação de combinada;
- persistência;
- dashboard consumindo API.

---

## 33. Critério de Pronto do Primeiro Ciclo

O primeiro ciclo só estará pronto quando:

- o projeto rodar localmente;
- o backend subir;
- o frontend subir;
- o banco subir;
- o dashboard abrir;
- jogos mockados da Copa aparecerem;
- recomendações mockadas forem geradas;
- uma combinada manual puder ser avaliada;
- o sistema sugerir rearranjo;
- uma simulação puder ser registrada;
- um resultado puder ser conferido;
- um insight simples for gerado;
- todos os testes básicos passarem.

---

## 34. Critério Para Ativar APIs Reais

Só ativar APIs reais depois que:

- o fluxo mockado estiver funcionando;
- `.env` estiver preenchido;
- `.env` estiver fora do Git;
- cache básico existir;
- logs de chamadas existirem;
- sistema lidar com erro de API;
- sistema lidar com ausência de odds;
- entrada manual continuar funcionando.

---

## 35. Critério Para Iniciar Ao Vivo

O modo ao vivo só poderá ser planejado depois que:

- Copa pré-jogo estiver funcional;
- recomendações forem registradas;
- resultados forem conferidos;
- aprendizado estiver funcionando;
- houver histórico suficiente;
- o custo de API estiver controlado;
- o sistema já souber lidar com divergência de dados;
- a arquitetura estiver pronta para eventos.

---

## 36. Instruções Para Codex

O Codex deve obedecer este documento.

Primeira tarefa do Codex:

```text
Criar o projeto localmente com fluxo mockado completo para Copa do Mundo pré-jogo, recomendações ranqueadas, avaliador de combinadas, simulação e aprendizado básico.
```

O Codex não deve:

- conectar API real antes do mock;
- implementar aposta real;
- implementar scraping;
- implementar modo ao vivo;
- usar IA como decisora;
- criar complexidade desnecessária.

---

## 37. Prompt Base Para Codex

```text
Você está desenvolvendo localmente o projeto Robet.

Leia PROJECT_CONSTITUTION.md antes de programar.

Objetivo do primeiro ciclo:
Criar um MVP local com backend FastAPI, frontend em português, banco PostgreSQL via Docker, providers mockados da Copa do Mundo, recomendações ranqueadas, avaliador de combinadas manuais, simulação de banca e aprendizado básico.

Regras:
- Não implementar aposta real.
- Não implementar scraping.
- Não implementar automação em casas.
- Não implementar live betting ainda.
- Não usar IA para decidir.
- O app deve funcionar com USE_MOCK_PROVIDERS=true.
- A interface deve ser em português.
- O código pode ser em inglês.
- O .env real nunca deve ser commitado.
```

---

## 38. Resumo Final

O Robet será um sistema de análise de futebol que começa pela Copa do Mundo, com foco em pré-jogo, recomendações ranqueadas, simulação, avaliação de apostas simples e combinadas, conferência de resultados e aprendizado.

Ele não aposta sozinho.

Ele não acessa casas de aposta de forma automatizada.

Ele não depende de IA para funcionar.

Ele usa IA somente para resumir e compactar aprendizados, quando isso fizer sentido.

A prioridade é construir uma base robusta, explicável e testável antes de qualquer evolução para dados reais, Brasileirão Série A ou modo ao vivo.
