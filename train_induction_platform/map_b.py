import streamlit as st
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go


class KochiMetroMap:
    def __init__(self):
        # -------------------------------
        # Metro Station Coordinates
        self.stations = {
            "Aluva": [10.1096, 76.3516],
            "Pulinchodu": [10.09503, 76.34658],
            "Companypady": [10.087293, 76.34284],
            "Ambattukavu": [10.079372, 76.339004],
            "Muttom": [10.072701, 76.33375],
            "Kalamassery": [10.0481, 76.3097],
            "Cochin University": [10.046879, 76.318377],
            "Pathadipalam": [10.035948, 76.314371],
            "Edapally": [10.0274, 76.3080],
            "Changampuzha Park": [10.01488, 76.30232],
            "Palarivattom": [9.998480, 76.311935],
            "JLN Stadium": [9.9973, 76.3010],
            "Kaloor": [9.99709, 76.302815],
            "Town Hall": [9.991247, 76.288035],
            "M.G. Road": [9.971295, 76.299317],
            "Maharajas": [9.973487, 76.285015],
            "Vyttila": [9.9630, 76.3126],
        }

        self.station_names = list(self.stations.keys())
        self.route_coords = list(self.stations.values())

        # -------------------------------
        # Station Info
        self.station_info = {
            "Aluva": {
                "Tourist Attractions": "Near Periyar River, Aluva Market",
                "Connectivity": "12.3 km → Kochi Airport; Feeder shuttle ₹50 every 40 mins (5 am – 11 pm)",
                "Facilities": "Beside NH 544, Aluva Bypass; KSRTC Bus Station 1.5 km"
            },
            "Pulinchodu": {
                "Tourist Attractions": "Local area markets",
                "Connectivity": "Connected to Aluva–Kochi corridor",
                "Facilities": "Basic transport access nearby"
            },
            "Companypady": {
                "Tourist Attractions": "Residential and local shopping hub",
                "Connectivity": "Accessible via NH 544",
                "Facilities": "Bus stops nearby"
            },
            "Ambattukavu": {
                "Tourist Attractions": "Residential locality",
                "Connectivity": "Metro access point between Aluva and Kalamassery",
                "Facilities": "Nearby shops and housing areas"
            },
            "Muttom": {
                "Tourist Attractions": "Industrial and metro yard area",
                "Connectivity": "Part of Aluva–Kochi metro stretch",
                "Facilities": "Metro operational hub"
            },
            "Kalamassery": {
                "Tourist Attractions": "Kalamassery industrial hub",
                "Connectivity": "Close to NH 544",
                "Facilities": "Educational institutions, industries nearby"
            },
            "Cochin University": {
                "Tourist Attractions": "CUSAT campus",
                "Connectivity": "Well connected by metro",
                "Facilities": "Student hub, eateries, academic institutions"
            },
            "Pathadipalam": {
                "Tourist Attractions": "Local residential area",
                "Connectivity": "Metro access to Edapally",
                "Facilities": "Hospitals and city access nearby"
            },
            "Edapally": {
                "Tourist Attractions": "Lulu Mall, St. George Forane Church, Jawaharlal Nehru Stadium",
                "Connectivity": "~12.3 km to Airport; ~5–6 km to Ernakulam Town Jn",
                "Facilities": "Major shopping & business hub; hospitals nearby"
            },
            "Changampuzha Park": {
                "Tourist Attractions": "Changampuzha Park (cultural centre)",
                "Connectivity": "Close to Edapally metro",
                "Facilities": "Cultural events, park access"
            },
            "Palarivattom": {
                "Tourist Attractions": "Commercial hub, restaurants, hotels",
                "Connectivity": "Metro & bus connectivity",
                "Facilities": "Shops, eateries, traffic junction"
            },
            "JLN Stadium": {
                "Tourist Attractions": "Jawaharlal Nehru International Stadium",
                "Connectivity": "Metro connectivity via Kaloor & Edapally",
                "Facilities": "Sports hub, events venue"
            },
            "Kaloor": {
                "Tourist Attractions": "Kaloor Bus Stand area",
                "Connectivity": "Connected to city buses",
                "Facilities": "Commercial hub, hotels, shops"
            },
            "Town Hall": {
                "Tourist Attractions": "Town Hall, near commercial hub",
                "Connectivity": "Metro link to MG Road",
                "Facilities": "Shops, offices nearby"
            },
            "M.G. Road": {
                "Tourist Attractions": "Rainbow Hanging Bridge, Mangalavanam Bird Sanctuary, commercial hub",
                "Connectivity": "~2.5 km to Ernakulam Junction railway station",
                "Facilities": "Connected to city bus routes; shopping & offices"
            },
            "Maharajas": {
                "Tourist Attractions": "Maharaja’s College Grounds, Public Library",
                "Connectivity": "800 m to Ernakulam Jn (10–15 min walk)",
                "Facilities": "General Hospital (470 m), Krishna Hospital (190 m), ATMs, hotels, limited parking"
            },
            "Vyttila": {
                "Tourist Attractions": "Vyttila Mobility Hub, backwaters access",
                "Connectivity": "~5 km to Ernakulam Jn; linked to bus + water metro",
                "Facilities": "Biggest transit hub in Kochi (bus + metro + water metro)"
            }
        }

    def render(self):
        # -------------------------------
        # Streamlit Layout
        st.set_page_config(layout="wide")
        st.title("🚇 Kochi Metro Interactive Dashboard")

        # Two columns layout
        col1, col2 = st.columns([1.2, 1])

        # -------------------------------
        # Left: Folium Map
        with col1:
            st.markdown("### 🗺️ Metro Route Map")

            m = folium.Map(location=[9.9312, 76.2673], zoom_start=12, tiles="CartoDB positron")
            for i, (station_name, coords) in enumerate(self.stations.items()):
                folium.Marker(
                    location=coords,
                    popup=f"<b>{station_name}</b>",
                    tooltip=f"Station {i+1}: {station_name}",
                    icon=folium.Icon(color="green", icon="train", prefix="fa")
                ).add_to(m)

            folium.PolyLine(
                locations=self.route_coords,
                color="blue",
                weight=5,
                opacity=0.7,
                tooltip="Metro Route"
            ).add_to(m)

            st_folium(m, width=650, height=700)

        # -------------------------------
        # Right: Vertical Timeline + Dropdowns
        with col2:
            st.markdown("### 🕘 Metro Station Timeline (Vertical)")

            y_values = list(range(len(self.station_names)))[::-1]  # reverse for vertical top to bottom
            x_values = [0] * len(self.station_names)

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='markers+text',
                marker=dict(color='green', size=14),
                text=self.station_names,
                textposition='middle right',
                hoverinfo='text'
            ))

            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines',
                line=dict(color='blue', width=3),
                hoverinfo='skip'
            ))

            fig.update_layout(
                showlegend=False,
                height=750,
                margin=dict(l=20, r=40, t=20, b=20),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )

            st.plotly_chart(fig, use_container_width=True)

            # Interactive dropdowns
            st.markdown("### 📂 Station Details")
            for station in self.station_names:
                with st.expander(f"📍 {station}"):
                    info = self.station_info.get(station, {})
                    if info:
                        st.write(f"**🏙️ Tourist Attractions:** {info.get('Tourist Attractions', 'N/A')}")
                        st.write(f"**🛣️ Connectivity:** {info.get('Connectivity', 'N/A')}")
                        st.write(f"**💡 Facilities:** {info.get('Facilities', 'N/A')}")
                    else:
                        st.info("Details not available for this station.")
