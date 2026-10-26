"""Cálculos sobre los resultados del análisis (sin Streamlit, fáciles de probar)."""
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd

from dashboard import config

RESULT_COLUMNS = ["text", "sentiment", "sentiment_prob", "sentiment_neg_prob", "sentiment_neu_prob",
                  "sentiment_pos_prob", "intent", "intent_prob", "churn_score", "sentiment_contrib",
                  "frustration_contrib", "intent_contrib"]


def results_to_frame(results: Iterable[dict]) -> pd.DataFrame:
    """Aplana la salida del pipeline: una fila por mensaje."""
    rows = []
    for r in results:
        sent, intent, churn = r["sentiment"], r["intent"], r["churn"]
        probs = sent.get("probabilities", {})
        rows.append({
            "text": r["text"], "sentiment": sent["label"], "sentiment_prob": sent["probability"],
            "sentiment_neg_prob": probs.get("negative", 0.0), "sentiment_neu_prob": probs.get("neutral", 0.0),
            "sentiment_pos_prob": probs.get("positive", 0.0), "intent": intent["intent"],
            "intent_prob": intent["probability"], "churn_score": churn["aggregate_score"],
            "sentiment_contrib": churn["sentiment_contribution"],
            "frustration_contrib": churn["frustration_contribution"], "intent_contrib": churn["intent_contribution"],
        })
    return pd.DataFrame(rows, columns=RESULT_COLUMNS)


def analyze(engine, data: pd.DataFrame) -> pd.DataFrame:
    if "text" not in data.columns:
        raise ValueError("El CSV debe tener una columna 'text' con los mensajes.")
    return results_to_frame(engine.batch_predict(data["text"].fillna("").tolist()))


def has_fallback(status: Optional[Dict[str, str]]) -> bool:
    if status is None:
        return True
    return status.get("sentiment") == "fallback" or status.get("intent") == "fallback"


@dataclass(frozen=True)
class Overview:
    total: int
    avg_churn: float
    high_risk: int
    high_risk_pct: float
    negative: int
    negative_pct: float


def overview(df: pd.DataFrame, threshold: float = config.HIGH_RISK_DEFAULT) -> Overview:
    total = len(df)
    high = int((df["churn_score"] >= threshold).sum())
    neg = int((df["sentiment"] == "negative").sum())
    pct = lambda n: n / total * 100 if total else 0.0
    return Overview(total, float(df["churn_score"].mean()) if total else 0.0, high, pct(high), neg, pct(neg))


def sentiment_counts(df):
    return df["sentiment"].value_counts().reindex(config.SENTIMENTS, fill_value=0)


def intent_counts(df):
    return df["intent"].value_counts().reindex(config.INTENT_LABELS, fill_value=0)


def intent_sentiment_mix(df, sentiments: Optional[List[str]] = None) -> pd.DataFrame:
    """Proporción de cada sentimiento dentro de cada intención (filas suman 1)."""
    data = df[df["sentiment"].isin(sentiments)] if sentiments else df
    mix = pd.crosstab(data["intent"], data["sentiment"], normalize="index")
    for s in config.SENTIMENTS:
        if s not in mix.columns:
            mix[s] = 0.0
    return mix.reindex(config.INTENT_LABELS, fill_value=0.0)[config.SENTIMENTS]


def filter_messages(df, sentiment: str = "Todos", intent: str = "Todos",
                    churn_range: Tuple[float, float] = (0.0, 1.0)) -> pd.DataFrame:
    out = df
    if sentiment != "Todos":
        out = out[out["sentiment"] == sentiment]
    if intent != "Todos":
        out = out[out["intent"] == intent]
    lo, hi = churn_range
    return out[(out["churn_score"] >= lo) & (out["churn_score"] <= hi)]


def sentiment_badge(sentiment: str) -> str:
    return f"{config.SENTIMENT_EMOJI.get(sentiment, '⚪')} {sentiment.capitalize()}"


def preview(text, limit: int = config.PREVIEW_CHARS):
    return text[:limit] + "..." if isinstance(text, str) and len(text) > limit else text


def high_risk_table(df, threshold: float) -> pd.DataFrame:
    cols = {"text": "Mensaje", "sentiment": "Sentimiento", "intent": "Intención", "churn_score": "Churn Score",
            "sentiment_contrib": "Contrib. Sent.", "frustration_contrib": "Contrib. Frust.",
            "intent_contrib": "Contrib. Intent"}
    out = df[df["churn_score"] >= threshold][list(cols)].rename(columns=cols)
    for c in ["Churn Score", "Contrib. Sent.", "Contrib. Frust.", "Contrib. Intent"]:
        out[c] = out[c].map(lambda x: f"{x:.3f}")
    out["Mensaje"] = out["Mensaje"].map(preview)
    out["Sentimiento"] = out["Sentimiento"].map(sentiment_badge)
    return out


def explorer_table(df) -> pd.DataFrame:
    out = df[["text", "sentiment", "intent", "churn_score"]].copy()
    out.columns = ["Mensaje", "Sentimiento", "Intención", "Churn Score"]
    out["Sentimiento"] = out["Sentimiento"].map(sentiment_badge)
    out["Intención"] = out["Intención"].map(config.intent_name)
    out["Churn Score"] = out["Churn Score"].map(lambda x: f"{x:.3f}")
    return out


def churn_by_intent(df) -> pd.Series:
    return df.groupby("intent")["churn_score"].mean().reindex(config.INTENT_LABELS, fill_value=0)


def churn_contributions(df) -> pd.DataFrame:
    cols = ["sentiment_contrib", "frustration_contrib", "intent_contrib"]
    return df.groupby("intent")[cols].mean().reindex(config.INTENT_LABELS, fill_value=0)


def top_intents(df, mask, n: int = 5) -> pd.Series:
    return df[mask]["intent"].value_counts().head(n)


@dataclass(frozen=True)
class Alert:
    intent: str
    cases: int
    avg_churn: float
    action: str


def alerts(df, threshold: float = config.HIGH_RISK_DEFAULT, min_cases: int = config.ALERT_MIN_CASES) -> List[Alert]:
    """Intenciones con varios mensajes de alto riesgo y la acción sugerida para cada una."""
    out = []
    for intent, count in df[df["churn_score"] >= threshold]["intent"].value_counts().items():
        if count >= min_cases:
            out.append(Alert(config.intent_name(intent), int(count), float(df[df["intent"] == intent]["churn_score"].mean()),
                             config.ACTIONS.get(intent, config.DEFAULT_ACTION)))
    return out
