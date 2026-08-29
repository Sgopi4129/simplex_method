"use client";

import { useState } from "react";

type Result = { solution: number[]; maximum: number };
type InputValue = number | "";
type Relation = "<=" | ">=" | "=";
const initialObjective: InputValue[] = [""];
const initialConstraints: InputValue[][] = [[""]];
const initialLimits: InputValue[] = [""];
const backendUrl = process.env.NEXT_PUBLIC_API_URL || "";

function formatNumber(value: number) {
  return Number.isInteger(value) ? String(value) : value.toFixed(4).replace(/0+$/, "").replace(/\.$/, "");
}

function combinations<T>(items: T[], size: number): T[][] {
  if (size === 0) return [[]];
  if (size > items.length) return [];
  return items.flatMap((item, index) => combinations(items.slice(index + 1), size - 1).map((rest) => [item, ...rest]));
}

function solveModel(objective: number[], constraints: number[][], limits: number[], relations: Relation[], sense: "max" | "min"): Result {
  const variableCount = objective.length;
  const inequalities: Array<[number[], number]> = [];
  const equalities: Array<[number[], number]> = [];
  constraints.forEach((coefficients, index) => {
    if (relations[index] === "=") equalities.push([coefficients, limits[index]]);
    else if (relations[index] === "<=") inequalities.push([coefficients, limits[index]]);
    else inequalities.push([coefficients.map((value) => -value), -limits[index]]);
  });
  for (let index = 0; index < variableCount; index += 1) {
    const boundary = Array(variableCount).fill(0);
    boundary[index] = -1;
    inequalities.push([boundary, 0]);
  }
  const solveSystem = (rows: number[][], values: number[]) => {
    if (rows.length !== variableCount) return null;
    const matrix = rows.map((row, index) => [...row, values[index]]);
    for (let column = 0; column < variableCount; column += 1) {
      let pivot = column;
      for (let row = column + 1; row < variableCount; row += 1) if (Math.abs(matrix[row][column]) > Math.abs(matrix[pivot][column])) pivot = row;
      if (Math.abs(matrix[pivot][column]) < 1e-9) return null;
      [matrix[column], matrix[pivot]] = [matrix[pivot], matrix[column]];
      const divisor = matrix[column][column];
      matrix[column] = matrix[column].map((value) => value / divisor);
      for (let row = 0; row < variableCount; row += 1) if (row !== column) {
        const factor = matrix[row][column];
        matrix[row] = matrix[row].map((value, item) => value - factor * matrix[column][item]);
      }
    }
    return matrix.map((row) => row[variableCount]);
  };
  const feasible = (point: number[]) => inequalities.every(([row, limit]) => row.reduce((sum, value, index) => sum + value * point[index], 0) <= limit + 1e-9) && equalities.every(([row, limit]) => Math.abs(row.reduce((sum, value, index) => sum + value * point[index], 0) - limit) <= 1e-9) && point.every((value) => value >= -1e-9);
  const candidates: number[][] = [];
  const origin = Array(variableCount).fill(0);
  if (feasible(origin)) candidates.push(origin);
  combinations(inequalities, variableCount - equalities.length).forEach((active) => {
    const point = solveSystem([...equalities.map(([row]) => row), ...active.map(([row]) => row)], [...equalities.map(([, limit]) => limit), ...active.map(([, limit]) => limit)]);
    if (point && feasible(point)) candidates.push(point);
  });
  if (!candidates.length) throw new Error("The linear program has no feasible solution.");
  const values = candidates.map((point) => objective.reduce((sum, coefficient, index) => sum + coefficient * point[index], 0));
  const best = (sense === "max" ? Math.max : Math.min)(...values);
  return { solution: candidates[values.indexOf(best)], maximum: best };
}

