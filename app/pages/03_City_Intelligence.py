import streamlit as st
import plotly.express as px
from utils.data import load_data, apply_filters
from utils.ui import css, filters, header, footer
st.set_page_config(page_title="City Intelligence | FoodPulse",page_icon="📍",layout="wide"); css()
base=load_data(); df=apply_filters(base,filters(base)); header("City Intelligence","Compare speed, demand, distance and ratings across city categories.")
city=df.groupby("City",as_index=False).agg(Orders=("ID","count"),Avg_Time=("Time_taken_min","mean"),Median_Time=("Time_taken_min","median"),Avg_Rating=("Delivery_person_Ratings","mean"),Avg_Distance=("Distance_km","mean"))
a,b=st.columns(2)
with a:
    st.plotly_chart(px.bar(city.sort_values("Avg_Time"),x="Avg_Time",y="City",orientation="h",color="Avg_Time",title="City delivery-time ranking"),use_container_width=True)
with b:
    st.plotly_chart(px.scatter(city,x="Orders",y="Avg_Time",size="Avg_Distance",hover_name="City",title="Demand vs delivery time"),use_container_width=True)
for c in ["Avg_Time","Median_Time","Avg_Rating","Avg_Distance"]: city[c]=city[c].round(2)
st.dataframe(city.sort_values("Orders",ascending=False),use_container_width=True,hide_index=True); footer()
