import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap

st.set_page_config(page_title="Jakarta Transportation Analytics", layout="wide")

# Header dan logo
st.markdown("""
    <div style='display:flex; align-items:center; gap:14px; margin-bottom:0.2em'>
        <img src='https://i.ibb.co/tbpD8LP/qg-logo.png' height='36' style='border-radius:5px; margin-right:6px'>
        <span style='font-size:2.1em; font-weight:700; letter-spacing:1px;'>Jakarta Transportation Analytics <span style='font-size:0.68em; font-weight:400;'>(June 2025)</span></span>
    </div>
    <div style='color: #BBB; font-size:0.96em; margin-bottom:0.8em;'>
        By <b>Milzon</b> &middot; With Coach Ramin &middot; Built with Python, pandas, folium, streamlit
    </div>
""", unsafe_allow_html=True)

# --- Load Data ---
df = pd.read_csv("jakarta_traffic_data.csv")

col_map, col_stats = st.columns([2.1, 1.6], gap="large")

with col_map:
    st.markdown("<div style='font-size:1.25em; font-weight:600; margin-bottom:0.5em;'>Heatmap Lalu Lintas</div>", unsafe_allow_html=True)
    heat_data = df.groupby(['lat', 'lon']).agg({'traffic_volume': 'sum'}).reset_index()
    m = folium.Map(location=[-6.2, 106.816666], zoom_start=12, control_scale=True, tiles="cartodbpositron")
    HeatMap(
        data=heat_data[['lat', 'lon', 'traffic_volume']].values,
        min_opacity=0.4, radius=15, blur=18, max_zoom=1,
    ).add_to(m)
    folium_static(m, width=480, height=350)

with col_stats:
    st.markdown("<div style='font-size:1.4em; font-weight:600; margin-bottom:0.1em;'>Statistik Singkat</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='font-size:1.12em;line-height:1.6em;'>
            <b>Jalur Terpadat:</b> {df['route'].mode()[0]}<br>
            <b>Jam Tersibuk:</b> {df['hour'].mode()[0]}:00<br>
            <b>Total Records:</b> {len(df):,}<br>
            <b>Top 5 Jalur Terpadat:</b>
            <ol style='margin:0 0 0 22px;padding:0'>
            {"".join([f"<li>{r} : {v:,} kendaraan</li>" for r,v in df.groupby('route')['traffic_volume'].sum().sort_values(ascending=False).head(5).items()])}
            </ol>
        </div>
    """, unsafe_allow_html=True)