export default function Home() {
  const [objective, setObjective] = useState(initialObjective);
  const [constraints, setConstraints] = useState(initialConstraints);
  const [limits, setLimits] = useState(initialLimits);
  const [sense, setSense] = useState<"max" | "min">("max");
  const [relations, setRelations] = useState<Relation[]>(["<="]);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const parseInput = (value: string): InputValue => value === "" ? "" : Number(value);
  const updateObjective = (index: number, value: string) => setObjective((current) => current.map((item, itemIndex) => itemIndex === index ? parseInput(value) : item));
  const updateConstraint = (rowIndex: number, columnIndex: number, value: string) => setConstraints((current) => current.map((row, currentRow) => currentRow === rowIndex ? row.map((item, currentColumn) => currentColumn === columnIndex ? parseInput(value) : item) : row));
  const addVariable = () => { setObjective((current) => [...current, 0]); setConstraints((current) => current.map((row) => [...row, 0])); };
  const removeVariable = () => { if (objective.length > 1) { setObjective((current) => current.slice(0, -1)); setConstraints((current) => current.map((row) => row.slice(0, -1))); } };
  const addConstraint = () => { setConstraints((current) => [...current, objective.map(() => "")]); setLimits((current) => [...current, ""]); setRelations((current) => [...current, "<="]); };
  const removeConstraint = () => { if (constraints.length > 1) { setConstraints((current) => current.slice(0, -1)); setLimits((current) => current.slice(0, -1)); setRelations((current) => current.slice(0, -1)); } };
  const calculate = async () => {
    setLoading(true); setError(""); setResult(null);
    try {
      if (objective.some((value) => value === "") || constraints.some((row) => row.some((value) => value === "")) || limits.some((value) => value === "")) {
        throw new Error("Complete every coefficient and constraint limit before calculating.");
      }

      const payload = {
        objective: objective.map(Number),
        constraints: constraints.map((row) => row.map(Number)),
        limits: limits.map(Number),
        relations,
        sense,
      };

      if (backendUrl) {
        const response = await fetch(backendUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData?.error || "The backend was unable to solve this problem.");
        }

        const data = await response.json();
        if (!Array.isArray(data.solution) || typeof data.maximum !== "number") {
          throw new Error("The backend returned an invalid result.");
        }

        setResult({ solution: data.solution, maximum: data.maximum });
        return;
      }

      setResult(solveModel(payload.objective, payload.constraints, payload.limits, payload.relations, payload.sense));
    } catch (requestError) { setError(requestError instanceof Error ? requestError.message : "Unable to solve this problem."); } finally { setLoading(false); }
  };

  return <main className="workspace-shell">
    <header className="topbar"><div className="brand-mark">S</div><div><p className="eyebrow">Operations research / solver</p><h1>Simplex Studio</h1></div><span className="status-dot">Solver engine online</span></header>
    <section className="intro"><div><p className="eyebrow accent">Linear programming</p><h2>Find the best allocation.</h2><p>Build a model, choose your objective and constraints, and let the simplex method find the optimum.</p></div><div className="model-note"><span>MODEL</span><strong>{sense === "max" ? "Maximize" : "Minimize"}</strong><code>cᵀx</code><small>subject to Ax {relations.join(", ")}</small></div></section>
    <div className="content-grid">
      <section className="panel model-panel">
        <div className="panel-heading"><div><span className="step">01</span><h3>Define your model</h3></div><span className="constraint-count">{constraints.length} equations · {objective.length} unknowns</span></div>
        <div className="objective-block"><div className="objective-label"><label>Objective function</label><select aria-label="Objective direction" value={sense} onChange={(event) => setSense(event.target.value as "max" | "min")}><option value="max">Maximize Z</option><option value="min">Minimize Z</option></select></div><div className="formula-row"><strong>Z =</strong>{objective.map((value, index) => <div className="coefficient" key={`objective-${index}`}><input aria-label={`Objective coefficient x${index + 1}`} type="number" value={value} onChange={(event) => updateObjective(index, event.target.value)} /><em>x{index + 1}</em>{index < objective.length - 1 && <b>+</b>}</div>)}</div><p className="formula-hint">Z = aX1 + bX2 + cX3 + ...</p></div>
        <div className="constraints-heading"><label>Subject to <span>choose a relation for every equation</span></label><div className="table-actions"><button type="button" onClick={removeConstraint} disabled={constraints.length <= 1}>− equation</button><button type="button" onClick={addConstraint}>+ equation</button></div></div>
        <div className="constraint-table"><div className="table-header" style={{ gridTemplateColumns: `48px repeat(${objective.length}, minmax(70px, 1fr)) 72px 80px` }}> <span>eq.</span>{objective.map((_, index) => <span key={`header-${index}`}>x{index + 1}</span>)}<span>relation</span><span>limit</span></div>{constraints.map((row, rowIndex) => <div className="table-row" style={{ gridTemplateColumns: `48px repeat(${objective.length}, minmax(70px, 1fr)) 72px 80px` }} key={`constraint-${rowIndex}`}><span className="row-number">C{String(rowIndex + 1).padStart(2, "0")}</span>{row.map((value, columnIndex) => <input key={`${rowIndex}-${columnIndex}`} aria-label={`Constraint ${rowIndex + 1}, x${columnIndex + 1}`} type="number" value={value} onChange={(event) => updateConstraint(rowIndex, columnIndex, event.target.value)} />)}<select className="relation-select" aria-label={`Constraint ${rowIndex + 1} relation`} value={relations[rowIndex]} onChange={(event) => setRelations((current) => current.map((item, index) => index === rowIndex ? event.target.value as Relation : item))}><option value="<=">≤</option><option value=">=">≥</option><option value="=">=</option></select><input aria-label={`Constraint ${rowIndex + 1} limit`} type="number" value={limits[rowIndex]} onChange={(event) => setLimits((current) => current.map((item, index) => index === rowIndex ? parseInput(event.target.value) : item))} /></div>)}</div>
        <div className="panel-footer"><div className="variable-actions"><button type="button" onClick={removeVariable} disabled={objective.length <= 1}>− variable</button><button type="button" onClick={addVariable}>+ variable</button></div><button className="solve-button" type="button" onClick={calculate} disabled={loading}>{loading ? "Calculating..." : "Calculate optimum"}<span>→</span></button></div>{error && <div className="error-message" role="alert">{error}</div>}
      </section>
      <aside className={`panel result-panel ${result ? "has-result" : ""}`}><div className="panel-heading"><div><span className="step">02</span><h3>Solution</h3></div><span className="result-badge">{result ? "OPTIMAL" : "WAITING"}</span></div>{result ? <><div className="maximum-label">{sense === "max" ? "Maximum" : "Minimum"} objective value</div><div className="maximum-value">{formatNumber(result.maximum)}</div><div className="solution-list">{result.solution.map((value, index) => <div className="solution-line" key={`solution-${index}`}><span>x{index + 1}</span><strong>{formatNumber(value)}</strong><small>units</small></div>)}</div><div className="result-footnote">All variables are non-negative. Result returned by the Python simplex engine.</div></> : <div className="empty-result"><div className="empty-icon">∑</div><h4>Your result will appear here</h4><p>Enter your coefficients and run the model to see the optimal variable values and objective.</p></div>}</aside>
    </div><footer><span>Simplex Studio</span><span>Standard form · Non-negative variables · ≤ constraints</span></footer>
  </main>;
}
