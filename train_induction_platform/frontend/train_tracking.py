from common_imports import *
from train_tracker import TrainTracker, TrainStatus, CollisionDetector, TimetableAnalyzer
import folium
from folium import plugins
import streamlit_folium as st_folium

def generate_timetable_data():
    """Generate comprehensive timetable data for train tracking"""
    
    # Station coordinates for Kochi Metro
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
    
    # Routes
    routes = {
        "Aluva-Kakkanad": ["Aluva", "Pulinchodu", "Companypady", "Ambattukavu", "Muttom", 
                           "Kalamassery", "CUSAT", "Pathadipalam", "Edapally", "Changampuzha Park", 
                           "Palarivattom", "JLN Stadium", "Kaloor", "Lissie", "MG Road", 
                           "Maharaja's College", "Ernakulam South", "Kadavanthra", "Elamkulam", 
                           "Vytilla", "Thaikoodam", "Petta", "Vadakkekotta", "SN Junction", "Kakkanad"],
        "Thrippunithura-Vytilla": ["Thrippunithura", "Vadakkekotta", "Petta", "SN Junction", "Kakkanad", "Kalamassery"]
    }
    
    # Generate timetable for 12 hours (6 AM to 6 PM)
    timetable = []
    base_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    
    # Peak hours
    peak_hours = [7, 8, 17, 18]  # 7-8 AM, 5-6 PM
    
    for hour in range(12):  # 6 AM to 6 PM
        for minute in range(0, 60, 30):  # Every 30 minutes
            current_time = base_time + timedelta(hours=hour, minutes=minute)
            time_slot = f"{current_time.strftime('%H:%M')}-{(current_time + timedelta(minutes=30)).strftime('%H:%M')}"
            
            # Determine number of trains based on peak hours
            is_peak_hour = current_time.hour in peak_hours
            if is_peak_hour:
                num_trains = random.randint(12, 18)  # More trains during peak
            else:
                num_trains = random.randint(8, 12)   # Fewer trains during off-peak
            
            # Generate trains for this time slot
            trains = []
            for i in range(num_trains):
                # Select route
                route = random.choice(list(routes.keys()))
                
                # Generate train data
                train_data = {
                    'trainset_id': f'TRAIN_{i+1:03d}',
                    'depot': random.choice(['Aluva Depot', 'Petta Depot']),
                    'route': route,
                    'capacity': random.choice([250, 300, 350]),
                    'ai_score': round(random.uniform(75, 95), 1),
                    'reliability_score': round(random.uniform(80, 98), 1),
                    'maintenance_status': random.choice(['Good', 'Due Soon', 'Overdue']),
                    'passenger_count': random.randint(50, 300),
                    'speed': random.uniform(25, 35),
                    'delay_minutes': random.randint(0, 5),
                    'weather_impact': random.choice(['None', 'Low', 'Medium', 'High'])
                }
                
                trains.append(train_data)
            
            # Add time slot to timetable
            timetable.append({
                'time_slot': time_slot,
                'trains': trains,
                'total_trains': len(trains),
                'peak_hour': is_peak_hour,
                'demand_level': 'High' if is_peak_hour else 'Normal',
                'weather_condition': random.choice(['Clear', 'Clouds', 'Rain', 'Thunderstorm']),
                'temperature': round(random.uniform(22, 35), 1),
                'humidity': round(random.uniform(60, 90), 1)
            })
    
    return timetable

