import streamlit as st
import plotly.express as px
from utils.data import load_data, apply_filters
from utils.ui import css, filters, header, footer
st.set_page_config(page_title="Order Patterns | FoodPulse",page_icon="⏱️",layout="wide"); css()
base=load_data(); df=apply_filters(base,filters(base)); header("Order Patterns","Discover when demand concentrates and how delivery duration changes.")
a,b=st.columns(2)
with a:
    x=df.groupby("Order_Hour",as_index=False).agg(Orders=("ID","count")); st.plotly_chart(px.area(x,x="Order_Hour",y="Orders",title="Orders by hour"),use_container_width=True)
with b:
    order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]; x=df.groupby("Order_DayOfWeek",as_index=False).agg(Orders=("ID","count")); x["sort"]=x.Order_DayOfWeek.map({v:i for i,v in enumerate(order)}); x=x.sort_values("sort")
    st.plotly_chart(px.bar(x,x="Order_DayOfWeek",y="Orders",title="Orders by day of week"),use_container_width=True)
a,b=st.columns(2)
with a:
    x=df.groupby("Type_of_order",as_index=False).agg(Orders=("ID","count")); st.plotly_chart(px.pie(x,names="Type_of_order",values="Orders",hole=.55,title="Order type mix"),use_container_width=True)
with b:
    x=df.groupby("Festival",as_index=False).agg(Avg_Time=("Time_taken_min","mean")); st.plotly_chart(px.bar(x,x="Festival",y="Avg_Time",title="Festival vs non-festival delivery time"),use_container_width=True)
footer()
