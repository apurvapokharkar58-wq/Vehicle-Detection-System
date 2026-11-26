
import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=5000, key="dashboard_refresh")
import pandas as pd
import os

st.set_page_config(
    page_title="Vehicle Detection Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Vehicle Detection System")
st.subheader("Live Vehicle Analytics Dashboard")

# Load vehicle report
if os.path.exists("vehicle_report.csv"):
    df = pd.read_csv("vehicle_report.csv")

    vehicle_data = df[df["Vehicle Type"] != "Total"]
    total = int(vehicle_data["Detected Count"].sum())

    st.metric("Total Vehicles Detected", total)

    col1, col2, col3, col4 = st.columns(4)

    for col, name in zip(
        [col1, col2, col3, col4],
        ["Car", "Bike", "Bus", "Truck"]
    ):
        count = vehicle_data.loc[
            vehicle_data["Vehicle Type"] == name,
            "Detected Count"
        ].sum()

        col.metric(name, int(count))

    st.subheader("Vehicle Count Analysis")

    chart_data = vehicle_data.set_index("Vehicle Type")["Detected Count"]
    st.bar_chart(chart_data)

    st.subheader("Vehicle Detection Report")
    st.dataframe(vehicle_data, use_container_width=True)

else:
    st.warning("vehicle_report.csv not found. Run vehicle detection first.")

# Display processed video
st.subheader("Vehicle Tracking Output")

if os.path.exists("tracking_output_web.mp4"):
    st.video("tracking_output_web.mp4")
else:
    st.info("Tracking video will appear here after detection is completed.")
