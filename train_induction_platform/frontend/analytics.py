from common_imports import *

def create_analytics_tab():
    """Create the analytics and trends tab"""
    
    # Enhanced Analytics CSS
    st.markdown("""
    <style>
    .analytics-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .analytics-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        transition: all 0.3s ease;
    }
    
    .analytics-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .section-title {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #667eea;
        font-size: 1.3rem;
        font-weight: 600;
        color: #495057;
    }
    
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .metric-item {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .metric-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-number {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced Analytics Header
    st.markdown("""
    <div class="analytics-header">
        <h1 style="margin: 0; font-size: 2rem; font-weight: 700;">📈 Analytics & Performance Trends</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.1rem;">Comprehensive insights and data-driven analytics</p>
    </div>
    """, unsafe_allow_html=True)
    # Historical trends
    trends = st.session_state.system_manager.get_optimization_trends()
    if trends and len(trends['timestamps']) > 1:
        # Create time series plots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Service Readiness', 'Fitness Compliance', 
                           'Alert Counts', 'Processing Time'),
            vertical_spacing=0.1
        )
        # Service readiness trend
        fig.add_trace(
            go.Scatter(x=trends['timestamps'], y=trends['service_readiness'], 
                      name='Service Ready', line=dict(color='green')),
            row=1, col=1
        )
        # Fitness compliance trend
        fig.add_trace(
            go.Scatter(x=trends['timestamps'], y=trends['fitness_compliance'], 
                      name='Fitness %', line=dict(color='blue')),
            row=1, col=2
        )
        # Alert counts
        fig.add_trace(
            go.Scatter(x=trends['timestamps'], y=trends['alert_counts'], 
                      name='Alerts', line=dict(color='red')),
            row=2, col=1
        )
        # Processing times
        fig.add_trace(
            go.Scatter(x=trends['timestamps'], y=trends['processing_times'], 
                      name='Processing Time (s)', line=dict(color='orange')),
            row=2, col=2
        ) 
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Run multiple optimizations to see trends")
    # Performance metrics summary
    if 'current_metrics' in st.session_state:
        metrics = st.session_state.current_metrics
        st.subheader("Current Performance Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Fitness Compliance", f"{metrics.get('fitness_compliance', 0)}%")
            st.metric("Avg Reliability", f"{metrics.get('avg_reliability', 0)}%")
        with col2:
            st.metric("Maintenance Backlog", metrics.get('maintenance_backlog', 0))
            st.metric("Processing Time", f"{metrics.get('processing_time', 0)}s")
        with col3:
            st.metric("Estimated Savings", f"₹{metrics.get('estimated_savings', 0):,}")
            st.metric("Energy Efficiency", f"{metrics.get('energy_efficiency', 0)}%")
    # IoT Sensors Analytics
    st.subheader("📡 IoT Sensors Analytics")
    
    if 'system_manager' in st.session_state:
        system_manager = st.session_state.system_manager
        
        # Get IoT sensor summary
        sensor_summary = system_manager.iot_manager.get_fleet_sensor_summary()
        
        if sensor_summary:
            # Calculate sensor counts from sensor_stats
            sensor_stats = sensor_summary.get('sensor_stats', {})
            total_sensors = sum(sum(stats.values()) for stats in sensor_stats.values())
            healthy_sensors = sum(stats.get('normal', 0) for stats in sensor_stats.values())
            warning_sensors = sum(stats.get('warning', 0) for stats in sensor_stats.values())
            critical_sensors = sum(stats.get('critical', 0) for stats in sensor_stats.values())
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Trainsets", sensor_summary.get('total_trainsets', 0))
            
            with col2:
                st.metric("Fleet Health Score", f"{sensor_summary.get('health_score', 0):.1f}%")
            
            with col3:
                st.metric("Active Alerts", len(sensor_summary.get('alerts', [])))
            
            with col4:
                st.metric("Total Sensors", total_sensors)
            
            # Sensor health distribution
            if total_sensors > 0:
                st.write("**Sensor Health Distribution:**")
                health_data = {
                    'Normal': healthy_sensors,
                    'Warning': warning_sensors,
                    'Critical': critical_sensors
                }
                
                fig = px.pie(values=list(health_data.values()), names=list(health_data.keys()),
                            title="Sensor Health Distribution",
                            color_discrete_map={'Normal': '#28a745', 'Warning': '#ffc107', 'Critical': '#dc3545'})
                st.plotly_chart(fig, use_container_width=True)
            
            # Sensor alerts
            alerts = sensor_summary.get('alerts', [])
            if alerts:
                st.write("**Recent Sensor Alerts:**")
                alerts_df = pd.DataFrame(alerts[:10])  # Show last 10 alerts
                st.dataframe(alerts_df, use_container_width=True)
            else:
                st.success("✅ No active sensor alerts")
        else:
            st.info("IoT sensor data not available")
    
    # Smart Systems Analytics
    st.subheader("🏢 Smart Systems Analytics")
    
    if 'system_manager' in st.session_state:
        # Get station summary
        station_summary = system_manager.station_manager.get_fleet_station_summary()
        
        if station_summary:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Stations", station_summary['total_stations'])
            
            with col2:
                st.metric("Overall Health", f"{station_summary['overall_health']:.1f}%")
            
            with col3:
                st.metric("Crowd Alerts", len(station_summary['crowd_alerts']))
            
            with col4:
                critical_stations = len([s for s in station_summary['stations'] if s['status'] == 'Critical'])
                st.metric("Critical Stations", critical_stations)
            
            # Station health overview
            st.write("**Station Health Overview:**")
            if station_summary['stations']:
                stations_df = pd.DataFrame(station_summary['stations'])
                
                # Station health chart
                fig = px.bar(stations_df, x='station_id', y='health_score',
                            title="Station Health Scores",
                            color='health_score',
                            color_continuous_scale=['red', 'yellow', 'green'])
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Station capacity utilization
                st.write("**Station Capacity Utilization:**")
                capacity_data = []
                for station in station_summary['stations']:
                    capacity_data.append({
                        'Station': station['station_id'],
                        'Current Capacity': station.get('current_capacity', 0),
                        'Max Capacity': station.get('max_capacity', 100),
                        'Utilization %': (station.get('current_capacity', 0) / station.get('max_capacity', 100)) * 100
                    })
                
                capacity_df = pd.DataFrame(capacity_data)
                fig = px.bar(capacity_df, x='Station', y='Utilization %',
                            title="Station Capacity Utilization",
                            color='Utilization %',
                            color_continuous_scale=['green', 'yellow', 'red'])
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Smart systems data not available")
    
    # Export options
    st.subheader("📊 Export Options")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📄 Export Fleet Status"):
            fleet_df = pd.DataFrame([
                {
                    'Trainset': t['id'],
                    'Depot': t['depot'],
                    'AI_Score': t['ai_score'],
                    'Recommendation': t['recommendation'],
                    'Fitness_Valid': t['fitness']['overall_valid'],
                    'Open_Jobs': t['job_cards']['open'],
                    'Reliability': t['operational']['reliability_score']
                }
                for t in st.session_state.trainsets
            ])
            csv = fleet_df.to_csv(index=False)
            st.download_button(
                label="Download Fleet Status CSV",
                data=csv,
                file_name=f"fleet_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    with col2:
        if st.button("🔧 Export Maintenance Plan"):
            if 'maintenance_predictions' in st.session_state:
                csv = st.session_state.maintenance_predictions.to_csv(index=False)
                st.download_button(
                    label="Download Maintenance Plan CSV",
                    data=csv,
                    file_name=f"maintenance_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    with col3:
        if st.button("📊 Export Analytics Report"):
            # Generate comprehensive report
            report = st.session_state.system_manager.generate_comprehensive_report(
                st.session_state.trainsets,
                st.session_state.get('current_metrics', {}),
                st.session_state.get('current_alerts', []),
                'optimization_summary'
            ) 
            if report:
                report_json = json.dumps(report, default=str, indent=2)
                st.download_button(
                    label="Download Analytics Report JSON",
                    data=report_json,
                    file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )