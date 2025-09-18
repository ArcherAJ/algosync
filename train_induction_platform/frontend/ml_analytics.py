from common_imports import *

def create_ml_analytics_tab():
    """Create the ML Analytics tab with comprehensive ML insights"""
    st.header("🤖 ML Analytics & Insights")
    
    # Initialize system manager if not exists
    if 'system_manager' not in st.session_state:
        st.error("System not initialized. Please refresh the page.")
        return
    
    system_manager = st.session_state.system_manager
    
    # ML Models Overview
    st.subheader("📊 ML Models Performance")
    
    # Get ML insights
    ml_insights = system_manager.get_ml_insights()
    
    if ml_insights:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if ml_insights['maintenance_model']:
                st.metric(
                    "Maintenance Prediction",
                    "✅ Trained" if ml_insights['maintenance_model']['is_trained'] else "❌ Not Trained",
                    "Random Forest + Gradient Boosting"
                )
        
        with col2:
            if ml_insights['demand_predictor']:
                demand_perf = ml_insights['demand_predictor']['demand_prediction']
                st.metric(
                    "Demand Forecasting",
                    f"R² = {demand_perf['r2']:.3f}",
                    demand_perf['model_type']
                )
        
        with col3:
            if ml_insights['energy_optimizer']:
                energy_perf = ml_insights['energy_optimizer']['energy_prediction']
                st.metric(
                    "Energy Optimization",
                    f"R² = {energy_perf['r2']:.3f}",
                    energy_perf['model_type']
                )
        
        with col4:
            if ml_insights['fleet_analytics']:
                st.metric(
                    "Fleet Analytics",
                    "✅ Active" if ml_insights['fleet_analytics']['is_trained'] else "❌ Inactive",
                    f"{ml_insights['fleet_analytics']['total_trainsets_analyzed']} trainsets"
                )
    
    # Tabs for different ML modules
    tab1, tab2, tab3, tab4 = st.tabs([
        "🚆 Passenger Demand", "⚡ Energy Optimization", 
        "🔧 Maintenance Analytics", "📈 Fleet Performance"
    ])
    
    with tab1:
        create_passenger_demand_section(system_manager)
    
    with tab2:
        create_energy_optimization_section(system_manager)
    
    with tab3:
        create_maintenance_analytics_section(system_manager)
    
    with tab4:
        create_fleet_performance_section(system_manager)

def create_passenger_demand_section(system_manager):
    """Create passenger demand forecasting section"""
    st.subheader("🚆 Passenger Demand Forecasting")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Demand Prediction Interface**")
        
        station_name = st.selectbox(
            "Select Station",
            ["Aluva", "Pulinchodu", "Companypady", "Ambattukavu", "Muttom", "Kalamassery"]
        )
        
        hours_ahead = st.slider("Forecast Hours Ahead", 1, 48, 24)
        
        if st.button("🔮 Generate Demand Forecast"):
            forecast = system_manager.get_demand_forecast(station_name, hours_ahead)
            
            if forecast:
                st.success("✅ Demand forecast generated!")
                
                # Display forecast summary
                total_demand = sum(item['predicted_demand'] for item in forecast)
                peak_hours = len([item for item in forecast if item['is_peak_hour']])
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Total Predicted Demand", f"{total_demand:,}")
                with col_b:
                    st.metric("Peak Hours", peak_hours)
                
                # Create forecast chart
                forecast_df = pd.DataFrame(forecast)
                fig = px.line(forecast_df, x='time_slot', y='predicted_demand',
                             title=f"Demand Forecast for {station_name}",
                             color='is_peak_hour',
                             color_discrete_map={True: 'red', False: 'blue'})
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)
                
                # Display detailed forecast table
                st.write("**Detailed Forecast:**")
                st.dataframe(forecast_df[['time_slot', 'predicted_demand', 'is_peak_hour', 'peak_probability']])
            else:
                st.error("❌ Failed to generate demand forecast")
    
    with col2:
        st.write("**Station Insights**")
        
        # Get station insights
        insights = system_manager.demand_predictor.get_station_insights("Aluva")
        if insights:
            st.write(f"**{insights['station_name']} Station Analysis:**")
            st.metric("Average Daily Passengers", f"{insights['avg_daily_passengers']:,.0f}")
            st.metric("Peak Hour Demand", f"{insights['peak_hour_demand']:,.0f}")
            st.metric("Off-Peak Demand", f"{insights['off_peak_demand']:,.0f}")
            st.write(f"**Busiest Hour:** {insights['busiest_hour']}")

