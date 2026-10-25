import streamlit as st
from utils.data import load_data
from utils.ui import css, filters, header, footer
st.set_page_config(page_title="Spark Lab | FoodPulse",page_icon="⚡",layout="wide"); css()
df=load_data(); filters(df); header("Spark Lab","A presentation-friendly view of how the Colab analysis maps to Apache Spark.")
st.markdown("### Architecture")
st.code("Public CSV\n   ↓\nSparkSession\n   ↓\nRaw DataFrame\n   ↓\nCleaning + Feature Engineering\n   ├── Haversine distance\n   └── Performance bands\n   ↓\nRDD + DataFrame + Spark SQL\n   ↓\nFoodPulse analytical outputs\n   ↓\nStreamlit website",language="text")
a,b,c=st.columns(3)
with a:
    st.markdown("#### 🔹 RDD"); st.code('city_rdd = (df.select("City","Time_taken_min").dropna().rdd.map(lambda r: (r["City"], (1, float(r["Time_taken_min"])))).reduceByKey(lambda a,b: (a[0]+b[0], a[1]+b[1])))',language="python")
with b:
    st.markdown("#### 🔹 DataFrame"); st.code('df.groupBy("City").agg(F.count("*").alias("Orders"), F.avg("Time_taken_min"))',language="python")
with c:
    st.markdown("#### 🔹 Spark SQL"); st.code('SELECT City, COUNT(*) AS orders, AVG(Time_taken_min) FROM food_delivery GROUP BY City ORDER BY orders DESC',language="sql")
x,y,z=st.columns(3); x.metric("Rows",f"{len(df):,}"); y.metric("Raw columns","20"); z.metric("Derived columns",str(len(df.columns)-20))
st.info("The Colab notebook is the Spark computation/lab evidence layer. This website is the interactive presentation layer using the same source and derived analytical concepts.")
footer()
