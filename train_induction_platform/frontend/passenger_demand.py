from common_imports import *

def create_passenger_demand_tab():
    """Create the passenger demand forecasting tab"""
    st.header("🚆 Passenger Demand Forecasting")
    
    # Initialize system manager if not exists
    if 'system_manager' not in st.session_state:
        st.error("System not initialized. Please refresh the page.")
        return
    
    system_manager = st.session_state.system_manager
    
    # Main interface
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
        
        # Historical demand trends
        st.write("**Historical Demand Trends**")
        
        # Generate sample historical data for visualization
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        sample_demand = np.random.normal(1000, 200, len(dates))
        
        # Add seasonal patterns
        seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * np.arange(len(dates)) / 365)
        sample_demand = sample_demand * seasonal_factor
        
        historical_df = pd.DataFrame({
            'date': dates,
            'demand': sample_demand
        })
        
        fig = px.line(historical_df, x='date', y='demand',
                     title="Historical Passenger Demand Trends")
        st.plotly_chart(fig, use_container_width=True)
        
        # Peak hour analysis
        st.write("**Peak Hour Analysis**")
        hours = list(range(24))
        hourly_demand = [800 + 300 * np.sin(2 * np.pi * h / 24) + np.random.normal(0, 50) for h in hours]
        
        hourly_df = pd.DataFrame({
            'hour': hours,
            'demand': hourly_demand
        })
        
        fig = px.bar(hourly_df, x='hour', y='demand',
                    title="Average Hourly Demand Pattern")
        fig.update_xaxes(title_text="Hour of Day")
        fig.update_yaxes(title_text="Passenger Demand")
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional analytics section
    st.subheader("📊 Demand Analytics")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("**Demand Patterns by Day of Week**")
        
        # Generate sample weekly data
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_demand = [1200, 1300, 1250, 1350, 1400, 1000, 800]  # Weekend lower
        
        weekly_df = pd.DataFrame({
            'day': days,
            'demand': weekly_demand
        })
        
        fig = px.bar(weekly_df, x='day', y='demand',
                    title="Average Daily Demand by Day of Week")
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        st.write("**Demand Forecasting Accuracy**")
        
        # Sample accuracy metrics
        accuracy_metrics = {
            'Model': ['ARIMA', 'Prophet', 'LSTM', 'Random Forest'],
            'RMSE': [45.2, 38.7, 42.1, 41.5],
            'MAE': [32.1, 28.9, 30.4, 29.8],
            'R²': [0.89, 0.92, 0.90, 0.91]
        }
        
        accuracy_df = pd.DataFrame(accuracy_metrics)
        st.dataframe(accuracy_df, use_container_width=True)
        
        # Best model recommendation
        best_model = accuracy_df.loc[accuracy_df['R²'].idxmax()]
        st.success(f"**Best Model:** {best_model['Model']} (R² = {best_model['R²']:.2f})")
    
    # Export functionality
    st.subheader("📤 Export Demand Data")
    
    if st.button("📊 Export Demand Report"):
        # Generate comprehensive demand report
        report_data = {
            'station': station_name,
            'forecast_hours': hours_ahead,
            'total_predicted_demand': total_demand if 'total_demand' in locals() else 0,
            'peak_hours': peak_hours if 'peak_hours' in locals() else 0,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        report_df = pd.DataFrame([report_data])
        csv_data = report_df.to_csv(index=False)
        
        st.download_button(
            label="Download Demand Report",
            data=csv_data,
            file_name=f"demand_report_{station_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
