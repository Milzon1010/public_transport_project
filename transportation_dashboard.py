import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static

st.set_page_config(page_title="Jakarta Transportation Analytics", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv('jakarta_traffic_data.csv')
    return df

df = load_data()

# --- Title ---
st.title("🚦 Jakarta Transportation Analytics (June 2025)")

# --- Statistik Umum (3 Kolom) ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Records", f"{len(df):,}")
with col2:
    st.metric("Jalur Terpadat", df['route'].mode()[0])
with col3:
    st.metric("Jam Tersibuk", f"{df['hour'].mode()[0]}:00")

st.divider()

# --- Heatmap Section (langsung terlihat tanpa scroll) ---
st.header("Peta Lalu Lintas Jakarta (Heatmap)")

heat_data = df.groupby(['lat', 'lon']).agg({'traffic_volume': 'sum'}).reset_index()
m = folium.Map(location=[-6.2, 106.816666], zoom_start=13, control_scale=True)
HeatMap(
    data=heat_data[['lat', 'lon', 'traffic_volume']].values,
    min_opacity=0.4,
    radius=18,
    blur=18,
    max_zoom=1,
).add_to(m)
folium_static(m, width=1100, height=520)

# --- Statistik Detail (dalam Expander agar tidak penuh layar) ---
with st.expander("Lihat Top 5 Jalur Terpadat"):
    top_routes = df.groupby('route')['traffic_volume'].sum().sort_values(ascending=False).head(5)
    st.dataframe(top_routes.reset_index().rename(columns={'traffic_volume': 'Total Volume'}))

with st.expander("Lihat Jalur Tersibuk per Jam (Sample)"):
    for jam in sorted(df['hour'].unique())[:3]:
        top_r = df[df['hour'] == jam].groupby('route')['traffic_volume'].sum().sort_values(ascending=False).head(1)
        route_name = top_r.index[0]
        route_vol = top_r.iloc[0]
        st.write(f"Jam {jam:02d}: {route_name} – {route_vol} kendaraan")

st.caption("By Milzon, built with Python, pandas, folium, streamlit.")