def create_train_tracking_tab():
    """Create the train tracking platform tab"""
    st.header("🚆 Real-Time Train Tracking Platform")
    
    # Initialize train tracker
    if 'train_tracker' not in st.session_state:
        st.session_state.train_tracker = TrainTracker()
        st.session_state.timetable_analyzer = TimetableAnalyzer()
    
    tracker = st.session_state.train_tracker
    analyzer = st.session_state.timetable_analyzer
    
    # Control panel
    st.subheader("🎛️ Control Panel")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 Initialize Tracking", type="primary"):
            # Get timetable from session state or generate one
            timetable = st.session_state.get('timetable', [])
            
            if not timetable:
                # Generate timetable data if not available
                st.info("📅 Generating timetable data...")
                timetable = generate_timetable_data()
                st.session_state.timetable = timetable
                st.success(f"✅ Generated timetable with {len(timetable)} time slots")
            
            # Initialize trains from timetable
            tracker.initialize_trains_from_timetable(timetable)
            st.success(f"✅ Initialized {len(tracker.trains)} trains from timetable")
    
    with col2:
        if st.button("▶️ Start Tracking"):
            tracker.start_tracking()
            st.success("🚆 Real-time tracking started")
    
    with col3:
        if st.button("⏹️ Stop Tracking"):
            tracker.stop_tracking()
            st.warning("🛑 Tracking stopped")
    
    with col4:
        if st.button("🔄 Refresh Positions"):
            st.rerun()
    
    # Main tracking interface
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Live Map", "📊 Train Status", "⚠️ Alerts & Analysis", "📈 Timetable Analysis"
    ])
    
    with tab1:
        create_live_map_section(tracker)
    
    with tab2:
        create_train_status_section(tracker)
    
    with tab3:
        create_alerts_section(tracker)
    
    with tab4:
        create_timetable_analysis_section(analyzer)

