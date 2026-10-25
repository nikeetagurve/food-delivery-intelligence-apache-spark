import streamlit as st
from utils.data import load_data, apply_filters
from utils.ui import css, filters, header, footer
st.set_page_config(page_title="Insights | FoodPulse",page_icon="💡",layout="wide"); css()
base=load_data(); df=apply_filters(base,filters(base)); header("Business Insights","Evidence-based observations generated from the selected data.")
city=df.groupby("City").agg(Orders=("ID","count"),Avg=("Time_taken_min","mean")).reset_index()
traffic=df.groupby("Road_traffic_density").agg(Avg=("Time_taken_min","mean")).reset_index()
weather=df.groupby("Weather_conditions").agg(Avg=("Time_taken_min","mean")).reset_index()
vehicle=df.groupby("Type_of_vehicle").agg(Avg=("Time_taken_min","mean")).reset_index()
cards=[("📍","City bottleneck",city.loc[city.Avg.idxmax(),"City"],f"{city.Avg.max():.1f} min average"),
("🚦","Traffic signal",traffic.loc[traffic.Avg.idxmax(),"Road_traffic_density"],f"{traffic.Avg.max():.1f} min average"),
("🌦️","Weather signal",str(weather.loc[weather.Avg.idxmax(),"Weather_conditions"]),f"{weather.Avg.max():.1f} min average"),
("🛵","Fastest vehicle group",str(vehicle.loc[vehicle.Avg.idxmin(),"Type_of_vehicle"]),f"{vehicle.Avg.min():.1f} min average")]
cc=st.columns(4)
for col,(icon,title,val,desc) in zip(cc,cards):
    col.markdown(f'<div class="card"><div class="icon">{icon}</div><b>{title}</b><h3>{val}</h3><p>{desc}</p></div>',unsafe_allow_html=True)
st.markdown("### Recommendations")
for n,t,d in [("01","Traffic-aware dispatch","Prioritize route and workload adjustments in traffic categories showing higher observed delivery duration."),
              ("02","Control batching","Review multiple-delivery assignments where the selected data shows increased delivery time."),
              ("03","Monitor city bottlenecks","Use city-level KPIs to identify locations requiring operational attention."),
              ("04","Weather readiness","Compare weather conditions against delivery time and plan buffers for slower conditions.")]:
    st.markdown(f'<div class="source-box"><b>{n} · {t}</b><br>{d}</div>',unsafe_allow_html=True)
st.warning("These are descriptive associations, not proof of causation. The source does not establish revenue impact, customer satisfaction or official service-level targets."); footer()
