import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data import load_data, apply_filters
from utils.ui import css, filters, header, footer

st.set_page_config(
    page_title="Area & Rider Intelligence | FoodPulse",
    page_icon="🛵",
    layout="wide",
)
css()

base = load_data()
selected_filters = filters(base)
df = apply_filters(base, selected_filters).copy()

header(
    "Area & Rider Intelligence",
    "Explore demand concentration, delivery delays, busy hours and historical delivery-partner performance.",
)

if df.empty:
    st.warning("No records match the selected filters. Reset or change the filters to continue.")
    st.stop()

# Project-defined delayed threshold: more than 35 minutes.
df["Is_Delayed"] = df["Time_taken_min"] > 35

orders = len(df)
avg_time = df["Time_taken_min"].mean()
delay_rate = df["Is_Delayed"].mean() * 100
avg_distance = df["Distance_km"].mean()

a, b, c, d = st.columns(4)
with a:
    st.metric("Orders in selection", f"{orders:,}")
with b:
    st.metric("Average delivery time", f"{avg_time:.1f} min" if pd.notna(avg_time) else "N/A")
with c:
    st.metric("Delayed share", f"{delay_rate:.1f}%")
with d:
    st.metric("Average estimated distance", f"{avg_distance:.2f} km" if pd.notna(avg_distance) else "N/A")

st.caption(
    "Delay is defined for this academic project as delivery time >35 minutes; "
    "it is not an official Zomato service-level target."
)

st.markdown("---")
st.subheader("📍 Delivery-area intelligence")
st.write(
    "Approximate zones are derived by rounding valid delivery coordinates. "
    "They are analytical clusters, not verified neighbourhoods or restaurant catchment areas."
)

lat_col = "Delivery_location_latitude"
lon_col = "Delivery_location_longitude"