def create_live_map_section(tracker: TrainTracker):
    """Create the live map visualization"""
    st.subheader("🗺️ Live Train Tracking Map")
    
    # Get current train positions
    trains = tracker.get_train_positions()
    
    if not trains:
        st.warning("⚠️ No trains are currently being tracked. Please initialize tracking first.")
        return
    
    # Create base map centered on Kochi Metro
    center_lat, center_lon = 10.0, 76.3
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add station markers
    station_coords = tracker.station_coordinates
    for station_name, (lat, lon) in station_coords.items():
        folium.Marker(
            [lat, lon],
            popup=f"<b>{station_name}</b><br>Metro Station",
            icon=folium.Icon(color='blue', icon='train', prefix='fa'),
            tooltip=station_name
        ).add_to(m)
    
    # Add train markers
    for train_id, train in trains.items():
        # Determine marker color based on status
        color_map = {
            TrainStatus.STATIONARY: 'green',
            TrainStatus.MOVING: 'red',
            TrainStatus.ARRIVING: 'orange',
            TrainStatus.DEPARTING: 'yellow',
            TrainStatus.DELAYED: 'purple',
            TrainStatus.MAINTENANCE: 'gray'
        }
        
        color = color_map.get(train.status, 'blue')
        
        # Create popup content
        popup_content = f"""
        <div style="width: 250px;">
            <h4>🚆 Train {train_id}</h4>
            <p><b>Status:</b> {train.status.value.title()}</p>
            <p><b>Current Station:</b> {train.current_station}</p>
            <p><b>Next Station:</b> {train.next_station}</p>
            <p><b>Route:</b> {train.route}</p>
            <p><b>Speed:</b> {train.speed:.1f} km/h</p>
            <p><b>Passengers:</b> {train.passenger_count}/{train.capacity}</p>
            <p><b>Delay:</b> {train.delay_minutes} min</p>
            <p><b>Direction:</b> {train.direction}</p>
            <p><b>Last Update:</b> {train.last_update.strftime('%H:%M:%S')}</p>
        </div>
        """
        
        folium.Marker(
            [train.position_lat, train.position_lon],
            popup=folium.Popup(popup_content, max_width=300),
            icon=folium.Icon(color=color, icon='train', prefix='fa'),
            tooltip=f"Train {train_id} - {train.status.value.title()}"
        ).add_to(m)
    
    # Add route lines
    add_route_lines(m, tracker)
    
    # Add collision alerts
    add_collision_alerts(m, tracker)
    
    # Display map
    st_folium.st_folium(m, width=1000, height=600, returned_objects=[])
    
    # Map controls
    st.subheader("🎛️ Map Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        show_stations = st.checkbox("Show Stations", value=True)
        show_routes = st.checkbox("Show Routes", value=True)
    
    with col2:
        filter_status = st.multiselect(
            "Filter by Status",
            options=[status.value for status in TrainStatus],
            default=[status.value for status in TrainStatus]
        )
    
    with col3:
        filter_route = st.multiselect(
            "Filter by Route",
            options=list(tracker.route_segments.keys()),
            default=list(tracker.route_segments.keys())
        )

def add_route_lines(m, tracker: TrainTracker):
    """Add route lines to the map"""
    route_colors = {
        "Aluva-Kakkanad": "red",
        "Thrippunithura-Vytilla": "blue"
    }
    
    for route_name, stations in tracker.route_segments.items():
        if route_name in route_colors:
            color = route_colors[route_name]
            
            # Create route line
            route_coords = []
            for station in stations:
                if station in tracker.station_coordinates:
                    lat, lon = tracker.station_coordinates[station]
                    route_coords.append([lat, lon])
            
            if route_coords:
                folium.PolyLine(
                    route_coords,
                    color=color,
                    weight=4,
                    opacity=0.7,
                    popup=f"<b>{route_name}</b> Route"
                ).add_to(m)

def add_collision_alerts(m, tracker: TrainTracker):
    """Add collision alert markers to the map"""
    collision_alerts = tracker.collision_detector.get_collision_alerts()
    
    for alert in collision_alerts:
        # Get position of first train in collision
        train1_id = alert['trains'][0]
        train1 = tracker.get_train_by_id(train1_id)
        
        if train1:
            severity_color = 'red' if alert['severity'] == 'HIGH' else 'orange'
            
            folium.Marker(
                [train1.position_lat, train1.position_lon],
                popup=f"""
                <div style="width: 200px;">
                    <h4>⚠️ Collision Alert</h4>
                    <p><b>Severity:</b> {alert['severity']}</p>
                    <p><b>Trains:</b> {', '.join(alert['trains'])}</p>
                    <p><b>Distance:</b> {alert['distance']:.4f}°</p>
                    <p><b>Location:</b> {alert['location']}</p>
                </div>
                """,
                icon=folium.Icon(color=severity_color, icon='exclamation-triangle', prefix='fa'),
                tooltip=f"Collision Alert: {alert['severity']}"
            ).add_to(m)

def create_train_status_section(tracker: TrainTracker):
    """Create train status overview section"""
    st.subheader("📊 Train Status Overview")
    
    trains = tracker.get_train_positions()
    
    if not trains:
        st.warning("⚠️ No trains are currently being tracked.")
        return
    
    # Status summary
    col1, col2, col3, col4 = st.columns(4)
    
    status_counts = {}
    for train in trains.values():
        status = train.status.value
        status_counts[status] = status_counts.get(status, 0) + 1
    
    with col1:
        st.metric("Total Trains", len(trains))
    
    with col2:
        moving_trains = status_counts.get('moving', 0)
        st.metric("Moving", moving_trains)
    
    with col3:
        stationary_trains = status_counts.get('stationary', 0)
        st.metric("Stationary", stationary_trains)
    
    with col4:
        delayed_trains = status_counts.get('delayed', 0)
        st.metric("Delayed", delayed_trains)
    
    # Detailed train status table
    st.subheader("🚆 Detailed Train Status")
    
    # Create status DataFrame
    status_data = []
    for train_id, train in trains.items():
        status_data.append({
            'Train ID': train_id,
            'Status': train.status.value.title(),
            'Current Station': train.current_station,
            'Next Station': train.next_station,
            'Route': train.route,
            'Speed (km/h)': f"{train.speed:.1f}",
            'Passengers': f"{train.passenger_count}/{train.capacity}",
            'Delay (min)': train.delay_minutes,
            'Direction': train.direction.title(),
            'Last Update': train.last_update.strftime('%H:%M:%S')
        })
    
    status_df = pd.DataFrame(status_data)
    st.dataframe(status_df, use_container_width=True)
    
    # Status distribution chart
    if status_counts:
        st.subheader("📈 Status Distribution")
        
        fig = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Train Status Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

def create_alerts_section(tracker: TrainTracker):
    """Create alerts and monitoring section"""
    st.subheader("⚠️ Alerts & Monitoring")
    
    # Collision alerts
    collision_alerts = tracker.collision_detector.get_collision_alerts()
    
    # Send collision alerts to main dashboard alerts
    if collision_alerts and 'system_manager' in st.session_state:
        # Get collision alerts and integrate with main alert system
        system_alerts = st.session_state.system_manager.get_collision_alerts()
        if system_alerts:
            st.info(f"📢 **{len(system_alerts)} collision alert(s) sent to main dashboard**")
    
    if collision_alerts:
        st.error(f"🚨 **{len(collision_alerts)} Collision Alert(s) Detected**")
        
        for alert in collision_alerts:
            severity_color = "🔴" if alert['severity'] == 'HIGH' else "🟡"
            
            with st.expander(f"{severity_color} Alert: Trains {', '.join(alert['trains'])}"):
                st.write(f"**Severity:** {alert['severity']}")
                st.write(f"**Distance:** {alert['distance']:.4f} degrees")
                st.write(f"**Location:** {alert['location']}")
                st.write(f"**Time:** {alert['timestamp'].strftime('%H:%M:%S')}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🚨 Emergency Stop Trains {', '.join(alert['trains'])}"):
                        st.error("🚨 Emergency stop initiated! Contact control center immediately.")
                with col2:
                    if st.button(f"📢 Send to Dashboard", key=f"send_alert_{alert['trains'][0]}_{alert['trains'][1]}"):
                        st.success("✅ Alert sent to main dashboard alerts section!")
    else:
        st.success("✅ No collision alerts detected")
    
    # Delay alerts
    st.subheader("⏰ Delay Monitoring")
    
    trains = tracker.get_train_positions()
    delayed_trains = [train for train in trains.values() if train.delay_minutes > 5]
    
    if delayed_trains:
        st.warning(f"⚠️ **{len(delayed_trains)} Train(s) with Significant Delays**")
        
        delay_data = []
        for train in delayed_trains:
            delay_data.append({
                'Train ID': train.trainset_id,
                'Delay (min)': train.delay_minutes,
                'Current Station': train.current_station,
                'Route': train.route,
                'Status': train.status.value.title()
            })
        
        delay_df = pd.DataFrame(delay_data)
        st.dataframe(delay_df, use_container_width=True)
    else:
        st.success("✅ No significant delays detected")
    
    # Capacity alerts
    st.subheader("👥 Capacity Monitoring")
    
    overcrowded_trains = [train for train in trains.values() 
                        if train.passenger_count > train.capacity * 0.9]
    
    if overcrowded_trains:
        st.warning(f"⚠️ **{len(overcrowded_trains)} Train(s) Near Capacity**")
        
        capacity_data = []
        for train in overcrowded_trains:
            utilization = (train.passenger_count / train.capacity) * 100
            capacity_data.append({
                'Train ID': train.trainset_id,
                'Utilization %': f"{utilization:.1f}%",
                'Passengers': f"{train.passenger_count}/{train.capacity}",
                'Current Station': train.current_station,
                'Route': train.route
            })
        
        capacity_df = pd.DataFrame(capacity_data)
        st.dataframe(capacity_df, use_container_width=True)
    else:
        st.success("✅ All trains operating within normal capacity")

def create_timetable_analysis_section(analyzer: TimetableAnalyzer):
    """Create timetable analysis section"""
    st.subheader("📈 Timetable Analysis & Optimization")
    
    # Get timetable from session state
    timetable = st.session_state.get('timetable', [])
    
    if not timetable:
        st.warning("⚠️ No timetable data available for analysis.")
        st.info("💡 Click '🚀 Initialize Tracking' to generate timetable data.")
        return
    
    # Analyze timetable
    analysis = analyzer.analyze_timetable(timetable)
    
    # Display timetable overview
    st.subheader("📅 Generated Timetable Overview")
    
    # Show first few time slots as example
    st.write("**Sample Time Slots:**")
    sample_slots = timetable[:5]  # Show first 5 slots
    
    for slot in sample_slots:
        with st.expander(f"🕒 {slot['time_slot']} - {slot['total_trains']} trains ({'Peak' if slot['peak_hour'] else 'Normal'})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Trains:** {slot['total_trains']}")
                st.write(f"**Demand:** {slot['demand_level']}")
            
            with col2:
                st.write(f"**Weather:** {slot['weather_condition']}")
                st.write(f"**Temperature:** {slot['temperature']}°C")
            
            with col3:
                st.write(f"**Humidity:** {slot['humidity']}%")
                st.write(f"**Peak Hour:** {'Yes' if slot['peak_hour'] else 'No'}")
            
            # Show train details
            st.write("**Train Details:**")
            train_df = pd.DataFrame(slot['trains'])
            st.dataframe(train_df[['trainset_id', 'route', 'capacity', 'ai_score', 'delay_minutes']], use_container_width=True)
    
    # Analysis summary
    st.subheader("📊 Analysis Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Time Slots", analysis['total_slots'])
    
    with col2:
        st.metric("Peak Hour Slots", analysis['peak_slots'])
    
    with col3:
        st.metric("Total Train Assignments", analysis['total_train_assignments'])
    
    with col4:
        overlap_count = len(analysis['potential_overlaps'])
        st.metric("Potential Overlaps", overlap_count)
    
    # Route distribution
    st.subheader("🚏 Route Distribution")
    
    if analysis['route_distribution']:
        route_df = pd.DataFrame([
            {'Route': route, 'Train Count': count}
            for route, count in analysis['route_distribution'].items()
        ])
        
        fig = px.bar(route_df, x='Route', y='Train Count',
                    title="Train Distribution by Route")
        st.plotly_chart(fig, use_container_width=True)
    
    # Capacity utilization
    st.subheader("📊 Capacity Utilization")
    
    if analysis['capacity_utilization']:
        capacity_df = pd.DataFrame(analysis['capacity_utilization'])
        
        fig = px.line(capacity_df, x='time_slot', y='total_capacity',
                     title="Capacity Utilization Over Time")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Potential overlaps
    if analysis['potential_overlaps']:
        st.subheader("⚠️ Potential Overlaps")
        
        overlap_data = []
        for overlap in analysis['potential_overlaps']:
            overlap_data.append({
                'Time Slot 1': overlap['slot1'],
                'Time Slot 2': overlap['slot2'],
                'Overlapping Trains': len(overlap['overlapping_trains']),
                'Severity': overlap['severity'],
                'Train IDs': ', '.join(overlap['overlapping_trains'])
            })
        
        overlap_df = pd.DataFrame(overlap_data)
        st.dataframe(overlap_df, use_container_width=True)
    else:
        st.success("✅ No timetable overlaps detected")
    
    # Optimization suggestions
    st.subheader("💡 Optimization Suggestions")
    
    if analysis['optimization_suggestions']:
        for i, suggestion in enumerate(analysis['optimization_suggestions'], 1):
            st.write(f"{i}. {suggestion}")
    else:
        st.info("ℹ️ No optimization suggestions at this time.")
    
    # Export options
    st.subheader("📤 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Timetable CSV"):
            # Convert timetable to CSV format
            csv_data = []
            for slot in timetable:
                for train in slot['trains']:
                    csv_data.append({
                        'time_slot': slot['time_slot'],
                        'peak_hour': slot['peak_hour'],
                        'demand_level': slot['demand_level'],
                        'weather_condition': slot['weather_condition'],
                        'temperature': slot['temperature'],
                        'humidity': slot['humidity'],
                        'trainset_id': train['trainset_id'],
                        'depot': train['depot'],
                        'route': train['route'],
                        'capacity': train['capacity'],
                        'ai_score': train['ai_score'],
                        'reliability_score': train['reliability_score'],
                        'maintenance_status': train['maintenance_status'],
                        'passenger_count': train['passenger_count'],
                        'speed': train['speed'],
                        'delay_minutes': train['delay_minutes'],
                        'weather_impact': train['weather_impact']
                    })
            
            df = pd.DataFrame(csv_data)
            csv_string = df.to_csv(index=False)
            
            st.download_button(
                label="Download Timetable CSV",
                data=csv_string,
                file_name=f"generated_timetable_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📈 Export Analysis Report"):
            analysis_report = {
                'analysis_timestamp': datetime.now().isoformat(),
                'timetable_summary': {
                    'total_slots': analysis['total_slots'],
                    'peak_slots': analysis['peak_slots'],
                    'off_peak_slots': analysis['off_peak_slots'],
                    'total_train_assignments': analysis['total_train_assignments']
                },
                'route_distribution': analysis['route_distribution'],
                'capacity_utilization': analysis['capacity_utilization'],
                'potential_overlaps': analysis['potential_overlaps'],
                'optimization_suggestions': analysis['optimization_suggestions']
            }
            
            json_data = json.dumps(analysis_report, indent=2, default=str)
            st.download_button(
                label="Download Analysis Report",
                data=json_data,
                file_name=f"timetable_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
