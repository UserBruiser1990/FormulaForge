import { FormEvent, useState } from "react";

const API_URL = "http://localhost:8000";
type Mode = "generate" | "explain" | "fix" | "vba" | "power-query";

function App() {
  const [mode, setMode] = useState<Mode>("generate");
  const [prompt, setPrompt] = useState("");
  const [formula, setFormula] = useState("");
  const [explanation, setExplanation] = useState("");
  const [correctedFormula, setCorrectedFormula] = useState("");
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const resultText = formula || correctedFormula || code || explanation;
  const example =
    mode === "generate"
      ? "Sum sales where region equals West"
      : mode === "explain"
        ? '=SUMIFS(C:C, B:B, "West")'
        : mode === "fix"
          ? '=SUMIF(B:B, "West", C:C'
          : mode === "vba"
            ? "Highlight overdue invoices in red"
            : "Remove blank rows and group sales by region";

  function clearForm() {
    setPrompt("");
    setFormula("");
    setExplanation("");
    setCorrectedFormula("");
    setCode("");
    setError("");
    setCopied(false);
  }

  async function copyResult() {
    try {
      await navigator.clipboard.writeText(resultText);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setError("Copying is unavailable in this browser.");
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setFormula("");
    setExplanation("");
    setCorrectedFormula("");
    setCode("");
    setError("");
    setCopied(false);
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/${mode}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(
          mode === "generate" || mode === "vba" || mode === "power-query"
            ? { prompt }
            : { formula: prompt },
        ),
      });

      if (!response.ok) {
        const body = (await response.json()) as { detail?: string };
        throw new Error(body.detail ?? "The request could not be completed.");
      }

      const body = (await response.json()) as {
        formula?: string;
        explanation?: string;
        code?: string;
      };
      if (mode === "generate") setFormula(body.formula ?? "");
      else if (mode === "explain") setExplanation(body.explanation ?? "");
      else if (mode === "fix") setCorrectedFormula(body.formula ?? "");
      else setCode(body.code ?? "");
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "The request could not be completed.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="page">
      <div className="dashboard">
        <aside className="sidebar">
          <header className="brand">
            <div className="brand-mark" aria-hidden="true">F</div>
            <div>
              <p className="eyebrow">FORMULAFORGE AI</p>
              <p className="tagline">Intelligent Excel workspace</p>
            </div>
          </header>
          <p className="nav-label">TOOLS</p>
          <nav className="tool-nav" aria-label="Formula tools">
            {(["generate", "explain", "fix", "vba", "power-query"] as Mode[]).map(
              (tool) => (
                <button
                  key={tool}
                  type="button"
                  className={mode === tool ? "active" : ""}
                  onClick={() => setMode(tool)}
                >
                  <span className="tool-icon" aria-hidden="true">
                    {tool === "generate" ? "+" : tool === "explain" ? "?" : tool === "fix" ? "✓" : tool === "vba" ? "{" : "≡"}
                  </span>
                  {tool === "power-query"
                    ? "Power Query"
                    : tool === "vba"
                      ? "VBA Generator"
                      : tool[0].toUpperCase() + tool.slice(1)}
                </button>
              ),
            )}
          </nav>
          <div className="sidebar-footer">
            <span className="status-dot" aria-hidden="true" />
            Ollama connected
          </div>
        </aside>
        <section className="workspace">
          <div className="workspace-topbar">
            <span>Workspace</span>
            <span className="model-badge">● Llama 3.1 8B</span>
          </div>
          <div className="card">
            <h1>
              {mode === "generate"
                ? "Turn plain English into Excel formulas."
                : mode === "explain"
                  ? "Understand any Excel formula."
                  : mode === "fix"
                    ? "Fix broken Excel formulas."
                    : mode === "vba"
                      ? "Generate Excel VBA macros."
                      : "Generate Power Query M code."}
            </h1>
            <p className="intro">
              {mode === "generate"
                ? "Describe what you want your formula to do, and FormulaForge will generate a starting point."
                : mode === "explain"
                  ? "Paste an existing formula and FormulaForge will explain it in plain English."
                  : mode === "fix"
                    ? "Paste a broken formula and FormulaForge will return a corrected version."
                    : mode === "vba"
                      ? "Describe an Excel task and FormulaForge will generate a VBA macro."
                      : "Describe a data transformation and FormulaForge will generate M code."}
            </p>
            <button type="button" className="example" onClick={() => setPrompt(example)}>
              <span>Try an example</span>
              <span aria-hidden="true">→</span>
            </button>
            <form onSubmit={handleSubmit}>
              <label htmlFor="prompt">
                {mode === "generate" ? "What should the formula do?" : mode === "explain" ? "Which formula should we explain?" : mode === "fix" ? "Which formula should we fix?" : mode === "vba" ? "What should the macro do?" : "What should the query do?"}
              </label>
              <textarea
                id="prompt"
                value={prompt}
                onChange={(event) => setPrompt(event.target.value)}
                placeholder={example}
                required
                rows={7}
              />
              <div className="form-actions">
                <button type="submit" disabled={isLoading || !prompt.trim()}>
                  {isLoading ? "Working..." : mode === "generate" ? "Generate formula" : mode === "explain" ? "Explain formula" : mode === "fix" ? "Fix formula" : mode === "vba" ? "Generate VBA" : "Generate M code"}
                </button>
                {prompt && <button type="button" className="clear" onClick={clearForm}>Clear</button>}
              </div>
            </form>
            {formula && <section className="result" aria-live="polite"><div className="result-header"><h2>Generated formula</h2><button type="button" className="copy" onClick={copyResult}>{copied ? "Copied" : "Copy"}</button></div><code>{formula}</code></section>}
            {explanation && <section className="result" aria-live="polite"><h2>Explanation</h2><p>{explanation}</p></section>}
            {correctedFormula && <section className="result" aria-live="polite"><div className="result-header"><h2>Corrected formula</h2><button type="button" className="copy" onClick={copyResult}>{copied ? "Copied" : "Copy"}</button></div><code>{correctedFormula}</code></section>}
            {code && <section className="result" aria-live="polite"><div className="result-header"><h2>{mode === "vba" ? "Generated VBA" : "Generated Power Query"}</h2><button type="button" className="copy" onClick={copyResult}>{copied ? "Copied" : "Copy"}</button></div><pre><code>{code}</code></pre></section>}
            {error && <p className="error" role="alert">{error}</p>}
          </div>
        </section>
      </div>
    </main>
  );
}

export default App;
