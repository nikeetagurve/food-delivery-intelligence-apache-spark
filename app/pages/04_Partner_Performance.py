import streamlit as st
import plotly.express as px
from utils.data import load_data, apply_filters
from utils.ui import css, filters, header, footer
st.set_page_config(page_title="Partner Performance | FoodPulse",page_icon="⭐",layout="wide"); css()
base=load_data(); df=apply_filters(base,filters(base)); header("Partner Performance","Understand ratings, workload and operating conditions for delivery partners.")
a,b=st.columns(2)
with a:
    x=df.groupby("Delivery_person_Ratings",as_index=False).agg(Orders=("ID","count"))
    st.plotly_chart(px.bar(x,x="Delivery_person_Ratings",y="Orders",title="Order volume by partner rating"),use_container_width=True)
with b:
    x=df.groupby("Delivery_person_Age",as_index=False).agg(Orders=("ID","count"),Avg_Time=("Time_taken_min","mean"))
    st.plotly_chart(px.scatter(x,x="Delivery_person_Age",y="Avg_Time",size="Orders",title="Partner age vs average delivery time"),use_container_width=True)
top=df.groupby("Delivery_person_ID",as_index=False).agg(Orders=("ID","count"),Avg_Rating=("Delivery_person_Ratings","mean"),Avg_Time=("Time_taken_min","mean"),Avg_Distance=("Distance_km","mean"))
top=top[top.Orders>=10].sort_values(["Avg_Rating","Orders"],ascending=[False,False]).head(15).round(2)
st.markdown("### Highest-rated partner groups"); st.dataframe(top,use_container_width=True,hide_index=True)
st.caption("Partner IDs are pseudonymous identifiers in the source dataset; this page does not identify real individuals."); footer()
