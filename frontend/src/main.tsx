import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

type Match = {
  id: string;
  competition: string;
  home_team: string;
  away_team: string;
  commence_time: string;
  status: string;
};

type Recommendation = {
  id: string;
  match_id: string;
  market: string;
  selection: string;
  odd_decimal: number;
  implied_probability: number;
  model_probability: number;
  edge: number;
  expected_value: number;
  confidence: number;
  quality_score: number;
  risk_label: string;
  recommendation_type: string;
  explanation: string;
  simulated_stake: number;
  status: string;
};

type Bankroll = {
  initial_balance: number;
  current_balance: number;
  simulated_exposure: number;
  simulated_profit_loss: number;
  total_recommendations: number;
  won: number;
  lost: number;
  pending: number;
};

type LearningInsight = {
  id: string;
  insight_type: string;
  description: string;
  confidence: number;
};

type CombinedLeg = {
  market: string;
  selection: string;
  individual_odd: number;
  estimated_probability: number;
};

type CombinedResult = {
  id: string;
  match_id: string;
  legs: CombinedLeg[];
  individual_odds: number[];
  offered_combined_odd: number;
  fair_combined_odd_estimate: number;
  estimated_joint_probability: number;
  adjusted_joint_probability: number;
  implied_probability: number;
  edge: number;
  expected_value: number;
  correlation_penalty: number;
  quality_score: number;
  risk_label: string;
  recommendation: string;
  rearrangement_suggestions: { type: string; reason: string; new_estimated_quality_score: number }[];
};

function percent(value: number) {
  return `${(value * 100).toFixed(1)}%`;
}

function brl(value: number) {
  return new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(value);
}