def create_energy_optimization_section(system_manager):
    """Create energy optimization section"""
    st.subheader("⚡ Energy Consumption Optimization")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Energy Optimization Interface**")
        
        distance_km = st.number_input("Distance (km)", min_value=1, max_value=1000, value=100)
        passengers = st.number_input("Passengers", min_value=1, max_value=10000, value=1000)
        month = st.selectbox("Month", range(1, 13), index=8)  # Default to September
        
        if st.button("⚡ Optimize Energy"):
            optimization = system_manager.get_energy_optimization(distance_km, passengers, month)
            
            if optimization:
                st.success("✅ Energy optimization completed!")
                
                # Display optimization results
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Predicted Energy", f"{optimization['predicted_energy_kwh']:,.0f} kWh")
                with col_b:
                    st.metric("Predicted Cost", f"₹{optimization['predicted_cost']:,.0f}")
                with col_c:
                    st.metric("Optimal Renewable %", f"{optimization['optimal_renewable_percentage']:.1f}%")
                
                # Display efficiency metrics
                st.write("**Efficiency Metrics:**")
                col_d, col_e = st.columns(2)
                with col_d:
                    st.metric("Efficiency Score", f"{optimization['efficiency_score']:.2f}")
                with col_e:
                    st.metric("Energy per Passenger", f"{optimization['energy_per_passenger']:.3f} kWh")
                
                # Display recommendations
                st.write("**Optimization Recommendations:**")
                for rec in optimization['recommendations']:
                    st.write(f"• {rec}")
                
                # Display savings potential
                st.write("**Savings Potential:**")
                savings = optimization['savings_potential']
                col_f, col_g, col_h = st.columns(3)
                with col_f:
                    st.metric("Renewable Optimization", f"₹{savings['renewable_optimization']:,.0f}")
                with col_g:
                    st.metric("Efficiency Improvement", f"₹{savings['efficiency_improvement']:,.0f}")
                with col_h:
                    st.metric("Maintenance Optimization", f"₹{savings['maintenance_optimization']:,.0f}")
            else:
                st.error("❌ Failed to generate energy optimization")
    
    with col2:
        st.write("**Monthly Energy Forecast**")
        
        if st.button("📅 Generate Monthly Forecast"):
            forecast = system_manager.energy_optimizer.get_monthly_forecast(2024, month)
            
            if forecast:
                st.success("✅ Monthly forecast generated!")
                
                # Display monthly forecast
                col_i, col_j, col_k = st.columns(3)
                with col_i:
                    st.metric("Monthly Energy", f"{forecast['predicted_energy_kwh']:,.0f} kWh")
                with col_j:
                    st.metric("Monthly Cost", f"₹{forecast['predicted_cost']:,.0f}")
                with col_k:
                    st.metric("Efficiency Score", f"{forecast['efficiency_score']:.2f}")

def create_maintenance_analytics_section(system_manager):
    """Create maintenance analytics section"""
    st.subheader("🔧 Maintenance Analytics")
    
    trainsets = st.session_state.trainsets
    
    if trainsets:
        # Maintenance predictions
        maintenance_predictions = system_manager.ml_model.predict_maintenance(trainsets)
        
        if not maintenance_predictions.empty:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                high_risk = len(maintenance_predictions[maintenance_predictions['risk_score'] > 75])
                st.metric("High Risk Trainsets", high_risk)
            
            with col2:
                avg_cost = maintenance_predictions['predicted_cost'].mean()
                st.metric("Avg Predicted Cost", f"₹{avg_cost:,.0f}")
            
            with col3:
                critical_severity = len(maintenance_predictions[maintenance_predictions['severity_level'] == 'Critical'])
                st.metric("Critical Severity", critical_severity)
            
            with col4:
                total_cost = maintenance_predictions['predicted_cost'].sum()
                st.metric("Total Predicted Cost", f"₹{total_cost:,.0f}")
            
            # Risk distribution chart
            st.write("**Risk Score Distribution:**")
            fig = px.histogram(maintenance_predictions, x='risk_score', 
                             title="Maintenance Risk Score Distribution",
                             nbins=20)
            st.plotly_chart(fig, use_container_width=True)
            
            # Severity analysis
            st.write("**Severity Level Analysis:**")
            severity_counts = maintenance_predictions['severity_level'].value_counts()
            fig = px.pie(values=severity_counts.values, names=severity_counts.index,
                        title="Maintenance Severity Distribution")
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed maintenance table
            st.write("**Detailed Maintenance Predictions:**")
            st.dataframe(maintenance_predictions[['trainset_id', 'risk_score', 'predicted_cost', 
                                                'severity_level', 'recommended_action']])
            
            # Individual trainset analysis
            st.write("**Individual Trainset Analysis:**")
            selected_trainset_id = st.selectbox("Select Trainset", maintenance_predictions['trainset_id'].tolist())
            
            if selected_trainset_id:
                selected_trainset = next(t for t in trainsets if t['id'] == selected_trainset_id)
                
                # Get detailed predictions
                cost_prediction = system_manager.predict_maintenance_cost(selected_trainset)
                severity_prediction = system_manager.predict_failure_severity(selected_trainset)
                
                if cost_prediction and severity_prediction:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Predicted Maintenance Cost", f"₹{cost_prediction:,.0f}")
                    with col_b:
                        st.metric("Severity Level", severity_prediction['severity_level'])
                    
                    st.write("**Severity Probabilities:**")
                    for level, prob in severity_prediction['probabilities'].items():
                        st.write(f"• {level}: {prob:.1%}")

