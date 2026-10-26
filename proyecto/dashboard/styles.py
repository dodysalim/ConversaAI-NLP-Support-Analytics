"""Tema visual (oscuro, coherente con el portafolio)."""

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    :root { --bg:#0B1220; --surface:#121B2A; --surface-2:#16213A; --line:#24324D;
            --text:#E6ECF5; --muted:#93A1BD; --accent:#75E6CE; --blue:#88B7FF; --violet:#C99BFF; }
    html, body, [class*="css"], .stApp { font-family:'Inter', system-ui, sans-serif; }
    .stApp { background:
        radial-gradient(900px 500px at 0% -10%, rgba(201,155,255,.10), transparent 60%),
        radial-gradient(800px 500px at 100% 0%, rgba(117,230,206,.10), transparent 60%), var(--bg); }
    .block-container { padding-top:3.5rem; max-width:1400px; }
    h1, h2, h3 { color:var(--text) !important; font-weight:700 !important; letter-spacing:-.02em; }
    hr { border-color:var(--line) !important; opacity:.6; }
    .hero { border:1px solid var(--line); border-radius:20px; padding:28px 32px; margin-bottom:12px;
            background:linear-gradient(135deg, rgba(22,33,58,.95), rgba(18,27,42,.85)); box-shadow:0 20px 60px rgba(0,0,0,.35); }
    .hero .eyebrow { color:var(--violet); font-size:12px; font-weight:700; letter-spacing:.16em; text-transform:uppercase; }
    .hero h1 { font-size:38px !important; margin:6px 0 8px !important; padding:0 !important; }
    .hero h1 span { background:linear-gradient(110deg, var(--violet), var(--blue) 50%, var(--accent));
                    -webkit-background-clip:text; background-clip:text; color:transparent; }
    .hero p { color:var(--muted); font-size:16px; margin:0; }
    .feature-grid { display:grid; grid-template-columns:repeat(3, minmax(0,1fr)); gap:14px; margin-top:16px; }
    .feature { background:var(--surface); border:1px solid var(--line); border-radius:16px; padding:18px; }
    .feature b { color:var(--text); display:block; margin-bottom:4px; }
    .feature span { color:var(--muted); font-size:14px; }
    @media (max-width: 900px) { .feature-grid { grid-template-columns:1fr; } }
    div[data-testid="stMetric"] { background:linear-gradient(160deg, var(--surface-2), var(--surface));
        border:1px solid var(--line); border-radius:16px; padding:18px 20px; transition:transform .25s, border-color .25s; }
    div[data-testid="stMetric"]:hover { transform:translateY(-4px); border-color:var(--violet); }
    div[data-testid="stMetricLabel"] p { color:var(--muted) !important; text-transform:uppercase; letter-spacing:.06em; font-size:12px !important; }
    div[data-testid="stMetricValue"] { font-weight:800; }
    [data-testid="stPlotlyChart"], [data-testid="stDataFrame"] { background:var(--surface); border:1px solid var(--line);
                                                                  border-radius:16px; padding:6px; }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#0F1829,#0B1220); border-right:1px solid var(--line); }
    [data-testid="stExpander"] { border:1px solid var(--line) !important; border-radius:14px !important; background:var(--surface); }
    .stButton > button, .stDownloadButton > button { border-radius:12px !important; font-weight:600 !important; }
</style>
"""


def hero(title_plain: str, title_accent: str, subtitle: str, eyebrow: str = "NLP · Soporte al cliente") -> str:
    return (f'<div class="hero"><div class="eyebrow">{eyebrow}</div>'
            f'<h1>{title_plain} <span>{title_accent}</span></h1><p>{subtitle}</p></div>')
