import io, re, requests
import numpy as np
import pandas as pd
import streamlit as st

DATA_URL = "https://raw.githubusercontent.com/Varunnagar/Zomato-Food-Delivery-Analysis/main/Zomato%20Dataset.csv"

@st.cache_data(ttl=3600, show_spinner="Loading FoodPulse data...")
def load_data():
    r = requests.get(DATA_URL, timeout=60)
    r.raise_for_status()
    df = pd.read_csv(io.BytesIO(r.content))
    if len(df) != 45584 or len(df.columns) != 20:
        raise ValueError(f"Dataset verification failed: expected 45,584 x 20, got {len(df)} x {len(df.columns)}.")
    df.columns = [re.sub(r"_+", "_", re.sub(r"[^A-Za-z0-9]+", "_", c.strip())).strip("_") for c in df.columns]
    numeric = ["Delivery_person_Age","Delivery_person_Ratings","Restaurant_latitude","Restaurant_longitude",
               "Delivery_location_latitude","Delivery_location_longitude","Vehicle_condition",
               "multiple_deliveries","Time_taken_min"]
    for c in numeric:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["Order_Date_parsed"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y", errors="coerce")
    df["Order_Month"] = df["Order_Date_parsed"].dt.month
    df["Order_DayOfWeek"] = df["Order_Date_parsed"].dt.day_name()
    df["Order_Hour"] = pd.to_datetime(df["Time_Orderd"], format="%H:%M", errors="coerce").dt.hour
    for c in ["Weather_conditions","Road_traffic_density","Type_of_order","Type_of_vehicle","Festival","City"]:
        df[c] = df[c].astype("string").str.strip().replace({"NaN": pd.NA, "nan": pd.NA})
    R = 6371.0
    lat1, lon1 = np.radians(df["Restaurant_latitude"]), np.radians(df["Restaurant_longitude"])
    lat2, lon2 = np.radians(df["Delivery_location_latitude"]), np.radians(df["Delivery_location_longitude"])
    a = np.sin((lat2-lat1)/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin((lon2-lon1)/2)**2
    df["Distance_km"] = 2 * R * np.arcsin(np.sqrt(a))
    df["Delivery_Speed_kmph"] = df["Distance_km"] / (df["Time_taken_min"]/60)
    df["Delivery_Performance"] = pd.cut(df["Time_taken_min"], bins=[-np.inf,25,35,np.inf],
                                        labels=["Fast","Standard","Delayed"]).astype("string")
    return df

def apply_filters(df, filters):
    out = df
    for key, col in [("city","City"),("traffic","Road_traffic_density"),("weather","Weather_conditions"),
                     ("vehicle","Type_of_vehicle"),("performance","Delivery_Performance")]:
        if filters[key] != "All":
            out = out[out[col] == filters[key]]
    return out

def kpis(df):
    return {
        "orders": len(df),
        "time": df["Time_taken_min"].mean(),
        "rating": df["Delivery_person_Ratings"].mean(),
        "distance": df["Distance_km"].mean(),
        "speed": df["Delivery_Speed_kmph"].mean(),
    }

def source_box():
    return '''<div class="source-box"><b>Dataset provenance</b><br>
    Public Zomato Food Delivery Operations dataset · 45,584 records × 20 raw attributes.
    Source: <a href="https://github.com/Varunnagar/Zomato-Food-Delivery-Analysis" target="_blank">
    Varunnagar/Zomato-Food-Delivery-Analysis</a>.
    This is a publicly distributed dataset, not an official internal Zomato database.</div>'''
