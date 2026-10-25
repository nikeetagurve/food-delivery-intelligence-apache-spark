import streamlit as st

def css():
    st.markdown('''<style>
    @import url("https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap");
    html,body,[class*="css"]{font-family:"DM Sans",sans-serif}.stApp{background:#f7f8fb}
    [data-testid="stSidebar"]{background:#111827}[data-testid="stSidebar"] *{color:#eef2ff!important}
    .hero{background:linear-gradient(120deg,#111827,#1f2937 55%,#ff5a36 140%);padding:34px 40px;border-radius:24px;color:white;margin-bottom:24px}
    .hero h1{font-family:"Space Grotesk";font-size:58px;letter-spacing:-3px;margin:6px 0}.hero h1 span{color:#ff6b4a}
    .hero p{font-size:17px;opacity:.82;max-width:720px}.badge{display:inline-block;font-size:11px;font-weight:800;letter-spacing:1.3px;background:#ffffff18;padding:8px 11px;border-radius:999px}
    .metric{background:white;border:1px solid #e7eaf0;border-radius:18px;padding:20px;min-height:112px;box-shadow:0 8px 25px #1118270d}
    .label{font-size:11px;font-weight:800;color:#6b7280;letter-spacing:1.1px}.value{font-family:"Space Grotesk";font-size:29px;font-weight:700;margin-top:8px;color:#111827}.sub{color:#9ca3af;font-size:12px;margin-top:4px}
    .card{background:white;border:1px solid #e7eaf0;border-radius:18px;padding:22px;min-height:150px;box-shadow:0 8px 25px #1118270a}.card h3{font-family:"Space Grotesk";margin:5px 0}.card p{color:#6b7280}.icon{font-size:28px}
    .title{font-family:"Space Grotesk";font-size:38px;letter-spacing:-1.5px}.subtitle{color:#6b7280;margin-bottom:25px}
    .source-box{background:#fff7f3;border:1px solid #ffd9ce;border-radius:15px;padding:16px 18px;margin-top:25px;color:#4b5563;font-size:13px}.source-box a{color:#e64d2f;font-weight:700}
    footer{visibility:hidden}</style>''', unsafe_allow_html=True)

def filters(df):
    st.sidebar.markdown("## 🍔 FOODPULSE")
    st.sidebar.caption("Food Delivery Intelligence")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Global filters")
    def opts(c): return ["All"] + sorted([str(x) for x in df[c].dropna().unique()])
    return {"city":st.sidebar.selectbox("City",opts("City")),
            "traffic":st.sidebar.selectbox("Traffic",opts("Road_traffic_density")),
            "weather":st.sidebar.selectbox("Weather",opts("Weather_conditions")),
            "vehicle":st.sidebar.selectbox("Vehicle",opts("Type_of_vehicle")),
            "performance":st.sidebar.selectbox("Performance",opts("Delivery_Performance"))}

def header(title, subtitle):
    st.markdown(f'<div class="title">{title}</div><div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)

def metric(col,label,value,sub):
    col.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)

def footer():
    st.markdown("---")
    st.caption("FOODPULSE · Big Data Analytics Lab · Apache Spark · Academic Year 2026–27")
