import streamlit as st
import plotly.express as px
from utils.data import load_data, apply_filters, kpis
from utils.ui import css, filters, header, metric, footer
st.set_page_config(page_title="Overview | FoodPulse",page_icon="📊",layout="wide"); css()
base=load_data(); df=apply_filters(base,filters(base)); k=kpis(df)
header("Overview","A command-center view of volume, speed, service quality and geography.")
c=st.columns(5)
metric(c[0],"ORDERS",f"{k['orders']:,}","Selected view"); metric(c[1],"AVG TIME",f"{k['time']:.1f} min","Delivery")
metric(c[2],"RATING",f"{k['rating']:.2f}","Partner rating"); metric(c[3],"DISTANCE",f"{k['distance']:.1f} km","Estimated")
metric(c[4],"SPEED",f"{k['speed']:.1f} km/h","Estimated")
a,b=st.columns(2)
with a:
    x=df.groupby("City",as_index=False).agg(Orders=("ID","count")).sort_values("Orders")
    st.plotly_chart(px.bar(x,x="Orders",y="City",orientation="h",title="Order volume by city"),use_container_width=True)
with b:
    x=df.groupby("Delivery_Performance",as_index=False).agg(Avg_Time=("Time_taken_min","mean"))
    st.plotly_chart(px.bar(x,x="Delivery_Performance",y="Avg_Time",color="Delivery_Performance",title="Average time by performance band"),use_container_width=True)
x=df.groupby("Order_Month",as_index=False).agg(Orders=("ID","count"))
fig=px.line(x,x="Order_Month",y="Orders",markers=True,title="Monthly order volume"); fig.update_xaxes(dtick=1)
st.plotly_chart(fig,use_container_width=True); footer()
