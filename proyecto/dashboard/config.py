"""Constantes del dashboard de ConversaAI."""
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SAMPLE_CSV = PROJECT_DIR / "data" / "corpus_demo_bilingue.csv"

PAGE_CONFIG = dict(page_title="ConversaAI — Dashboard de Insights", page_icon="💬",
                   layout="wide", initial_sidebar_state="expanded")

SENTIMENTS = ["negative", "neutral", "positive"]
SENTIMENT_EMOJI = {"negative": "🔴", "neutral": "🟡", "positive": "🟢"}
INTENT_LABELS = ["cancelacion", "consulta_general", "facturacion_pago", "feedback", "gestion_cuenta",
                 "modificacion_pedido", "queja", "reembolso", "seguimiento"]
INTENT_DISPLAY = {
    "cancelacion": "Cancelación", "consulta_general": "Consulta General", "facturacion_pago": "Facturación/Pago",
    "feedback": "Feedback", "gestion_cuenta": "Gestión de Cuenta", "modificacion_pedido": "Modificación Pedido",
    "queja": "Queja", "reembolso": "Reembolso", "seguimiento": "Seguimiento",
}

HIGH_RISK_DEFAULT = 0.7
ALERT_MIN_CASES = 3
EXPLORER_ROWS = 100
PREVIEW_CHARS = 100

# Acción sugerida por intención (agregar una intención nueva no requiere tocar código)
ACTIONS = {
    "cancelacion": "🔴 Revisar proceso de retención — ofrecer descuentos o beneficios",
    "queja": "🔴 Escalar a equipo de calidad — contactar al cliente en < 24h",
    "reembolso": "🟠 Agilizar proceso de reembolso — priorizar sobre otros tickets",
    "facturacion_pago": "🟠 Revisar errores de cobro — verificar integraciones con gateway",
}
DEFAULT_ACTION = "🟡 Investigar causa raíz — revisar conversaciones recientes"

# Paleta (coherente con el portafolio)
SENTIMENT_COLORS = {"negative": "#FF8A80", "neutral": "#F8D66D", "positive": "#75E6CE"}
ACCENT = "#C99BFF"
BLUE = "#88B7FF"
ABOVE_AVG = "#FF8A80"
BELOW_AVG = "#75E6CE"
CONTRIB_COLORS = {"Sentimiento": "#88B7FF", "Frustración": "#FF8A80", "Intención": "#C99BFF"}
TEXT = "#E6ECF5"
MUTED = "#93A1BD"
GRID = "rgba(147,161,189,0.15)"


def intent_name(intent: str) -> str:
    return INTENT_DISPLAY.get(intent, intent.replace("_", " ").title())
