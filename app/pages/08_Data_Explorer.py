import streamlit as st
import pandas as pd
from utils.data import load_data, apply_filters
from utils.ui import css, filters, header, footer
st.set_page_config(page_title="Data Explorer | FoodPulse",page_icon="🔎",layout="wide"); css()
base=load_data(); df=apply_filters(base,filters(base)); header("Data Explorer","Inspect the analytical data behind the FoodPulse dashboard.")
a,b,c=st.columns(3); a.metric("Filtered rows",f"{len(df):,}"); b.metric("Columns",str(len(df.columns))); c.metric("Missing cells",f"{int(df.isna().sum().sum()):,}")
profile=pd.DataFrame({"Column":df.columns,"Type":[str(df[c].dtype) for c in df.columns],"Missing":[int(df[c].isna().sum()) for c in df.columns],"Unique":[int(df[c].nunique(dropna=True)) for c in df.columns]})
st.markdown("### Column profile"); st.dataframe(profile,use_container_width=True,hide_index=True)
st.markdown("### Sample records"); cols=st.multiselect("Columns",df.columns.tolist(),default=df.columns[:10].tolist()); st.dataframe(df[cols].head(100),use_container_width=True,hide_index=True)
footer()
