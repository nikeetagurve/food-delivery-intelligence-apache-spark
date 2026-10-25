import streamlit as st
import plotly.express as px
from utils.data import load_data, apply_filters, kpis, source_box
from utils.ui import css, filters, metric, footer

st.set_page_config(page_title="FoodPulse", page_icon="🍔", layout="wide")
css()
df = load_data()
fdf = apply_filters(df, filters(df))
k = kpis(fdf)

st.markdown('<div class="hero"><div class="badge">⚡ APACHE SPARK · FOOD DELIVERY INTELLIGENCE</div><h1>FOOD<span>PULSE</span></h1><p>Operational intelligence for food delivery — interactive analytics built from the public Zomato food-delivery dataset.</p></div>', unsafe_allow_html=True)

c = st.columns(4)
metric(c[0],"ORDERS",f"{k['orders']:,}","Selected records")
metric(c[1],"AVG DELIVERY",f"{k['time']:.1f} min","Delivery duration")
metric(c[2],"AVG RATING",f"{k['rating']:.2f} / 5","Partner rating")
metric(c[3],"AVG DISTANCE",f"{k['distance']:.1f} km","Haversine estimate")

a,b = st.columns([1.4,1])
with a:
    daily=fdf.groupby("Order_Date_parsed",as_index=False).agg(Orders=("ID","count"))
    fig=px.area(daily,x="Order_Date_parsed",y="Orders",title="Order volume over time")
    fig.update_layout(height=360,margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig,use_container_width=True)
with b:
    p=fdf["Delivery_Performance"].value_counts().reset_index()
    p.columns=["Performance","Orders"]
    fig=px.pie(p,names="Performance",values="Orders",hole=.62,title="Delivery performance mix")
    fig.update_layout(height=360,margin=dict(l=10,r=10,t=55,b=10))
    st.plotly_chart(fig,use_container_width=True)

st.markdown("### Control room signals")
city=fdf.groupby("City",as_index=False).agg(Orders=("ID","count"),Avg=("Time_taken_min","mean"))
traffic=fdf.groupby("Road_traffic_density",as_index=False).agg(Avg=("Time_taken_min","mean"))
slow=city.loc[city.Avg.idxmax()]; busy=city.loc[city.Orders.idxmax()]; high=traffic.loc[traffic.Avg.idxmax()]
cards=[("📍","Slowest city",str(slow.City),f"{slow.Avg:.1f} min average"),
       ("🔥","Highest volume",str(busy.City),f"{int(busy.Orders):,} orders"),
       ("🚦","Highest-delay traffic",str(high.Road_traffic_density),f"{high.Avg:.1f} min average")]
cc=st.columns(3)
for col,(icon,title,val,desc) in zip(cc,cards):
    col.markdown(f'<div class="card"><div class="icon">{icon}</div><b>{title}</b><h3>{val}</h3><p>{desc}</p></div>',unsafe_allow_html=True)

st.markdown(source_box(),unsafe_allow_html=True)
footer()
