"""Pruebas del score de churn y del pipeline offline (sin modelos ni GPU)."""
import csv
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import importlib.util  # noqa: E402

# Carga directa: src/__init__.py importa transformers, que no hace falta aquí.
_spec = importlib.util.spec_from_file_location("churn", ROOT / "src" / "features" / "churn.py")
_churn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_churn)
ChurnScorer = _churn.ChurnScorer
from pipeline_fallback import FallbackPipeline, INTENT_PATTERNS  # noqa: E402

SENTIMENTS = {"negative", "neutral", "positive"}
CORPUS = ROOT / "data" / "corpus_demo_bilingue.csv"


def test_churn_score_bounded_and_weighted():
    scorer = ChurnScorer()
    worst = scorer.score(
        {"probabilities": {"negative": 1.0}},
        {"probabilities": {"cancelacion": 1.0}},
        "Pésimo servicio, quiero la cancelación",
    )
    assert worst["aggregate_score"] == pytest.approx(1.0)

    calm = scorer.score(
        {"probabilities": {"positive": 1.0}},
        {"probabilities": {"consulta_general": 1.0}},
        "Gracias, todo perfecto",
    )
    assert calm["aggregate_score"] == pytest.approx(0.0)


def test_frustration_detected_in_portuguese():
    assert ChurnScorer._detect_frustration("Péssimo atendimento, nunca mais") == 1.0
    assert ChurnScorer._detect_frustration("Obrigado pela ajuda") == 0.0


def test_fallback_returns_valid_labels_for_demo_corpus():
    pipe = FallbackPipeline()
    with open(CORPUS, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) >= 100
    for row in rows:
        s = pipe.predict_sentiment(row["text"])
        i = pipe.predict_intent(row["text"])
        assert s["label"] in SENTIMENTS
        assert i["intent"] in INTENT_PATTERNS
        assert 0.0 <= s["probability"] <= 1.0
        assert 0.0 <= i["probability"] <= 1.0


def test_fallback_churn_is_higher_for_angry_cancellation():
    pipe = FallbackPipeline()
    angry = "Pésimo servicio, quiero cancelar ya, nunca más"
    happy = "Excelente atención, muchas gracias"
    def churn(text):
        out = pipe.compute_churn(text, pipe.predict_sentiment(text), pipe.predict_intent(text))
        return out["aggregate_score"]
    assert churn(angry) > churn(happy)