if lat_col in df.columns and lon_col in df.columns:
    geo = df.copy()
    geo = geo[
        geo[lat_col].between(-90, 90)
        & geo[lon_col].between(-180, 180)
        & geo[lat_col].notna()
        & geo[lon_col].notna()
        & (geo[lat_col].abs() > 1)
        & (geo[lon_col].abs() > 1)
    ]

    if not geo.empty:
        geo["Zone_Lat"] = geo[lat_col].round(2)
        geo["Zone_Lon"] = geo[lon_col].round(2)

        zones = (
            geo.groupby(["Zone_Lat", "Zone_Lon"], as_index=False)
            .agg(
                Orders=("ID", "count"),
                Avg_Delivery_Min=("Time_taken_min", "mean"),
                Delayed_Share=("Is_Delayed", "mean"),
                Avg_Distance_km=("Distance_km", "mean"),
            )
        )
        zones["Delayed_Share_Pct"] = zones["Delayed_Share"] * 100
        zones["Approx_Zone"] = zones.apply(
            lambda r: f"{r['Zone_Lat']:.2f}, {r['Zone_Lon']:.2f}", axis=1
        )

        left, right = st.columns([1.25, 1])

        with left:
            st.plotly_chart(
                px.scatter_geo(
                    zones,
                    lat="Zone_Lat",
                    lon="Zone_Lon",
                    size="Orders",
                    color="Delayed_Share_Pct",
                    hover_name="Approx_Zone",
                    hover_data={
                        "Orders": True,
                        "Avg_Delivery_Min": ":.1f",
                        "Delayed_Share_Pct": ":.1f",
                        "Avg_Distance_km": ":.2f",
                        "Zone_Lat": False,
                        "Zone_Lon": False,
                    },
                    color_continuous_scale=["#fed7aa", "#f97316", "#c2410c"],
                    projection="natural earth",
                    title="Approximate delivery-coordinate clusters",
                ),
                use_container_width=True,
            )

        with right:
            st.plotly_chart(
                px.bar(
                    zones.nlargest(12, "Orders").sort_values("Orders"),
                    x="Orders",
                    y="Approx_Zone",
                    orientation="h",
                    color="Delayed_Share_Pct",
                    color_continuous_scale=["#fed7aa", "#f97316", "#c2410c"],
                    title="Highest-volume approximate zones",
                    labels={
                        "Approx_Zone": "Coordinate zone",
                        "Delayed_Share_Pct": "Delayed share (%)",
                    },
                ),
                use_container_width=True,
            )

        display_zones = zones.sort_values("Orders", ascending=False).head(20).copy()
        display_zones["Avg_Delivery_Min"] = display_zones["Avg_Delivery_Min"].round(1)
        display_zones["Delayed_Share_Pct"] = display_zones["Delayed_Share_Pct"].round(1)
        display_zones["Avg_Distance_km"] = display_zones["Avg_Distance_km"].round(2)

        st.markdown("**Top coordinate clusters**")
        st.dataframe(
            display_zones[
                ["Approx_Zone", "Orders", "Avg_Delivery_Min", "Delayed_Share_Pct", "Avg_Distance_km"]
            ],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("No valid delivery coordinates are available for the current filters.")
else:
    st.info("Delivery-coordinate fields are not available in this dataset.")

st.markdown("---")
st.subheader("⏰ Demand and delay patterns")

if "Order_Hour" in df.columns:
    hourly = (
        df.dropna(subset=["Order_Hour"])
        .groupby("Order_Hour", as_index=False)
        .agg(
            Orders=("ID", "count"),
            Avg_Delivery_Min=("Time_taken_min", "mean"),
            Delayed_Share=("Is_Delayed", "mean"),
        )
    )
    hourly["Delayed_Share_Pct"] = hourly["Delayed_Share"] * 100

    h1, h2 = st.columns(2)
    with h1:
        st.plotly_chart(
            px.bar(
                hourly,
                x="Order_Hour",
                y="Orders",
                title="Recorded order volume by hour",
                labels={"Order_Hour": "Order hour", "Orders": "Orders"},
                color_discrete_sequence=["#f45b35"],
            ),
            use_container_width=True,
        )
    with h2:
        st.plotly_chart(
            px.line(
                hourly,
                x="Order_Hour",
                y="Delayed_Share_Pct",
                markers=True,
                title="Delayed share by order hour",
                labels={"Order_Hour": "Order hour", "Delayed_Share_Pct": "Delayed share (%)"},
            ),
            use_container_width=True,
        )

    if not hourly.empty:
        peak = hourly.loc[hourly["Orders"].idxmax()]
        st.info(
            f"Highest observed order volume occurs at hour {int(peak['Order_Hour']):02d}:00 "
            f"({int(peak['Orders']):,} records in the current selection). "
            "This is historical demand, not a live forecast."
        )
else:
    st.info("Order-hour information is unavailable.")

st.markdown("---")
st.subheader("🛵 Historical delivery-partner and vehicle performance")

partner_col = "Delivery_person_ID"

if partner_col in df.columns:
    partners = (
        df.dropna(subset=[partner_col])
        .groupby(partner_col, as_index=False)
        .agg(
            Deliveries=("ID", "count"),
            Avg_Delivery_Min=("Time_taken_min", "mean"),
            Delayed_Share=("Is_Delayed", "mean"),
            Avg_Rating=("Delivery_person_Ratings", "mean"),
        )
    )
    partners["Delayed_Share_Pct"] = partners["Delayed_Share"] * 100

    p1, p2 = st.columns(2)
    with p1:
        st.plotly_chart(
            px.scatter(
                partners,
                x="Deliveries",
                y="Avg_Delivery_Min",
                size="Delayed_Share_Pct",
                color="Delayed_Share_Pct",
                hover_name=partner_col,
                title="Recorded delivery workload vs average time",
                labels={
                    "Deliveries": "Deliveries in selected records",
                    "Avg_Delivery_Min": "Average delivery time (min)",
                    "Delayed_Share_Pct": "Delayed share (%)",
                },
                color_continuous_scale=["#fed7aa", "#f97316", "#c2410c"],
            ),
            use_container_width=True,
        )
    with p2:
        st.caption(
            "Partner IDs are pseudonymous dataset identifiers. These records do not reveal "
            "whether a partner is currently online, available, or assigned to a live order."
        )
        partner_table = partners.sort_values("Deliveries", ascending=False).head(20).copy()
        for col in ["Avg_Delivery_Min", "Delayed_Share_Pct", "Avg_Rating"]:
            partner_table[col] = partner_table[col].round(2)
        st.dataframe(partner_table, use_container_width=True, hide_index=True)

else:
    st.info("Delivery-partner identifier is unavailable in this dataset.")

if "Type_of_vehicle" in df.columns:
    vehicle = (
        df.groupby("Type_of_vehicle", as_index=False)
        .agg(
            Deliveries=("ID", "count"),
            Avg_Delivery_Min=("Time_taken_min", "mean"),
            Delayed_Share=("Is_Delayed", "mean"),
        )
    )
    vehicle["Delayed_Share_Pct"] = vehicle["Delayed_Share"] * 100

    st.plotly_chart(
        px.bar(
            vehicle,
            x="Type_of_vehicle",
            y="Delayed_Share_Pct",
            color="Avg_Delivery_Min",
            text="Deliveries",
            title="Historical delayed share by recorded vehicle type",
            labels={
                "Type_of_vehicle": "Vehicle type",
                "Delayed_Share_Pct": "Delayed share (%)",
                "Avg_Delivery_Min": "Average delivery time (min)",
            },
            color_continuous_scale=["#fed7aa", "#f97316", "#c2410c"],
        ),
        use_container_width=True,
    )

st.markdown("---")
st.subheader("How to interpret this page")
st.markdown("""
- **City** is a dataset category (`Metropolitian`, `Urban`, or `Semi-Urban`), not a named city.
- **Zones** are approximate clusters of recorded delivery coordinates, not named neighbourhoods.
- **Delayed share** uses the project's threshold of more than 35 minutes.
- **Partner and vehicle results** describe historical records, not live rider availability or causal performance.
- The dataset does not include restaurant names, exact food-item names, or a live rider roster.
""")

footer()
