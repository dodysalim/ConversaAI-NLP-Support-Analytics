"""Pruebas de la lógica del dashboard y del motor offline (sin Streamlit ni modelos)."""
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dashboard import analysis, config  # noqa: E402
from dashboard.engines import RuleBasedEngine, create_engine  # noqa: E402


@pytest.fixture(scope="module")
def results():
    corpus = pd.read_csv(config.SAMPLE_CSV)
    return analysis.analyze(RuleBasedEngine(), corpus)


def test_analyze_produces_one_row_per_message(results):
    assert len(results) == len(pd.read_csv(config.SAMPLE_CSV))
    assert list(results.columns) == analysis.RESULT_COLUMNS
    assert results["churn_score"].between(0, 1).all()
    assert set(results["sentiment"]) <= set(config.SENTIMENTS)
    assert set(results["intent"]) <= set(config.INTENT_LABELS)


def test_analyze_requires_text_column():
    with pytest.raises(ValueError):
        analysis.analyze(RuleBasedEngine(), pd.DataFrame({"mensaje": ["hola"]}))


def test_create_engine_falls_back_when_unavailable(monkeypatch):
    import dashboard.engines as eng

    class Broken:
        def __init__(self): raise ImportError("sin torch")

    monkeypatch.setitem(eng.ENGINES, "transformer", Broken)
    engine, warning = create_engine("transformer")
    assert isinstance(engine, RuleBasedEngine) and "sin torch" in warning
    assert analysis.has_fallback(engine.status())


def test_has_fallback():
    assert analysis.has_fallback(None)
    assert not analysis.has_fallback({"sentiment": "xlm-r", "intent": "xlm-r"})


def frame():
    return pd.DataFrame({
        "text": ["a" * 150, "b", "c", "d", "e"],
        "sentiment": ["negative", "negative", "positive", "neutral", "negative"],
        "intent": ["queja", "queja", "feedback", "seguimiento", "queja"],
        "churn_score": [0.9, 0.8, 0.1, 0.3, 0.75],
        "sentiment_contrib": [0.3] * 5, "frustration_contrib": [0.35] * 5, "intent_contrib": [0.2] * 5,
    })


def test_overview_metrics():
    o = analysis.overview(frame())
    assert (o.total, o.high_risk, o.negative) == (5, 3, 3)
    assert o.high_risk_pct == pytest.approx(60.0)


def test_intent_sentiment_mix_rows_sum_to_one_or_zero():
    mix = analysis.intent_sentiment_mix(frame())
    assert list(mix.columns) == config.SENTIMENTS and list(mix.index) == config.INTENT_LABELS
    assert mix.loc["queja", "negative"] == 1.0 and mix.loc["cancelacion"].sum() == 0


def test_filters_and_tables():
    df = frame()
    assert len(analysis.filter_messages(df, "negative", "queja", (0.8, 1.0))) == 2
    table = analysis.high_risk_table(df, 0.7)
    assert len(table) == 3 and table["Mensaje"].iloc[0].endswith("...")
    assert table["Sentimiento"].iloc[0] == "🔴 Negative"
    assert analysis.explorer_table(df)["Intención"].iloc[0] == "Queja"


def test_alerts_use_action_map():
    found = analysis.alerts(frame())
    assert len(found) == 1 and found[0].intent == "Queja" and found[0].cases == 3
    assert found[0].action == config.ACTIONS["queja"]
