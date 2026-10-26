"""Barra lateral: fuente de datos, motor de análisis, estado y navegación."""
from datetime import datetime

import pandas as pd
import streamlit as st

from dashboard import config
from dashboard.analysis import analyze
from dashboard.engines import create_engine

ENGINE_OPTIONS = {"⚙️ Reglas offline (instantáneo)": "rules", "🤖 XLM-R fine-tuneado (descarga modelos)": "transformer"}


@st.cache_data
def load_sample_corpus():
    return pd.read_csv(config.SAMPLE_CSV) if config.SAMPLE_CSV.exists() else None


@st.cache_resource
def get_engine(preferred: str):
    return create_engine(preferred)


def _data_source():
    source = st.sidebar.radio("Fuente de datos", ["📂 Corpus de ejemplo", "📁 Subir CSV"], index=0,
                              help="Seleccioná 'Corpus de ejemplo' para usar el dataset precargado "
                                   "o 'Subir CSV' para analizar tus propios datos.")
    if source == "📂 Corpus de ejemplo":
        data = load_sample_corpus()
        if data is not None:
            st.sidebar.success(f"✅ Corpus cargado: {len(data):,} mensajes")
        else:
            st.sidebar.warning("⚠️ No se encontró corpus_demo_bilingue.csv")
        return data
    uploaded = st.sidebar.file_uploader("Subí tu CSV", type=["csv"],
                                        help="El CSV debe tener una columna 'text' con los mensajes")
    if uploaded is None:
        return None
    try:
        data = pd.read_csv(uploaded)
    except Exception as e:
        st.error(f"❌ Error leyendo CSV: {e}")
        return None
    st.sidebar.success(f"✅ CSV cargado: {len(data):,} mensajes")
    return data


def _run_analysis(data, engine_key):
    with st.sidebar.status("Analizando...", expanded=True) as status:
        engine, warning = get_engine(engine_key)
        if warning:
            st.sidebar.warning(warning)
        try:
            results = analyze(engine, data)
        except ValueError as e:
            st.error(f"❌ {e}")
            return status.update(label="❌ Error en análisis", state="error")
        if results.empty:
            st.sidebar.warning("El análisis devolvió 0 resultados")
            return status.update(label="Sin resultados", state="error")
        st.session_state.update(results_df=results, model_status=engine.status(), engine_name=engine.name,
                                last_update=datetime.now().strftime('%Y-%m-%d %H:%M'))
        status.update(label="✅ Análisis completo", state="complete")


def render_sidebar(pages) -> str:
    st.sidebar.title("💬 ConversaAI")
    st.sidebar.markdown("### Pipeline de Análisis")
    data = _data_source()
    engine_label = st.sidebar.selectbox("Motor de análisis", list(ENGINE_OPTIONS),
                                        help="Las reglas funcionan sin internet; XLM-R descarga ~1 GB de modelos.")
    st.sidebar.divider()
    if st.sidebar.button("▶️ Run Analysis", type="primary", use_container_width=True, disabled=data is None,
                         help="Procesar todos los mensajes con el pipeline de IA") and data is not None:
        _run_analysis(data, ENGINE_OPTIONS[engine_label])

    st.sidebar.divider()
    st.sidebar.markdown("### Estado del Pipeline")
    status = st.session_state.get("model_status")
    if status:
        for model, mode in status.items():
            emoji, label = ("🤖", "XLM-R") if mode == "xlm-r" else ("⚙️", "Fallback")
            st.sidebar.markdown(f"{emoji} **{model.capitalize()}**: {label}")
    else:
        st.sidebar.info("ℹ️ Ejecutá 'Run Analysis' para ver el estado")

    st.sidebar.divider()
    st.sidebar.markdown("### Navegación")
    page = st.sidebar.radio("Ir a:", list(pages), label_visibility="collapsed")
    st.sidebar.divider()
    st.sidebar.markdown(f"**Actualizado:** {st.session_state.get('last_update') or '—'}")
    st.sidebar.caption("Desarrollado por ConversaAI · Modelos: "
                       "[Rosela/xlm-r-sentiment-espt](https://huggingface.co/Rosela/xlm-r-sentiment-espt)")
    return page
