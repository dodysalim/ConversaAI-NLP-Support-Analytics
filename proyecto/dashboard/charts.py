"""Fábrica de gráficos con el estilo del dashboard."""
import plotly.graph_objects as go

from dashboard import config as c

_LAYOUT = dict(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
               font=dict(family="Inter, system-ui, sans-serif", color=c.TEXT, size=12),
               legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=c.MUTED)),
               hoverlabel=dict(bgcolor="#121B2A", bordercolor=c.ACCENT, font=dict(color=c.TEXT)))
_AXES = dict(gridcolor=c.GRID, zeroline=False, linecolor=c.GRID, tickfont=dict(color=c.MUTED))


def _style(fig, **layout):
    fig.update_layout(**{**_LAYOUT, **layout})
    fig.update_xaxes(**_AXES)
    fig.update_yaxes(**_AXES)
    return fig


def _intent_names(index):
    return [c.intent_name(i) for i in index]


def sentiment_donut(counts):
    fig = go.Figure(go.Pie(labels=[s.capitalize() for s in counts.index], values=counts.values, hole=0.55,
                           marker=dict(colors=[c.SENTIMENT_COLORS[s] for s in counts.index],
                                       line=dict(color="#0B1220", width=2)),
                           textinfo="label+percent",
                           hovertemplate="<b>%{label}</b><br>%{value:,} mensajes (%{percent})<extra></extra>"))
    return _style(fig, height=350, margin=dict(t=0, b=0, l=0, r=0), showlegend=True,
                  legend=dict(orientation="h", yanchor="bottom", y=-0.2))


def intent_bars(counts):
    fig = go.Figure(go.Bar(x=_intent_names(counts.index), y=counts.values, marker_color=c.ACCENT,
                           hovertemplate="<b>%{x}</b><br>%{y:,} mensajes<extra></extra>"))
    return _style(fig, height=350, margin=dict(t=0, b=80, l=0, r=0), xaxis=dict(tickangle=45),
                  yaxis=dict(title="Cantidad de Mensajes"))


def churn_histogram(scores):
    fig = go.Figure(go.Histogram(x=scores, nbinsx=40, marker_color=c.BLUE,
                                 hovertemplate="Score: %{x:.2f}<br>Mensajes: %{y}<extra></extra>"))
    return _style(fig, height=350, xaxis=dict(title="Churn Score", range=[0, 1]),
                  yaxis=dict(title="Cantidad de Mensajes"), margin=dict(t=0, b=0, l=0, r=0), bargap=0.05)


def intent_sentiment_stack(mix):
    fig = go.Figure()
    names = _intent_names(mix.index)
    for s in c.SENTIMENTS:
        fig.add_trace(go.Bar(name=s.capitalize(), y=names, x=mix[s].values, orientation="h",
                             marker_color=c.SENTIMENT_COLORS[s],
                             hovertemplate="<b>%{y}</b><br>" + s.capitalize() + ": %{x:.1%}<extra></extra>"))
    return _style(fig, barmode="stack", height=400, margin=dict(t=0, b=0, l=0, r=0), hovermode="y unified",
                  xaxis=dict(title="Proporción", tickformat=".0%"), yaxis=dict(title="Intención"),
                  legend=dict(title="Sentimiento", orientation="h", yanchor="bottom", y=-0.15))


def churn_by_intent(series, overall):
    colors = [c.ABOVE_AVG if v > overall else c.BELOW_AVG for v in series.values]
    fig = go.Figure(go.Bar(x=_intent_names(series.index), y=series.values, marker_color=colors))
    fig.add_hline(y=overall, line_dash="dash", line_color=c.MUTED, annotation_text=f"Promedio general: {overall:.3f}", annotation_position="top left")
    return _style(fig, height=350, xaxis=dict(tickangle=45), margin=dict(t=0, b=80, l=0, r=0))


def contribution_stack(contrib):
    names = _intent_names(contrib.index)
    fig = go.Figure()
    for label, col in (("Sentimiento", "sentiment_contrib"), ("Frustración", "frustration_contrib"),
                       ("Intención", "intent_contrib")):
        fig.add_trace(go.Bar(name=label, x=names, y=contrib[col], marker_color=c.CONTRIB_COLORS[label]))
    return _style(fig, barmode="stack", height=350, xaxis=dict(tickangle=45), margin=dict(t=0, b=80, l=0, r=0))
