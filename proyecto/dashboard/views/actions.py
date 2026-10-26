"""Recomendaciones para el equipo de producto."""
import streamlit as st

from dashboard import analysis, charts, config


def _intent_list(title, series):
    st.markdown(title)
    for intent, count in series.items():
        st.write(f"- {config.intent_name(intent)}: {count:,} mensajes")


def render_actions(df, status):
    st.title("💡 Recomendaciones para el Equipo de Producto")
    st.markdown("### 📊 Churn Promedio por Intención")
    st.plotly_chart(charts.churn_by_intent(analysis.churn_by_intent(df), df["churn_score"].mean()),
                    use_container_width=True)
    st.caption("🔴 Barras rojas = por encima del promedio. Priorizar estas intenciones.")
    st.divider()

    st.markdown("### 🎯 Intenciones de Alto Riesgo")
    left, right = st.columns(2)
    with left:
        _intent_list("**Más sentimiento negativo:**", analysis.top_intents(df, df["sentiment"] == "negative"))
    with right:
        _intent_list("**Mayor churn (≥0.7):**", analysis.top_intents(df, df["churn_score"] >= config.HIGH_RISK_DEFAULT))
    st.divider()

    st.markdown("### 🔍 Desglose de Churn por Intención")
    st.plotly_chart(charts.contribution_stack(analysis.churn_contributions(df)), use_container_width=True)
    st.caption("Azul = sentimiento negativo · Rojo = frustración por keywords · Violeta = intención de riesgo")
    st.divider()

    st.markdown("### 🚨 Alertas y Acciones Sugeridas")
    found = analysis.alerts(df)
    if not found:
        st.success("✅ No hay alertas críticas en este lote de datos")
    for a in found:
        with st.expander(f"⚠️ {a.intent} — {a.cases:,} casos (churn prom. {a.avg_churn:.2f})"):
            st.markdown(a.action)
    st.divider()

    st.markdown("### 📋 Resumen Ejecutivo")
    o = analysis.overview(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total mensajes", f"{o.total:,}", help="Mensajes analizados en esta carga")
    c2.metric("Sentimiento negativo", f"{o.negative_pct:.1f}%", help="Porcentaje de mensajes con sentimiento negativo")
    c3.metric("Alto riesgo de churn", f"{o.high_risk_pct:.1f}%", help="Porcentaje de mensajes con churn ≥ 0.7")
