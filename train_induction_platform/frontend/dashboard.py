from common_imports import *

def create_dashboard_tab():
    """Create the main dashboard tab with hover cards."""
    
    # Enhanced Dashboard CSS
    st.markdown("""
    <style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 0 0 1px rgba(255,255,255,0.2),
            inset 0 1px 0 rgba(255,255,255,0.3);
    }
    
    .metric-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #6c757d;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-delta {
        font-size: 0.85rem;
        color: #28a745;
        font-weight: 600;
        background: rgba(40, 167, 69, 0.1);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        border: 1px solid rgba(40, 167, 69, 0.2);
    }
    
    .metric-delta.negative {
        color: #dc3545;
        background: rgba(220, 53, 69, 0.1);
        border-color: rgba(220, 53, 69, 0.2);
    }
    
    .section-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1.5rem 0 1rem 0;
        border-left: 4px solid #667eea;
        font-size: 1.2rem;
        font-weight: 600;
        color: #495057;
    }
    
    .weather-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    .activity-item {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .activity-item:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    
    # Enhanced Dashboard Header
    st.markdown("""
    <div class="dashboard-header">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">📊 Real-time Fleet Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.95; font-size: 1.2rem; font-weight: 400;">Live monitoring and analytics for your metro fleet</p>
        <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">
                🔴 Live Data
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">
                ⚡ Real-time Updates
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 500;">
                📈 Performance Metrics
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    trainsets = st.session_state.trainsets

    with col1:
        service_count = sum(1 for t in trainsets if t['recommendation'] == 'Service')
        delta_service = f"{service_count/len(trainsets)*100:.1f}%"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🚆 Service Ready</div>
            <div class="metric-value">{service_count}</div>
            <div class="metric-delta">↑ {delta_service}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        standby_count = sum(1 for t in trainsets if t['recommendation'] == 'Standby')
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">⏸️ Standby</div>
            <div class="metric-value">{standby_count}</div>
            <div class="metric-delta">Ready</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        ibl_count = sum(1 for t in trainsets if t['recommendation'] == 'IBL')
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🔧 IBL</div>
            <div class="metric-value">{ibl_count}</div>
            <div class="metric-delta">In Service</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        fitness_valid = sum(1 for t in trainsets if t['fitness']['overall_valid'])
        delta_fitness = f"{fitness_valid/len(trainsets)*100:.1f}%"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">✅ Fitness Valid</div>
            <div class="metric-value">{fitness_valid}</div>
            <div class="metric-delta">↑ {delta_fitness}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        avg_score = sum(t['ai_score'] for t in trainsets) / len(trainsets)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg AI Score</div>
            <div class="metric-value">{avg_score:.1f}</div>
            <div class="metric-delta">&nbsp;</div>
        </div>
        """, unsafe_allow_html=True)

    # Fleet status visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Fleet Status Distribution")
        
        # Create status distribution chart
        status_data = pd.DataFrame([
            {'Status': 'Service', 'Count': service_count, 'Color': '#28a745'},
            {'Status': 'Standby', 'Count': standby_count, 'Color': '#ffc107'},
            {'Status': 'IBL', 'Count': ibl_count, 'Color': '#dc3545'}
        ])
        
        fig = px.pie(status_data, values='Count', names='Status', 
                    color='Status', 
                    color_discrete_map={'Service': '#28a745', 'Standby': '#ffc107', 'IBL': '#dc3545'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Performers")
        top_trains = sorted(trainsets, key=lambda x: x['ai_score'], reverse=True)[:5]
        
        for i, train in enumerate(top_trains, 1):
            status_class = f"status-{train['recommendation'].lower()}"
            st.markdown(f"""
            <div class="trainset-card {status_class}">
                <strong>#{i} {train['id']}</strong><br>
                Score: {train['ai_score']}<br>
                Status: {train['recommendation']}
            </div>
            """, unsafe_allow_html=True)
    
    # Weather monitoring section
    st.subheader("🌤️ Weather Monitoring")
    
    # Initialize system manager for weather data
    if 'system_manager' in st.session_state:
        system_manager = st.session_state.system_manager
        
        # Get weather insights
        weather_insights = system_manager.weather_integrator.get_weather_insights()
        
        if weather_insights:
            current_weather = weather_insights.get('current_weather', {})
            
            if current_weather:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Current Temperature", f"{current_weather.get('temperature', 0):.1f}°C")
                
                with col2:
                    st.metric("Humidity", f"{current_weather.get('humidity', 0):.1f}%")
                
                with col3:
                    st.metric("Wind Speed", f"{current_weather.get('wind_speed', 0):.1f} m/s")
                
                with col4:
                    weather_status = current_weather.get('weather_condition', 'Unknown')
                    status_color = {
                        'Sunny': '🟡',
                        'Cloudy': '⚪',
                        'Rainy': '🔵',
                        'Stormy': '🔴',
                        'Clear': '🟡',
                        'Clouds': '⚪',
                        'Rain': '🔵',
                        'Thunderstorm': '🔴'
                    }.get(weather_status, '⚪')
                    st.metric("Weather Condition", f"{status_color} {weather_status}")
            else:
                st.info("🌤️ Weather data not available. Please check your weather API configuration.")
            
            # Weather impact on operations
            st.write("**Weather Impact on Operations:**")
            impact_factor = weather_insights.get('impact_factor', 0)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Overall Impact Factor", f"{impact_factor:.2f}")
            with col_b:
                st.metric("Weather Condition", current_weather.get('weather_description', 'Unknown'))
            with col_c:
                st.metric("Data Source", current_weather.get('data_source', 'Unknown'))
            
            # Weather forecast
            st.write("**7-Day Weather Forecast:**")
            forecast_data = weather_insights.get('forecast', [])
            
            if forecast_data:
                forecast_df = pd.DataFrame(forecast_data)
                fig = px.line(forecast_df, x='datetime', y='temperature',
                             title="Temperature Forecast",
                             labels={'temperature': 'Temperature (°C)', 'datetime': 'Date & Time'})
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Weather data not available")
    
    # Recent activity timeline
    st.subheader("Recent System Activity")
    activity_data = []
    
    # Simulate recent activities
    for i in range(5):
        activity_data.append({
            'Time': datetime.now() - timedelta(minutes=random.randint(1, 60)),
            'Activity': random.choice([
                'Fitness certificate updated',
                'Job card closed',
                'Maintenance scheduled',
                'Branding assignment changed',
                'IOT sensor data received',
                'Weather data updated'
            ]),
            'Trainset': random.choice([t['id'] for t in trainsets[:10]])
        })
    
    activity_df = pd.DataFrame(activity_data)
    st.dataframe(activity_df, use_container_width=True)

if __name__ == "__main__":
    create_dashboard_tab()