def create_fleet_performance_section(system_manager):
    """Create fleet performance analytics section"""
    st.subheader("📈 Fleet Performance Analytics")
    
    trainsets = st.session_state.trainsets
    
    if trainsets:
        fleet_insights = system_manager.get_fleet_insights()
        
        if fleet_insights:
            # Overall metrics
            overall = fleet_insights['overall_metrics']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Trainsets", overall['total_trainsets'])
            with col2:
                st.metric("Avg Performance", f"{overall['avg_performance']:.1f}")
            with col3:
                st.metric("High Performers", overall['high_performers'])
            with col4:
                st.metric("Anomalies Detected", overall['anomaly_count'])
            
            # Performance clusters
            st.write("**Performance Clusters:**")
            clusters = fleet_insights['clusters']
            
            for cluster_id, cluster_data in clusters.items():
                with st.expander(f"Cluster {cluster_id} - Avg Performance: {cluster_data['avg_performance']:.1f}"):
                    char = cluster_data['cluster_characteristics']
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        st.metric("Cluster Size", char['cluster_size'])
                        st.metric("Avg Mileage", f"{char['avg_mileage']:,.0f} km")
                    with col_b:
                        st.metric("Avg Wear", f"{char['avg_wear']:.1f}%")
                        st.metric("Avg Efficiency", f"{char['avg_efficiency']:.2f}")
                    with col_c:
                        st.metric("Maintenance Urgency", f"{char['avg_maintenance_urgency']:.1f}")
                        st.metric("Fitness Score", f"{char['avg_fitness']:.2f}")
            
            # Top performers
            st.write("**Top Performers:**")
            top_performers = fleet_insights['top_performers'][:10]
            top_df = pd.DataFrame([{
                'trainset_id': p['trainset_id'],
                'performance_score': p['performance_score'],
                'depot': p['depot'],
                'status': p['status']
            } for p in top_performers])
            st.dataframe(top_df)
            
            # Anomalies
            if fleet_insights['anomalies']:
                st.write("**Detected Anomalies:**")
                anomalies = fleet_insights['anomalies'][:5]
                anomaly_df = pd.DataFrame([{
                    'trainset_id': a['trainset_id'],
                    'performance_score': a['performance_score'],
                    'depot': a['depot'],
                    'status': a['status']
                } for a in anomalies])
                st.dataframe(anomaly_df)
            
            # Depot analysis
            st.write("**Depot Performance Analysis:**")
            depot_analysis = fleet_insights['depot_analysis']
            depot_df = pd.DataFrame([{
                'depot': depot,
                'count': data['count'],
                'avg_performance': data['avg_performance']
            } for depot, data in depot_analysis.items()])
            
            fig = px.bar(depot_df, x='depot', y='avg_performance',
                        title="Average Performance by Depot")
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            st.write("**AI Recommendations:**")
            for rec in fleet_insights['recommendations']:
                st.write(f"• {rec}")
            
            # Export functionality
            if st.button("📤 Export Fleet Report"):
                fleet_df, insights = system_manager.fleet_analytics.export_fleet_report()
                csv_data = fleet_df.to_csv(index=False)
                st.download_button(
                    label="Download Fleet Analytics Report",
                    data=csv_data,
                    file_name="fleet_analytics_report.csv",
                    mime="text/csv"
                )
