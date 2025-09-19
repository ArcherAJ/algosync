from common_imports import *
import folium
from folium import plugins
import streamlit_folium as st_folium

def create_map():
    """Create a simple Kochi Metro map"""
    st.header("🗺️ Kochi Metro Map")
    
    # Kochi Metro station coordinates
    stations = {
        "Aluva": (10.1076, 76.3516),
        "Pulinchodu": (10.1023, 76.3589),
        "Companypady": (10.0967, 76.3662),
        "Ambattukavu": (10.0911, 76.3735),
        "Muttom": (10.0855, 76.3808),
        "Kalamassery": (10.0799, 76.3881),
        "CUSAT": (10.0743, 76.3954),
        "Pathadipalam": (10.0687, 76.4027),
        "Edapally": (10.0631, 76.4100),
        "Changampuzha Park": (10.0575, 76.4173),
        "Palarivattom": (10.0519, 76.4246),
        "JLN Stadium": (10.0463, 76.4319),
        "Kaloor": (10.0407, 76.4392),
        "Lissie": (10.0351, 76.4465),
        "MG Road": (10.0295, 76.4538),
        "Maharaja's College": (10.0239, 76.4611),
        "Ernakulam South": (10.0183, 76.4684),
        "Kadavanthra": (10.0127, 76.4757),
        "Elamkulam": (10.0071, 76.4830),
        "Vytilla": (10.0015, 76.4903),
        "Thaikoodam": (9.9959, 76.4976),
        "Petta": (9.9903, 76.5049),
        "Vadakkekotta": (9.9847, 76.5122),
        "SN Junction": (9.9791, 76.5195),
        "Kakkanad": (9.9735, 76.5268),
        "Thrippunithura": (9.9450, 76.3500)
    }
    
    # Create map centered on Kochi Metro
    center_lat, center_lon = 10.0, 76.3
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add station markers
    for station_name, (lat, lon) in stations.items():
        folium.Marker(
            [lat, lon],
            popup=f"<b>{station_name}</b><br>Metro Station",
            icon=folium.Icon(color='blue', icon='train', prefix='fa'),
            tooltip=station_name
        ).add_to(m)
    
    # Add route lines
    aluva_kakkanad = [
        "Aluva", "Pulinchodu", "Companypady", "Ambattukavu", "Muttom", 
        "Kalamassery", "CUSAT", "Pathadipalam", "Edapally", "Changampuzha Park", 
        "Palarivattom", "JLN Stadium", "Kaloor", "Lissie", "MG Road", 
        "Maharaja's College", "Ernakulam South", "Kadavanthra", "Elamkulam", 
        "Vytilla", "Thaikoodam", "Petta", "Vadakkekotta", "SN Junction", "Kakkanad"
    ]
    
    # Create route line
    route_coords = []
    for station in aluva_kakkanad:
        if station in stations:
            lat, lon = stations[station]
            route_coords.append([lat, lon])
    
    if route_coords:
        folium.PolyLine(
            route_coords,
            color='red',
            weight=4,
            opacity=0.7,
            popup="<b>Aluva-Kakkanad Route</b>"
        ).add_to(m)
    
    # Display map
    st_folium.st_folium(m, width=1000, height=600, returned_objects=[])
    
    # Station information
    st.subheader("🚆 Station Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Total Stations:** 26")
        st.write("**Main Route:** Aluva-Kakkanad (25 stations)")
        st.write("**Extension Route:** Thrippunithura-Vytilla (6 stations)")
    
    with col2:
        st.write("**Total Length:** ~25 km")
        st.write("**Operational Hours:** 6:00 AM - 10:00 PM")
        st.write("**Frequency:** 3-5 minutes (peak), 8-10 minutes (off-peak)")
