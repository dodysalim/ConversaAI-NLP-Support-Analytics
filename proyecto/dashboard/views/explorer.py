"""Explorador de mensajes con filtros."""
from datetime import datetime

import streamlit as st

from dashboard import analysis, config


def render_explorer(df, status):
    st.title("🔍 Explorador de Mensajes")
    st.header("🔍 Explorador de Mensajes")
    c1, c2, c3 = st.columns(3)
    sentiment = c1.selectbox("Sentimiento", ["Todos"] + config.SENTIMENTS, key="explorer_sentiment")
    intent = c2.selectbox("Intención", ["Todos"] + config.INTENT_LABELS, key="explorer_intent",
                          format_func=lambda x: config.intent_name(x) if x != "Todos" else x)
    churn_range = c3.slider("Rango Churn Score", 0.0, 1.0, (0.0, 1.0), 0.05, key="explorer_churn")

    found = analysis.filter_messages(df, sentiment, intent, churn_range)
    st.write(f"### {len(found):,} mensajes encontrados")
    st.dataframe(analysis.explorer_table(found).head(config.EXPLORER_ROWS), use_container_width=True, height=400)
    st.download_button("📥 Descargar CSV filtrado", found.to_csv(index=False),
                       f"conversaai_filtrado_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
