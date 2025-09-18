from common_imports import *

def create_weather_section(system_manager):
    """Create weather monitoring and analytics section"""
    st.subheader("🌤️ Weather Monitoring & Analytics")
    
    # Get weather data
    weather_insights = system_manager.weather_integrator.get_weather_insights()
    current_weather = weather_insights['current_weather']
    forecast = weather_insights['forecast']
    recommendations = weather_insights['recommendations']
    
    # Current weather display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Temperature",
            f"{current_weather['temperature']}°C",
            f"Humidity: {current_weather['humidity']}%"
        )
    
    with col2:
        st.metric(
            "Weather Condition",
            current_weather['weather_condition'],
            current_weather['weather_description']
        )
    
    with col3:
        st.metric(
            "Wind Speed",
            f"{current_weather['wind_speed']} m/s",
            f"Pressure: {current_weather['pressure']} hPa"
        )
    
    with col4:
        st.metric(
            "Visibility",
            f"{current_weather['visibility']/1000:.1f} km",
            f"Impact Factor: {weather_insights['impact_factor']:.2f}"
        )
    
    # API Status indicator
    data_source = current_weather.get('data_source', 'Unknown')
    if 'API' in data_source:
        st.success(f"✅ **Live Weather Data**: {data_source}")
    elif 'Mock' in data_source:
        st.warning(f"⚠️ **Mock Weather Data**: {data_source} - Configure API key for real data")
    else:
        st.info(f"ℹ️ **Weather Data Source**: {data_source}")
    
    # Weather forecast chart
    st.subheader("📅 3-Day Weather Forecast")
    
    if forecast:
        forecast_df = pd.DataFrame(forecast)
        forecast_df['hour'] = forecast_df['datetime'].dt.hour
        forecast_df['date'] = forecast_df['datetime'].dt.date
        
        # Create forecast chart
        fig = px.line(forecast_df, x='datetime', y='temperature',
                     title="Temperature Forecast",
                     color='weather_condition',
                     hover_data=['humidity', 'weather_description'])
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display forecast table
        st.write("**Detailed Forecast:**")
        forecast_display = forecast_df[['datetime', 'temperature', 'humidity', 'weather_condition', 'weather_description']].copy()
        forecast_display['datetime'] = forecast_display['datetime'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(forecast_display, use_container_width=True)
    
    # Weather recommendations
    st.subheader("🌦️ Weather-Based Recommendations")
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    else:
        st.info("No specific weather recommendations at this time.")
    
    # Weather impact on operations
    st.subheader("📊 Weather Impact Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Passenger Demand Impact**")
        
        # Simulate demand impact for different weather conditions
        weather_conditions = ['Clear', 'Clouds', 'Rain', 'Thunderstorm']
        demand_impact = []
        
        for condition in weather_conditions:
            test_weather = current_weather.copy()
            test_weather['weather_condition'] = condition
            impact = system_manager.weather_integrator.calculate_weather_impact(test_weather, 1000)
            demand_impact.append(impact)
        
        impact_df = pd.DataFrame({
            'Weather Condition': weather_conditions,
            'Demand Impact': demand_impact
        })
        
        fig = px.bar(impact_df, x='Weather Condition', y='Demand Impact',
                    title="Demand Impact by Weather Condition",
                    color='Demand Impact',
                    color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Operational Recommendations**")
        
        # Generate operational recommendations based on weather
        if current_weather['weather_condition'] in ['Rain', 'Thunderstorm']:
            st.warning("🌧️ **Rain Alert** - Consider reducing train frequency and increasing platform staff")
        elif current_weather['temperature'] > 35:
            st.warning("🌡️ **Heat Alert** - Ensure HVAC systems are functioning optimally")
        elif current_weather['wind_speed'] > 20:
            st.warning("💨 **Wind Alert** - Secure outdoor equipment and monitor for debris")
        else:
            st.success("✅ **Normal Conditions** - Standard operations recommended")
    
    # Weather API configuration
    st.subheader("⚙️ Weather API Configuration")
    
    with st.expander("Configure Weather API", expanded=False):
        st.markdown("""
        ### 🌤️ Get Your Free Weather API Key
        
        **Step 1**: Visit [OpenWeatherMap](https://home.openweathermap.org/users/sign_up) and sign up for free
        
        **Step 2**: After registration, go to "API keys" section and copy your key
        
        **Step 3**: Paste your API key below and click "Save API Key"
        
        **Free Tier Benefits**:
        - ✅ 60 calls per minute
        - ✅ 1,000,000 calls per month  
        - ✅ Current weather data
        - ✅ 5-day weather forecast
        - ✅ No credit card required
        """)
        
        api_key = st.text_input("OpenWeatherMap API Key", type="password", 
                               help="Get your free API key from openweathermap.org",
                               placeholder="Enter your API key here...")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save API Key", type="primary"):
                if api_key and len(api_key) > 20:  # Basic validation
                    system_manager.weather_integrator.set_api_key(api_key)
                    st.success("✅ API key saved! Weather data will now be fetched from OpenWeatherMap.")
                    st.rerun()
                else:
                    st.error("❌ Please enter a valid API key (should be longer than 20 characters)")
        
        with col2:
            if st.button("🔄 Test API Key"):
                if api_key and len(api_key) > 20:
                    test_weather = system_manager.weather_integrator.get_weather_data()
                    if test_weather.get('data_source') == 'OpenWeatherMap API':
                        st.success("✅ API key is working! Real weather data is being fetched.")
                    else:
                        st.error("❌ API key test failed. Please check your key.")
                else:
                    st.error("❌ Please enter a valid API key first")
        
        # Show current API status
        if system_manager.weather_integrator.weather_api_key:
            st.success("✅ **API Key Configured** - Real weather data enabled")
            st.info(f"📊 **Rate Limit**: {system_manager.weather_integrator.api_requests_count}/{system_manager.weather_integrator.rate_limit} requests this minute")
        else:
            st.warning("⚠️ **No API Key** - Using mock weather data for demonstration")
        
        st.markdown("""
        ### 🔗 Quick Links
        - [OpenWeatherMap Sign Up](https://home.openweathermap.org/users/sign_up)
        - [API Documentation](https://openweathermap.org/api)
        - [API Key Management](https://home.openweathermap.org/api_keys)
        """)
    
    # Weather data export
    if st.button("📤 Export Weather Data"):
        weather_data = {
            'current_weather': current_weather,
            'forecast': forecast,
            'recommendations': recommendations,
            'impact_factor': weather_insights['impact_factor'],
            'export_time': datetime.now().isoformat()
        }
        
        json_data = json.dumps(weather_data, indent=2, default=str)
        st.download_button(
            label="Download Weather Data",
            data=json_data,
            file_name=f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def create_iot_sensors_section(system_manager):
    """Create IoT sensors monitoring section"""
    st.subheader("📡 IoT Sensors Monitoring")
    
    # Get sensor summary
    sensor_summary = system_manager.iot_manager.get_fleet_sensor_summary()
    
    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Trainsets", sensor_summary['total_trainsets'])
    
    with col2:
        st.metric("Fleet Health Score", f"{sensor_summary['health_score']:.1f}%")
    
    with col3:
        st.metric("Active Alerts", len(sensor_summary['alerts']))
    
    with col4:
        critical_alerts = len([a for a in sensor_summary['alerts'] if a['status'] == 'Critical'])
        st.metric("Critical Alerts", critical_alerts)
    
    # Sensor statistics
    st.subheader("📊 Sensor Statistics")
    
    if sensor_summary['sensor_stats']:
        # Create DataFrame from sensor stats
        sensor_stats_data = sensor_summary['sensor_stats']
        sensor_stats_rows = []
        for sensor_type, stats in sensor_stats_data.items():
            sensor_stats_rows.append({
                'Sensor Type': sensor_type.title(),
                'Normal': stats['normal'],
                'Warning': stats['warning'],
                'Critical': stats['critical']
            })
        sensor_stats_df = pd.DataFrame(sensor_stats_rows)
        
        # Create stacked bar chart
        fig = px.bar(sensor_stats_df, x='Sensor Type', y=['Normal', 'Warning', 'Critical'],
                    title="Sensor Status Distribution",
                    color_discrete_map={'Normal': 'green', 'Warning': 'orange', 'Critical': 'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Active alerts
    if sensor_summary['alerts']:
        st.subheader("⚠️ Active Sensor Alerts")
        
        alerts_df = pd.DataFrame(sensor_summary['alerts'])
        st.dataframe(alerts_df, use_container_width=True)
        
        # Alert severity distribution
        alert_counts = alerts_df['status'].value_counts()
        fig = px.pie(values=alert_counts.values, names=alert_counts.index,
                    title="Alert Severity Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No active sensor alerts")
    
    # Individual trainset sensor details
    st.subheader("🚆 Individual Trainset Sensor Details")
    
    trainsets = st.session_state.trainsets
    if trainsets:
        selected_trainset = st.selectbox("Select Trainset", [t['id'] for t in trainsets])
        
        if selected_trainset:
            sensor_insights = system_manager.iot_manager.get_sensor_insights(selected_trainset)
            
            if sensor_insights:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Health Score", f"{sensor_insights['health_score']:.1f}%")
                    st.metric("Overall Status", sensor_insights['overall_status'])
                
                with col2:
                    if sensor_insights['anomaly']:
                        st.warning(f"🚨 Anomaly Detected (Score: {sensor_insights['anomaly']['anomaly_score']:.2f})")
                    else:
                        st.success("✅ No anomalies detected")
                
                # Sensor details
                st.write("**Sensor Readings:**")
                sensors_data = sensor_insights['sensors']
                
                # Create a properly formatted DataFrame
                sensor_rows = []
                for sensor_type, data in sensors_data.items():
                    sensor_rows.append({
                        'Sensor': sensor_type.title(),
                        'Current Value': f"{data['current']:.2f}",
                        'Threshold': f"{data['threshold']:.2f}",
                        'Status': data['status'],
                        'Last Update': data['last_update'].strftime('%H:%M:%S') if isinstance(data['last_update'], datetime) else str(data['last_update'])
                    })
                
                sensors_df = pd.DataFrame(sensor_rows)
                st.dataframe(sensors_df, use_container_width=True)
                
                # Sensor alerts for this trainset
                if sensor_insights['alerts']:
                    st.write("**Alerts for this Trainset:**")
                    alerts_df = pd.DataFrame(sensor_insights['alerts'])
                    st.dataframe(alerts_df, use_container_width=True)

def create_smart_stations_section(system_manager):
    """Create smart stations management section"""
    st.subheader("🏢 Smart Stations Management")
    
    # Get station summary
    station_summary = system_manager.station_manager.get_fleet_station_summary()
    
    # Overall metrics
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
    st.subheader("📊 Station Health Overview")
    
    if station_summary['stations']:
        stations_df = pd.DataFrame(station_summary['stations'])
        
        # Health score distribution
        fig = px.bar(stations_df, x='station_name', y='health_score',
                    title="Station Health Scores",
                    color='health_score',
                    color_continuous_scale='RdYlGn')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Station status distribution
        status_counts = stations_df['status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                    title="Station Status Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    # Crowd density alerts
    if station_summary['crowd_alerts']:
        st.subheader("👥 Crowd Density Alerts")
        
        crowd_alerts_df = pd.DataFrame(station_summary['crowd_alerts'])
        st.dataframe(crowd_alerts_df, use_container_width=True)
        
        # Crowd density chart
        fig = px.bar(crowd_alerts_df, x='station_name', y='crowd_density',
                    title="Crowd Density by Station",
                    color='severity',
                    color_discrete_map={'High': 'red', 'Medium': 'orange'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No crowd density alerts")
    
    # Individual station details
    st.subheader("🏢 Individual Station Details")
    
    if station_summary['stations']:
        selected_station = st.selectbox("Select Station", 
                                       [s['station_id'] for s in station_summary['stations']])
        
        if selected_station:
            station_analytics = system_manager.station_manager.get_station_analytics(selected_station)
            
            if station_analytics:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Crowd Density", f"{station_analytics['current_crowd_density']:.1%}")
                    st.metric("Health Score", f"{station_analytics['health_score']:.1f}%")
                
                with col2:
                    st.write("**Facility Utilization:**")
                    for facility, util in station_analytics['facility_utilization'].items():
                        st.write(f"• {facility.title()}: {util:.1%}")
                
                # Recommendations
                if station_analytics['recommendations']:
                    st.write("**Recommendations:**")
                    for rec in station_analytics['recommendations']:
                        priority_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                        st.write(f"{priority_color.get(rec['priority'], '⚪')} **{rec['facility']}**: {rec['action']}")
                        st.write(f"   *{rec['reason']}*")
