import streamlit as st


def css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --fp-bg: #f5f7fa;
        --fp-surface: #ffffff;
        --fp-text: #1e293b;
        --fp-muted: #64748b;
        --fp-border: #e2e8f0;
        --fp-orange: #f45b35;
        --fp-orange-soft: #fff1eb;
        --fp-slate: #0f172a;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--fp-text);
    }

    .stApp {
        background: var(--fp-bg);
        color: var(--fp-text);
    }

    [data-testid="stHeader"] {
        background: rgba(245,247,250,.94);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--fp-border);
    }

    [data-testid="stSidebar"] * {
        color: var(--fp-text);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
        color: var(--fp-orange);
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] label p,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #334155 !important;
        font-weight: 600 !important;
    }

    /* Selectbox closed state: readable text on white surface */
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stApp"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
        box-shadow: none !important;
    }

    [data-baseweb="select"] *,
    [data-baseweb="select"] input,
    [data-baseweb="select"] [role="combobox"],
    [data-baseweb="select"] [role="button"] {
        color: #1e293b !important;
        -webkit-text-fill-color: #1e293b !important;
    }

    [data-baseweb="select"] svg {
        fill: #475569 !important;
        color: #475569 !important;
    }

    /* Open dropdown menu and its options */
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="menu"],
    [role="listbox"],
    [role="option"] {
        background: #ffffff !important;
        color: #1e293b !important;
    }

    [role="option"] * {
        color: #1e293b !important;
        -webkit-text-fill-color: #1e293b !important;
    }

    [role="option"]:hover {
        background: #fff1eb !important;
    }

    [aria-selected="true"] {
        background: #ffede5 !important;
        color: #9a3412 !important;
    }

    [data-baseweb="select"]:focus-within > div {
        border-color: var(--fp-orange) !important;
        box-shadow: 0 0 0 2px #f45b3522 !important;
    }

    input, textarea {
        background: #ffffff !important;
        color: #1e293b !important;
        border-color: #cbd5e1 !important;
    }

    [data-testid="stMultiSelect"] [data-baseweb="tag"] {
        background: #ffede5 !important;
        color: #9a3412 !important;
    }

    .hero {
        background: linear-gradient(120deg, #0f172a 0%, #334155 72%, #f45b35 145%);
        padding: 32px 36px;
        border-radius: 22px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 12px 28px #0f172a12;
    }

    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(34px, 4vw, 54px);
        letter-spacing: -1.8px;
        margin: 6px 0;
        color: #ffffff;
    }

    .hero h1 span { color: #ff9b7d; }

    .hero p {
        font-size: 16px;
        color: #e2e8f0;
        max-width: 760px;
    }

    .badge {
        display: inline-block;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        background: #ffffff20;
        padding: 8px 11px;
        border-radius: 999px;
        color: #ffffff;
    }

    .metric, .card {
        background: var(--fp-surface);
        border: 1px solid var(--fp-border);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 5px 18px #0f172a08;
    }

    .metric { min-height: 112px; }
    .card { min-height: 140px; }

    .label {
        font-size: 11px;
        font-weight: 800;
        color: var(--fp-muted);
        letter-spacing: .8px;
    }

    .value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        margin-top: 8px;
        color: var(--fp-slate);
    }

    .sub { color: var(--fp-muted); font-size: 12px; margin-top: 4px; }
    .card h3 { font-family: 'Space Grotesk', sans-serif; color: var(--fp-slate); }
    .card p { color: var(--fp-muted); }

    .title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(28px, 3vw, 38px);
        letter-spacing: -1px;
        color: var(--fp-slate);
    }

    .subtitle { color: var(--fp-muted); margin-bottom: 24px; }

    .source-box {
        background: #fff7f3;
        border: 1px solid #fed7c8;
        border-radius: 14px;
        padding: 16px 18px;
        margin-top: 20px;
        color: #475569;
        font-size: 13px;
    }

    .source-box a { color: #c2410c; font-weight: 700; }

    div.stButton > button {
        border-radius: 10px;
        border: 1px solid #f45b35;
    }

    div.stButton > button[kind="primary"] {
        background: #f45b35;
        color: #ffffff;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid var(--fp-border);
        border-radius: 12px;
        overflow: hidden;
    }

    footer { visibility: hidden; }

    @media (max-width: 700px) {
        .hero { padding: 24px 20px; }
        .metric, .card { padding: 15px; }
    }
    </style>
    """, unsafe_allow_html=True)


def filters(df):
    st.sidebar.markdown("## 🍊 FOODPULSE")
    st.sidebar.caption("Food delivery intelligence")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Explore your data")

    def opts(col):
        if col not in df.columns:
            return ["All"]
        return ["All"] + sorted(str(x) for x in df[col].dropna().unique())

    selected = {
        "city": st.sidebar.selectbox("City category", opts("City"), key="fp_city"),
        "traffic": st.sidebar.selectbox("Road traffic", opts("Road_traffic_density"), key="fp_traffic"),
        "weather": st.sidebar.selectbox("Weather", opts("Weather_conditions"), key="fp_weather"),
        "vehicle": st.sidebar.selectbox("Vehicle type", opts("Type_of_vehicle"), key="fp_vehicle"),
        "performance": st.sidebar.selectbox("Delivery performance", opts("Delivery_Performance"), key="fp_performance"),
    }

    st.sidebar.caption(
        "Filters apply across the dashboard. City values are dataset categories, "
        "not named cities or neighbourhoods."
    )
    if st.sidebar.button("Reset all filters", use_container_width=True):
        for key in ["fp_city", "fp_traffic", "fp_weather", "fp_vehicle", "fp_performance"]:
            st.session_state[key] = "All"
        st.rerun()

    return selected


def header(title, subtitle):
    st.markdown(
        f'<div class="title">{title}</div><div class="subtitle">{subtitle}</div>',
        unsafe_allow_html=True
    )


def metric(col, label, value, sub):
    col.markdown(
        f'<div class="metric"><div class="label">{label}</div>'
        f'<div class="value">{value}</div><div class="sub">{sub}</div></div>',
        unsafe_allow_html=True
    )


def footer():
    st.markdown("---")
    st.caption("FOODPULSE · Big Data Analytics Lab · Apache Spark · Academic Year 2026–27")