function App() {
  const [matches, setMatches] = useState<Match[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [bankroll, setBankroll] = useState<Bankroll | null>(null);
  const [insights, setInsights] = useState<LearningInsight[]>([]);
  const [combinedResult, setCombinedResult] = useState<CombinedResult | null>(null);
  const [combinedHistory, setCombinedHistory] = useState<CombinedResult[]>([]);
  const [legs, setLegs] = useState<CombinedLeg[]>([
    { market: "corners", selection: "Over 7.5 corners", individual_odd: 1.2, estimated_probability: 0.78 },
    { market: "h2h", selection: "Brazil wins", individual_odd: 1.1, estimated_probability: 0.82 },
    { market: "cards", selection: "Under 5.5 cards", individual_odd: 1.3, estimated_probability: 0.7 },
  ]);
  const [offeredOdd, setOfferedOdd] = useState(2.2);
  const [matchId, setMatchId] = useState("worldcup_mock_001");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadDashboard() {
    try {
      setError(null);
      const [matchesResponse, recommendationsResponse, bankrollResponse, insightsResponse, combinedHistoryResponse] = await Promise.all([
        fetch(`${API_URL}/matches/world-cup`),
        fetch(`${API_URL}/recommendations`),
        fetch(`${API_URL}/bankroll`),
        fetch(`${API_URL}/learning/insights`),
        fetch(`${API_URL}/bet-builder/history`),
      ]);
      if (!matchesResponse.ok || !recommendationsResponse.ok || !bankrollResponse.ok || !insightsResponse.ok || !combinedHistoryResponse.ok) {
        throw new Error("Falha ao carregar dados do backend.");
      }
      setMatches(await matchesResponse.json());
      setRecommendations(await recommendationsResponse.json());
      setBankroll(await bankrollResponse.json());
      setInsights(await insightsResponse.json());
      setCombinedHistory(await combinedHistoryResponse.json());
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Erro desconhecido.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadDashboard();
  }, []);

  async function runMock() {
    const response = await fetch(`${API_URL}/recommendations/run-mock`, { method: "POST" });
    setRecommendations(await response.json());
    await loadDashboard();
  }

  async function evaluateCombined() {
    const response = await fetch(`${API_URL}/bet-builder/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ match_id: matchId, offered_combined_odd: offeredOdd, legs }),
    });
    setCombinedResult(await response.json());
    await loadDashboard();
  }

  const history = useMemo(() => recommendations.slice(0, 8), [recommendations]);

  if (loading) return <main className="shell">Carregando Robet...</main>;

  return (
    <main className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Laboratório probabilístico</p>
          <h1>Robet</h1>
        </div>
        <button onClick={runMock}>Rodar análise mockada</button>
      </header>

      {error && <p className="error">{error}</p>}

      <section className="metrics">
        <Metric label="Banca simulada" value={bankroll ? brl(bankroll.current_balance) : "-"} />
        <Metric label="Exposição simulada" value={bankroll ? brl(bankroll.simulated_exposure) : "-"} />
        <Metric label="Recomendações" value={String(bankroll?.total_recommendations ?? 0)} />
        <Metric label="Pendentes" value={String(bankroll?.pending ?? 0)} />
      </section>

      <section className="grid two">
        <Panel title="Jogos da Copa">
          <div className="list">
            {matches.map((match) => (
              <article className="row" key={match.id}>
                <div>
                  <strong>{match.home_team} x {match.away_team}</strong>
                  <span>{new Date(match.commence_time).toLocaleString("pt-BR")} · {match.status}</span>
                </div>
                <button onClick={() => setMatchId(match.id)}>Usar</button>
              </article>
            ))}
          </div>
        </Panel>

        <Panel title="Recomendações ranqueadas">
          <div className="list">
            {recommendations.slice(0, 6).map((item) => (
              <article className="row recommendation" key={item.id}>
                <div>
                  <strong>{item.selection}</strong>
                  <span>{item.market} · odd {item.odd_decimal.toFixed(2)} · EV {brl(item.expected_value)}</span>
                </div>
                <Badge tone={item.recommendation_type === "GOOD_OPPORTUNITY" ? "good" : item.recommendation_type === "AVOID" ? "bad" : "watch"}>
                  {item.quality_score}
                </Badge>
              </article>
            ))}
          </div>
        </Panel>
      </section>

      <section className="grid two">
        <Panel title="Avaliador de combinadas">
          <div className="form">
            <label>
              Jogo
              <select id="combined-match" name="combined_match" value={matchId} onChange={(event) => setMatchId(event.target.value)}>
                {matches.map((match) => <option key={match.id} value={match.id}>{match.home_team} x {match.away_team}</option>)}
              </select>
            </label>
            <label>
              Odd combinada oferecida
              <input id="offered-odd" name="offered_combined_odd" type="number" step="0.01" value={offeredOdd} onChange={(event) => setOfferedOdd(Number(event.target.value))} />
            </label>
            {legs.map((leg, index) => (
              <div className="leg" key={`${leg.market}-${index}`}>
                <input id={`leg-${index}-market`} name={`leg_${index}_market`} aria-label={`Mercado da perna ${index + 1}`} value={leg.market} onChange={(event) => updateLeg(index, "market", event.target.value)} />
                <input id={`leg-${index}-selection`} name={`leg_${index}_selection`} aria-label={`Seleção da perna ${index + 1}`} value={leg.selection} onChange={(event) => updateLeg(index, "selection", event.target.value)} />
                <input id={`leg-${index}-odd`} name={`leg_${index}_odd`} aria-label={`Odd da perna ${index + 1}`} type="number" step="0.01" value={leg.individual_odd} onChange={(event) => updateLeg(index, "individual_odd", Number(event.target.value))} />
                <input id={`leg-${index}-probability`} name={`leg_${index}_probability`} aria-label={`Probabilidade da perna ${index + 1}`} type="number" step="0.01" value={leg.estimated_probability} onChange={(event) => updateLeg(index, "estimated_probability", Number(event.target.value))} />
                <button onClick={() => setLegs(legs.filter((_, legIndex) => legIndex !== index))}>Remover</button>
              </div>
            ))}
            <div className="actions">
              <button onClick={() => setLegs([...legs, { market: "manual", selection: "Nova perna", individual_odd: 1.5, estimated_probability: 0.6 }])}>Adicionar perna</button>
              <button onClick={evaluateCombined}>Avaliar combinada</button>
            </div>
          </div>
        </Panel>

        <Panel title="Sugestões de rearranjo">
          {combinedResult ? (
            <div className="combined">
              <div className="scoreline">
                <Badge tone={combinedResult.recommendation === "GOOD_OPPORTUNITY" ? "good" : combinedResult.recommendation === "AVOID" ? "bad" : "watch"}>
                  Score {combinedResult.quality_score}
                </Badge>
                <span>Risco {combinedResult.risk_label}</span>
              </div>
              <p>Probabilidade ajustada: {percent(combinedResult.adjusted_joint_probability)} · Odd justa: {combinedResult.fair_combined_odd_estimate.toFixed(2)}</p>
              <p>Edge: {percent(combinedResult.edge)} · EV: {brl(combinedResult.expected_value)} · Penalidade: {percent(combinedResult.correlation_penalty)}</p>
              <div className="list">
                {combinedResult.rearrangement_suggestions.map((suggestion) => (
                  <article className="row" key={suggestion.type}>
                    <div>
                      <strong>{suggestion.type}</strong>
                      <span>{suggestion.reason}</span>
                    </div>
                    <Badge tone="watch">{suggestion.new_estimated_quality_score}</Badge>
                  </article>
                ))}
              </div>
            </div>
          ) : (
            <p className="muted">Envie uma combinada manual para ver a avaliação e os rearranjos.</p>
          )}
          {combinedHistory.length > 0 && (
            <div className="history-block">
              <h3>Combinadas persistidas</h3>
              <div className="list">
                {combinedHistory.slice(0, 3).map((item, index) => (
                  <article className="row" key={`${item.quality_score}-${index}`}>
                    <div>
                      <strong>Odd {item.offered_combined_odd.toFixed(2)} · score {item.quality_score}</strong>
                      <span>{item.legs.length} pernas · EV {brl(item.expected_value)} · risco {item.risk_label}</span>
                    </div>
                    <Badge tone={item.recommendation === "GOOD_OPPORTUNITY" ? "good" : item.recommendation === "AVOID" ? "bad" : "watch"}>
                      {item.recommendation}
                    </Badge>
                  </article>
                ))}
              </div>
            </div>
          )}
        </Panel>
      </section>

      <section className="grid two">
        <Panel title="Histórico de recomendações">
          <table>
            <thead><tr><th>Seleção</th><th>Edge</th><th>Confiança</th><th>Status</th></tr></thead>
            <tbody>
              {history.map((item) => (
                <tr key={item.id}>
                  <td>{item.selection}</td>
                  <td>{percent(item.edge)}</td>
                  <td>{percent(item.confidence)}</td>
                  <td>{item.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>

        <Panel title="Aprendizados">
          <div className="list">
            {insights.map((insight) => (
              <article className="row" key={insight.id}>
                <div>
                  <strong>{insight.insight_type}</strong>
                  <span>{insight.description}</span>
                </div>
                <Badge tone="watch">{percent(insight.confidence)}</Badge>
              </article>
            ))}
          </div>
        </Panel>
      </section>
    </main>
  );

  function updateLeg<Key extends keyof CombinedLeg>(index: number, key: Key, value: CombinedLeg[Key]) {
    setLegs(legs.map((leg, legIndex) => (legIndex === index ? { ...leg, [key]: value } : leg)));
  }
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <article className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="panel">
      <h2>{title}</h2>
      {children}
    </section>
  );
}

function Badge({ children, tone }: { children: React.ReactNode; tone: "good" | "watch" | "bad" }) {
  return <span className={`badge ${tone}`}>{children}</span>;
}

createRoot(document.getElementById("root")!).render(<App />);
