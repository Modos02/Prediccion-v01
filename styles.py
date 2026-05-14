# ── Módulo de estilos CSS y helpers HTML ──
# Contiene todo el CSS profesional y funciones helper para componentes visuales

FONT_AWESOME = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">'
GOOGLE_FONTS = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Base ── */
html, body, .main, .stApp {
    font-family: 'Inter', sans-serif !important;
    background: linear-gradient(160deg, #070b14 0%, #0d1525 40%, #111d35 100%) !important;
    color: #e2e8f0 !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1628 0%, #0f1f3d 100%) !important;
    border-right: 1px solid rgba(59,130,246,0.15);
}
section[data-testid="stSidebar"] .stRadio > label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 600;
}
section[data-testid="stSidebar"] .stRadio > div > label {
    background: rgba(15,23,42,0.6);
    border: 1px solid rgba(59,130,246,0.1);
    border-radius: 10px;
    padding: 10px 14px !important;
    margin-bottom: 6px;
    transition: all 0.25s ease;
    color: #cbd5e1 !important;
    font-weight: 500;
}
section[data-testid="stSidebar"] .stRadio > div > label:hover {
    border-color: rgba(59,130,246,0.4);
    background: rgba(59,130,246,0.08);
    transform: translateX(3px);
}
section[data-testid="stSidebar"] .stRadio > div > label[data-checked="true"],
section[data-testid="stSidebar"] .stRadio > div [aria-checked="true"] {
    background: rgba(59,130,246,0.15) !important;
    border-color: #3b82f6 !important;
    color: #ffffff !important;
}
section[data-testid="stSidebar"] .stSlider > label,
section[data-testid="stSidebar"] .stSelectbox > label,
section[data-testid="stSidebar"] .stMultiSelect > label {
    color: #94a3b8 !important;
    font-weight: 600;
    font-size: 0.8rem;
}

/* ── Metric cards (Streamlit native) ── */
div[data-testid="stMetric"] {
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(59,130,246,0.12);
    border-radius: 16px;
    padding: 20px 18px;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(59,130,246,0.35);
    box-shadow: 0 8px 30px rgba(59,130,246,0.1);
}
div[data-testid="stMetric"] label {
    color: #64748b !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    font-size: 1.6rem !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] svg { display: none; }

/* ── Headings ── */
h1 { color: #f8fafc !important; font-weight: 800 !important; letter-spacing: -0.5px; }
h2 { color: #e2e8f0 !important; font-weight: 700 !important; }
h3 { color: #cbd5e1 !important; font-weight: 600 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.3px;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 4px 15px rgba(37,99,235,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 25px rgba(59,130,246,0.45) !important;
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: rgba(15,23,42,0.5);
    border-radius: 14px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #94a3b8;
    font-weight: 500;
    padding: 10px 20px;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background: rgba(59,130,246,0.15) !important;
    color: #3b82f6 !important;
    font-weight: 600;
}

/* ── DataFrame ── */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* ── Plotly charts ── */
.stPlotlyChart { border-radius: 16px; overflow: hidden; }

/* ── Divider ── */
hr { border-color: rgba(59,130,246,0.1) !important; margin: 1.5rem 0 !important; }

/* ── Custom metric card (HTML) ── */
.metric-row { display: flex; gap: 16px; margin-bottom: 20px; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 180px;
    background: rgba(15,23,42,0.65);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(59,130,246,0.12);
    border-radius: 16px;
    padding: 22px 20px;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}
.metric-card:hover {
    transform: translateY(-3px);
    border-color: rgba(59,130,246,0.3);
    box-shadow: 0 8px 30px rgba(59,130,246,0.08);
}
.metric-card .mc-icon {
    font-size: 1.3rem; color: #3b82f6;
    margin-bottom: 10px; opacity: 0.85;
}
.metric-card .mc-label {
    font-size: 0.72rem; color: #64748b;
    text-transform: uppercase; letter-spacing: 1.2px;
    font-weight: 600; margin-bottom: 6px;
}
.metric-card .mc-value {
    font-size: 1.5rem; font-weight: 700;
    color: #f1f5f9; line-height: 1.2;
}
.metric-card .mc-delta {
    font-size: 0.82rem; font-weight: 600;
    margin-top: 6px;
}
.mc-delta.positive { color: #22c55e; }
.mc-delta.negative { color: #ef4444; }

/* ── Section header ── */
.section-header {
    display: flex; align-items: center; gap: 14px;
    margin-bottom: 8px;
}
.section-header .sh-icon {
    width: 46px; height: 46px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; color: #ffffff;
    background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
    box-shadow: 0 4px 15px rgba(37,99,235,0.3);
}
.section-header h2 {
    margin: 0 !important; padding: 0 !important;
    font-size: 1.5rem !important;
}
.section-desc {
    color: #64748b; font-size: 0.9rem;
    margin-bottom: 24px; line-height: 1.6;
}

/* ── Info box ── */
.info-box {
    background: rgba(59,130,246,0.08);
    border-left: 3px solid #3b82f6;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px; margin: 16px 0;
    color: #94a3b8; font-size: 0.88rem;
}
.warn-box {
    background: rgba(245,158,11,0.08);
    border-left: 3px solid #f59e0b;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px; margin: 16px 0;
    color: #d4a052; font-size: 0.88rem;
}

/* ── Trend badge ── */
.trend-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 14px; border-radius: 20px;
    font-size: 0.85rem; font-weight: 600;
}
.trend-up { background: rgba(34,197,94,0.12); color: #22c55e; }
.trend-down { background: rgba(239,68,68,0.12); color: #ef4444; }

/* ── Progress / spinner ── */
.stSpinner > div { color: #3b82f6 !important; }

/* ── Footer ── */
.app-footer {
    text-align: center; padding: 30px 0 15px;
    color: #475569; font-size: 0.78rem;
    border-top: 1px solid rgba(59,130,246,0.08);
    margin-top: 40px;
}
</style>
"""


def section_header(icon_class, title):
    return f'''<div class="section-header">
        <div class="sh-icon"><i class="{icon_class}"></i></div>
        <h2>{title}</h2>
    </div>'''


def metric_card(icon_class, label, value, delta=None, delta_positive=True):
    delta_html = ""
    if delta is not None:
        cls = "positive" if delta_positive else "negative"
        arrow = "fa-arrow-trend-up" if delta_positive else "fa-arrow-trend-down"
        delta_html = f'<div class="mc-delta {cls}"><i class="fa-solid {arrow}"></i> {delta}</div>'
    return f'''<div class="metric-card">
        <div class="mc-icon"><i class="{icon_class}"></i></div>
        <div class="mc-label">{label}</div>
        <div class="mc-value">{value}</div>
        {delta_html}
    </div>'''


def metric_row(cards):
    return '<div class="metric-row">' + ''.join(cards) + '</div>'


def info_box(text, icon="fa-circle-info"):
    return f'<div class="info-box"><i class="fa-solid {icon}"></i> {text}</div>'


def warn_box(text, icon="fa-triangle-exclamation"):
    return f'<div class="warn-box"><i class="fa-solid {icon}"></i> {text}</div>'


def trend_badge(direction, text):
    cls = "trend-up" if direction == "up" else "trend-down"
    icon = "fa-arrow-trend-up" if direction == "up" else "fa-arrow-trend-down"
    return f'<span class="trend-badge {cls}"><i class="fa-solid {icon}"></i> {text}</span>'
