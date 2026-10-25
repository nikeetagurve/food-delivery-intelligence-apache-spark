import streamlit as st
import plotly.express as px
from utils.data import load_data, apply_filters
from utils.ui import css, filters, header, footer
st.set_page_config(page_title="Delivery Intelligence | FoodPulse",page_icon="🚴",layout="wide"); css()
base=load_data(); df=apply_filters(base,filters(base)); header("Delivery Intelligence","Find the operational factors associated with slower or faster deliveries.")
a,b=st.columns(2)
with a:
    x=df.groupby("Road_traffic_density",as_index=False).agg(Avg=("Time_taken_min","mean"))
    st.plotly_chart(px.bar(x,x="Road_traffic_density",y="Avg",text_auto=".1f",title="Traffic density → delivery time"),use_container_width=True)
with b:
    x=df.groupby("Weather_conditions",as_index=False).agg(Avg=("Time_taken_min","mean"))
    st.plotly_chart(px.bar(x,x="Weather_conditions",y="Avg",text_auto=".1f",title="Weather → delivery time"),use_container_width=True)
a,b=st.columns(2)
with a:
    x=df.groupby("Type_of_vehicle",as_index=False).agg(Avg=("Time_taken_min","mean"))
    st.plotly_chart(px.bar(x,x="Type_of_vehicle",y="Avg",color="Avg",title="Vehicle efficiency"),use_container_width=True)
with b:
    x=df.groupby("multiple_deliveries",as_index=False).agg(Avg=("Time_taken_min","mean"))
    st.plotly_chart(px.line(x,x="multiple_deliveries",y="Avg",markers=True,title="Multiple deliveries → delivery time"),use_container_width=True)
sample=df[["Distance_km","Time_taken_min","Road_traffic_density","Delivery_person_Ratings"]].dropna()
if len(sample)>5000: sample=sample.sample(5000,random_state=42)
st.plotly_chart(px.scatter(sample,x="Distance_km",y="Time_taken_min",color="Road_traffic_density",hover_data=["Delivery_person_Ratings"],title="Estimated straight-line distance vs delivery time"),use_container_width=True)
st.caption("Distance is a Haversine straight-line estimate from supplied coordinates; it is not road distance."); footer()
