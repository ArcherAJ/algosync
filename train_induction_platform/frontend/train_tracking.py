from common_imports import *
from train_tracker import TrainTracker, TrainStatus, CollisionDetector, TimetableAnalyzer
from mock_train_tracking_data import MockTrainTrackingDataGenerator, generate_timetable_data, generate_tracking_data
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
        if st.button("🚀 Initialize Tracking", type="primary", key="init_tracking_btn"):
            with st.spinner("🚆 Initializing train tracking system..."):
                # Get timetable from session state or generate one
                timetable = st.session_state.get('timetable', [])
                
                if not timetable:
                    # Generate comprehensive timetable data
                    st.info("📅 Generating comprehensive timetable data...")
                    generator = MockTrainTrackingDataGenerator()
                    timetable = generator.generate_timetable_data()
                    st.session_state.timetable = timetable
                    st.session_state.mock_generator = generator
                    st.success(f"✅ Generated timetable with {len(timetable)} time slots")
                
                # Initialize trains from timetable
                tracker.initialize_trains_from_timetable(timetable)
                
                # Generate real-time tracking data
                tracking_data = generate_tracking_data()
                st.session_state.tracking_data = tracking_data
                
                # Start tracking automatically
                tracker.start_tracking()
                
                st.success(f"✅ Initialized {len(tracker.trains)} trains from timetable")
                st.success("🚆 Real-time tracking started automatically")
                
                # Show summary
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Active Trains", len(tracker.trains))
                with col_b:
                    st.metric("Time Slots", len(timetable))
                with col_c:
                    st.metric("Routes", len(set(train.route for train in tracker.trains.values())))
    
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
    """Create the enhanced live map visualization"""
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
    
    # Add station markers with enhanced information
    station_coords = tracker.station_coordinates
    for station_name, (lat, lon) in station_coords.items():
        # Count trains at this station
        trains_at_station = [t for t in trains.values() if t.current_station == station_name]
        
        folium.Marker(
            [lat, lon],
            popup=f"""
            <b>🚉 {station_name}</b><br>
            <b>Trains at Station:</b> {len(trains_at_station)}<br>
            <b>Coordinates:</b> {lat:.4f}, {lon:.4f}
            """,
            icon=folium.Icon(color='blue', icon='train', prefix='fa'),
            tooltip=f"{station_name} ({len(trains_at_station)} trains)"
        ).add_to(m)
    
    # Add route lines
    routes = tracker.route_segments
    for route_name, stations in routes.items():
        route_coords = []
        for station in stations:
            if station in station_coords:
                route_coords.append([station_coords[station][0], station_coords[station][1]])
        
        if route_coords:
            folium.PolyLine(
                route_coords,
                color='blue' if 'Aluva' in route_name else 'red',
                weight=3,
                opacity=0.7,
                popup=f"<b>{route_name}</b> Route"
            ).add_to(m)
    
    # Add train markers with enhanced information
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
        
        # Create custom icon based on status
        icon_map = {
            TrainStatus.STATIONARY: 'pause',
            TrainStatus.MOVING: 'play',
            TrainStatus.ARRIVING: 'arrow-down',
            TrainStatus.DEPARTING: 'arrow-up',
            TrainStatus.DELAYED: 'exclamation-triangle',
            TrainStatus.MAINTENANCE: 'wrench'
        }
        
        icon = icon_map.get(train.status, 'train')
        
        # Calculate passenger load percentage
        load_percentage = (train.passenger_count / train.capacity) * 100
        
        # Add train marker with enhanced popup
        folium.Marker(
            [train.position_lat, train.position_lon],
            popup=f"""
            <div style="width: 300px;">
                <h3>🚆 {train_id}</h3>
                <table style="width: 100%; font-size: 12px;">
                    <tr><td><b>Status:</b></td><td>{train.status.value.title()}</td></tr>
                    <tr><td><b>Current Station:</b></td><td>{train.current_station}</td></tr>
                    <tr><td><b>Next Station:</b></td><td>{train.next_station}</td></tr>
                    <tr><td><b>Route:</b></td><td>{train.route}</td></tr>
                    <tr><td><b>Speed:</b></td><td>{train.speed:.1f} km/h</td></tr>
                    <tr><td><b>Passengers:</b></td><td>{train.passenger_count}/{train.capacity} ({load_percentage:.1f}%)</td></tr>
                    <tr><td><b>Delay:</b></td><td>{train.delay_minutes} min</td></tr>
                    <tr><td><b>Direction:</b></td><td>{train.direction.title()}</td></tr>
                    <tr><td><b>Last Update:</b></td><td>{train.last_update.strftime('%H:%M:%S')}</td></tr>
                </table>
            </div>
            """,
            icon=folium.Icon(color=color, icon=icon, prefix='fa'),
            tooltip=f"{train_id} - {train.status.value.title()} - {load_percentage:.0f}% full"
        ).add_to(m)
    
    # Add legend
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 200px; height: 120px; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <p><b>🚆 Train Status Legend</b></p>
    <p><i class="fa fa-pause" style="color:green"></i> Stationary</p>
    <p><i class="fa fa-play" style="color:red"></i> Moving</p>
    <p><i class="fa fa-arrow-down" style="color:orange"></i> Arriving</p>
    <p><i class="fa fa-arrow-up" style="color:yellow"></i> Departing</p>
    <p><i class="fa fa-exclamation-triangle" style="color:purple"></i> Delayed</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Display the map
    st_folium.st_folium(m, width=700, height=500)
    
    # Add map controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Refresh Map", key="refresh_map"):
            st.rerun()
    
    with col2:
        if st.button("📍 Center Map", key="center_map"):
            st.rerun()
    
    with col3:
        if st.button("📊 Show Statistics", key="show_stats"):
            st.rerun()
    
    # IBM Maximo Integration Controls
    st.subheader("🔧 IBM Maximo Integration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        maximo_status = tracker.get_maximo_status()
        if maximo_status['connected']:
            st.success("✅ Maximo Connected")
        else:
            st.warning("⚠️ Maximo Disconnected")
    
    with col2:
        if st.button("🔗 Connect Maximo", key="connect_maximo"):
            if tracker.enable_maximo_sync():
                st.success("✅ Connected to IBM Maximo")
            else:
                st.error("❌ Failed to connect to Maximo")
    
    with col3:
        if st.button("🔄 Sync with Maximo", key="sync_maximo"):
            with st.spinner("Syncing with Maximo..."):
                sync_results = tracker.sync_all_trains_with_maximo()
                if 'error' not in sync_results:
                    st.success(f"✅ Synced {sync_results['trains_synced']} trains")
                else:
                    st.error(f"❌ Sync failed: {sync_results['error']}")
    
    # Show Maximo status details
    if maximo_status['connected']:
        st.info(f"**Maximo Server:** {maximo_status['server_url']} | **Last Sync:** {maximo_status['last_sync'] or 'Never'}")
    
    # Show map statistics
    st.subheader("📊 Map Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Trains", len(trains))
    
    with col2:
        moving_trains = len([t for t in trains.values() if t.status == TrainStatus.MOVING])
        st.metric("Moving Trains", moving_trains)
    
    with col3:
        delayed_trains = len([t for t in trains.values() if t.delay_minutes > 0])
        st.metric("Delayed Trains", delayed_trains)
    
    with col4:
        total_passengers = sum(t.passenger_count for t in trains.values())
        st.metric("Total Passengers", total_passengers)
    
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
    
    # Handle both list and dictionary formats for display
    if isinstance(timetable, list):
        sample_slots = timetable[:5]  # Show first 5 slots from list
        slot_keys = [f"Slot {i+1}" for i in range(len(sample_slots))]
    else:
        # If it's a dictionary, convert to list for display
        sample_slots = list(timetable.values())[:5]
        slot_keys = list(timetable.keys())[:5]
    
    for i, slot in enumerate(sample_slots):
        time_slot = slot_keys[i] if i < len(slot_keys) else f"Slot {i+1}"
        
        # Handle different data structures
        if isinstance(slot, dict):
            # For AI optimizer output
            total_trains = len(slot.get('trains', []))
            is_peak = slot.get('is_peak_hour', False)
            predicted_demand = slot.get('predicted_demand', 0)
            
            with st.expander(f"🕒 {time_slot} - {total_trains} trains ({'Peak' if is_peak else 'Normal'})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Trains:** {total_trains}")
                    st.write(f"**Demand:** {predicted_demand}")
                
                with col2:
                    st.write(f"**Capacity:** {slot.get('total_capacity', 0)}")
                    st.write(f"**Avg Health:** {slot.get('avg_health_score', 0):.1f}")
                
                with col3:
                    st.write(f"**Peak Hour:** {'Yes' if is_peak else 'No'}")
                    st.write(f"**Routes:** {len(slot.get('route_assignments', {}))}")
                
                # Show train details if available
                if slot.get('trains'):
                    st.write("**Train Details:**")
                    train_data = []
                    for train in slot['trains']:
                        train_data.append({
                            'Train ID': train.get('trainset_id', 'Unknown'),
                            'Depot': train.get('depot', 'Unknown'),
                            'Health Score': f"{slot.get('avg_health_score', 0):.1f}",
                            'Status': train.get('operational_status', 'Unknown')
                        })
                    
                    if train_data:
                        train_df = pd.DataFrame(train_data)
                        st.dataframe(train_df, use_container_width=True)
        else:
            # For legacy format with time_slot field
            with st.expander(f"🕒 {slot.get('time_slot', time_slot)} - {slot.get('total_trains', 0)} trains ({'Peak' if slot.get('peak_hour', False) else 'Normal'})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Trains:** {slot.get('total_trains', 0)}")
                    st.write(f"**Demand:** {slot.get('demand_level', 'N/A')}")
                
                with col2:
                    st.write(f"**Weather:** {slot.get('weather_condition', 'N/A')}")
                    st.write(f"**Temperature:** {slot.get('temperature', 'N/A')}°C")
                
                with col3:
                    st.write(f"**Humidity:** {slot.get('humidity', 'N/A')}%")
                    st.write(f"**Peak Hour:** {'Yes' if slot.get('peak_hour', False) else 'No'}")
                
                # Show train details
                if slot.get('trains'):
                    st.write("**Train Details:**")
                    train_df = pd.DataFrame(slot['trains'])
                    if 'trainset_id' in train_df.columns:
                        display_cols = ['trainset_id', 'route', 'capacity', 'ai_score', 'delay_minutes']
                        available_cols = [col for col in display_cols if col in train_df.columns]
                        st.dataframe(train_df[available_cols], use_container_width=True)
    
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
        if st.button("📊 Export Timetable CSV", key="export_timetable_csv_tracking"):
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
