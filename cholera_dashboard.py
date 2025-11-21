import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from branca.element import Template, MacroElement
from streamlit_folium import st_folium

st.set_page_config(page_title="Cholera Death Map", layout="wide")
st.title("Cholera Death Dashboard")

# Load CSV data
gdf_deaths = pd.read_csv("Cholera_Deaths.csv")
gdf_pumps = pd.read_csv("Pumps.csv")

# Summary statistics
total_deaths = len(gdf_deaths)
death_counts = gdf_deaths.groupby(["X","Y"]).size()
max_death_same_location = death_counts.max()

st.metric("Total Cholera Deaths", total_deaths)
st.metric("Maximum Deaths at One Location", int(max_death_same_location))

# Create map
center_lat = gdf_deaths["Y"].mean()
center_lon = gdf_deaths["X"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=16)

# Add cholera deaths
deaths_layer = folium.FeatureGroup(name="Cholera Deaths")
for _, row in gdf_deaths.iterrows():
    folium.CircleMarker(
        location=[row["Y"], row["X"]],
        radius=3,
        color="red",
        fill=True,
        fill_opacity=0.8
    ).add_to(deaths_layer)
deaths_layer.add_to(m)

# Add water pumps
pumps_layer = folium.FeatureGroup(name="Water Pumps")
for _, row in gdf_pumps.iterrows():
    folium.Marker(
        location=[row["Y"], row["X"]],
        popup="Water Pump",
        icon=folium.Icon(color="blue", icon="tint", prefix="fa")
    ).add_to(pumps_layer)
pumps_layer.add_to(m)

# Layer control
folium.LayerControl().add_to(m)

# Title & legend
template = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    z-index:9999;
    background-color:white;
    padding:10px;
    border:2px solid grey;
    border-radius:5px;
    font-size:16px;
    font-weight:bold;
    ">
    CHOLERA DEATH MAP
</div>
<div style="
    position: fixed;
    bottom: 50px;
    left: 10px;
    z-index:9999;
    background-color:white;
    padding:10px;
    border:2px solid grey;
    border-radius:5px;
    font-size:14px;
    ">
    <i class="fa fa-circle" style="color:red;"></i> Cholera Deaths<br>
    <i class="fa fa-tint" style="color:blue;"></i> Water Pumps
</div>
{% endmacro %}
"""
macro = MacroElement()
macro._template = Template(template)
m.get_root().add_child(macro)

# Display map
st.subheader("Interactive Cholera Map")
st_folium(m, width=1000, height=600)
