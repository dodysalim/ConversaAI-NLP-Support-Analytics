"""ConversaAI · Dashboard interactivo (punto de entrada).

    streamlit run dashboard-streamlit/dashboard_app.py

La lógica vive en `proyecto/dashboard/`. Por defecto usa el motor de reglas offline;
desde la barra lateral se puede elegir el motor XLM-R (requiere transformers y torch).
"""
import sys
from pathlib import Path

PROYECTO = Path(__file__).resolve().parent.parent / "proyecto"
if str(PROYECTO) not in sys.path:
    sys.path.insert(0, str(PROYECTO))

from dashboard.app import run  # noqa: E402

run()
