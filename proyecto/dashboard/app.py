"""Composición del dashboard de ConversaAI."""
import streamlit as st

from dashboard import analysis, config
from dashboard.styles import CSS, hero
from dashboard.views.actions import render_actions
from dashboard.views.explorer import render_explorer
from dashboard.views.overview import render_overview
from dashboard.views.sidebar import render_sidebar

# Registro de páginas: agregar una página nueva = agregar una entrada
PAGES = {"📊 Dashboard": render_overview, "🔍 Explorar": render_explorer, "💡 Acciones": render_actions}

WELCOME = """
<div class="feature-grid">
  <div class="feature"><b>🎭 Sentimiento</b><span>3 clases (negativo, neutral, positivo) con XLM-R fine-tuneado (92.2% acc).</span></div>
  <div class="feature"><b>🎯 Intención</b><span>9 clases (cancelación, queja, reembolso…) con XLM-R fine-tuneado (99.6% F1).</span></div>
  <div class="feature"><b>⚠️ Churn Score</b><span>De 0 a 1, combinando sentimiento, frustración e intención.</span></div>
</div>
"""


def run() -> None:
    st.set_page_config(**config.PAGE_CONFIG)
    st.markdown(CSS, unsafe_allow_html=True)
    for key in ("results_df", "model_status", "last_update"):
        st.session_state.setdefault(key, None)

    page = render_sidebar(PAGES)
    df, status = st.session_state["results_df"], st.session_state["model_status"]
    if df is None:
        st.markdown(hero("ConversaAI ·", "Dashboard de Insights", "Sistema de análisis de conversaciones de soporte. "
                         "Cargá datos desde el panel izquierdo y presioná <b>▶️ Run Analysis</b> para comenzar."),
                    unsafe_allow_html=True)
        st.markdown(WELCOME, unsafe_allow_html=True)
        st.caption("📂 Usá el *Corpus de ejemplo* precargado o subí tu propio CSV. "
                   "El motor de reglas funciona sin internet; XLM-R descarga los modelos desde Hugging Face.")
        return
    if status and not analysis.has_fallback(status):
        st.success("✅ **Modo completo**: XLM-R fine-tuneado activo para sentimiento (92.2%) e intención (99.6% F1)")
    elif status:
        st.info("⚙️ **Motor de reglas offline** · resultados aproximados por palabras clave. "
                "Elegí XLM-R en la barra lateral para usar los modelos fine-tuneados.")
    PAGES[page](df, status)
