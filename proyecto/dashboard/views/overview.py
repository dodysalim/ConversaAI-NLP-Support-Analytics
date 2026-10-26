"""Página principal: métricas, distribuciones y mensajes de alto riesgo."""
from datetime import datetime

import streamlit as st

from dashboard import analysis, charts, config


def _metrics(df):
    st.header("📊 Métricas Principales")
    o = analysis.overview(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Mensajes Procesados", f"{o.total:,}", help="Cantidad de mensajes analizados en la carga actual")
    c2.metric("Churn Score Promedio", f"{o.avg_churn:.3f}",
              help="Score de riesgo de abandono promedio (0-1). Más alto = mayor riesgo.")
    c3.metric("Alto Riesgo (≥0.7)", f"{o.high_risk:,}", delta=f"{o.high_risk_pct:.1f}% del total",
              delta_color="inverse", help="Mensajes con churn score ≥ 0.7")
    c4.metric("Sentimiento Negativo", f"{o.negative_pct:.1f}%", delta=f"{o.negative:,} mensajes",
              delta_color="inverse", help="Porcentaje de mensajes con sentimiento negativo")


def _churn_section(df) -> float:
    st.header("⚠️ Distribución de Churn Score")
    left, right = st.columns([3, 1])
    with left:
        st.plotly_chart(charts.churn_histogram(df["churn_score"]), use_container_width=True)
    with right:
        threshold = st.slider("Threshold Alto Riesgo", 0.0, 1.0, config.HIGH_RISK_DEFAULT, 0.05,
                              help="Mensajes con churn score ≥ este valor se marcan como alto riesgo")
        o = analysis.overview(df, threshold)
        st.metric("Alto Riesgo", f"{o.high_risk:,}", delta=f"{o.high_risk_pct:.1f}%", delta_color="inverse")
    return threshold


def _high_risk(df, threshold):
    st.header(f"🔴 Mensajes de Alto Riesgo (Churn ≥ {threshold:.2f})")
    table = analysis.high_risk_table(df, threshold)
    if table.empty:
        st.success(f"✅ No hay mensajes con churn score ≥ {threshold:.2f}")
        return
    st.dataframe(table, use_container_width=True, height=400, column_config={
        "Mensaje": st.column_config.TextColumn("Mensaje", width="large"),
        "Churn Score": st.column_config.TextColumn("Churn Score", width="small"),
        "Sentimiento": st.column_config.TextColumn("Sentimiento", width="small")})
    st.download_button("📥 Descargar CSV de Alto Riesgo", df[df["churn_score"] >= threshold].to_csv(index=False),
                       f"conversaai_high_risk_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")


def _intent_by_sentiment(df):
    st.header("📊 Intenciones por Sentimiento")
    chosen = st.multiselect("Filtrar por Sentimiento", options=config.SENTIMENTS,
                            default=df["sentiment"].unique().tolist(),
                            help="Seleccioná uno o más sentimientos para filtrar las intenciones")
    st.plotly_chart(charts.intent_sentiment_stack(analysis.intent_sentiment_mix(df, chosen)), use_container_width=True)


def render_overview(df, status):
    from dashboard.styles import hero
    st.markdown(hero("ConversaAI ·", "Dashboard de Insights", "Análisis de conversaciones de soporte"),
                unsafe_allow_html=True)
    _metrics(df)
    st.divider()
    left, right = st.columns(2)
    with left:
        st.subheader("🎭 Distribución de Sentimiento")
        st.plotly_chart(charts.sentiment_donut(analysis.sentiment_counts(df)), use_container_width=True)
    with right:
        st.subheader("🎯 Distribución de Intenciones")
        st.plotly_chart(charts.intent_bars(analysis.intent_counts(df)), use_container_width=True)
    st.divider()
    threshold = _churn_section(df)
    st.divider()
    _high_risk(df, threshold)
    st.divider()
    _intent_by_sentiment(df)
