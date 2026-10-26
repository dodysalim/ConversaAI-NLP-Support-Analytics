"""Motores de análisis intercambiables (patrón Strategy + inversión de dependencias).

La interfaz solo conoce `AnalysisEngine`. Hay dos implementaciones:
    TransformerEngine → modelos XLM-R fine-tuneados (requiere transformers/torch)
    RuleBasedEngine   → reglas por palabras clave, 100 % offline y sin dependencias
"""
import sys
from typing import Dict, List, Protocol

from dashboard import config


class AnalysisEngine(Protocol):
    name: str

    def batch_predict(self, texts: List[str]) -> List[dict]: ...
    def status(self) -> Dict[str, str]: ...


class TransformerEngine:
    name = "XLM-R (modelos fine-tuneados)"

    def __init__(self):
        from src.pipeline import ConversaAIPipeline  # import diferido: es pesado
        self._pipeline = ConversaAIPipeline()

    def batch_predict(self, texts):
        return self._pipeline.batch_predict(texts)

    def status(self):
        return self._pipeline.get_model_status()


class RuleBasedEngine:
    name = "Reglas offline (palabras clave)"

    def __init__(self):
        scripts = str(config.PROJECT_DIR / "scripts")
        if scripts not in sys.path:
            sys.path.insert(0, scripts)
        from pipeline_fallback import FallbackPipeline
        self._pipeline = FallbackPipeline()

    def batch_predict(self, texts):
        return [self._pipeline.predict(t) for t in texts]

    def status(self):
        return {"sentiment": "fallback", "intent": "fallback"}


ENGINES = {"rules": RuleBasedEngine, "transformer": TransformerEngine}


def create_engine(preferred: str):
    """Crea el motor pedido; si no puede cargarse, usa el de reglas. Devuelve (motor, aviso)."""
    if preferred == "rules":
        return RuleBasedEngine(), None
    try:
        return ENGINES[preferred](), None
    except Exception as e:  # dependencias o modelos no disponibles
        return RuleBasedEngine(), f"No se pudo cargar {preferred}: {e}. Se usa el motor de reglas offline."
