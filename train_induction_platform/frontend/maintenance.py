from common_imports import *

def create_maintenance_tab():
    """Create the maintenance planning tab with integrated analytics"""
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
        width: 100%;
        height: 150px;
    }
    .metric-card:hover {
        transform: scale(1.03);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .metric-title {
        font-size: 16px;
        font-weight: 600;
        color: #333;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #dc3545;
    }
    .metric-delta {
        font-size: 14px;
        color: #28a745;
    }
    </style>
    """, unsafe_allow_html=True)

    st.header("🔧 Predictive Maintenance & Analytics Dashboard")
    
    # Initialize system manager
    if 'system_manager' not in st.session_state:
        st.error("System not initialized. Please refresh the page.")
        return
    
    system_manager = st.session_state.system_manager
    trainsets = st.session_state.trainsets

    if 'maintenance_predictions' in st.session_state:
        predictions_df = st.session_state.maintenance_predictions

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            critical_count = len(predictions_df[predictions_df['priority'] == 'High'])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Critical Maintenance</div>
                <div class="metric-value">{critical_count}</div>
                <div class="metric-delta">&nbsp;</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            avg_risk = predictions_df['risk_score'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Avg Risk Score</div>
                <div class="metric-value">{avg_risk:.1f}</div>
                <div class="metric-delta">&nbsp;</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            immediate_action = len(predictions_df[predictions_df['recommended_action'] == 'Schedule Immediately'])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Immediate Action</div>
                <div class="metric-value">{immediate_action}</div>
                <div class="metric-delta">&nbsp;</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            avg_days = predictions_df['days_until_maintenance'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Avg Days to Maintenance</div>
                <div class="metric-value">{avg_days:.1f}</div>
                <div class="metric-delta">&nbsp;</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Risk distribution chart
        fig = px.histogram(predictions_df, x='risk_score', nbins=10, 
                          title="Maintenance Risk Distribution")
        fig.update_layout(bargap=0.3)
        st.plotly_chart(fig, use_container_width=True)
        
        # Maintenance planning table
        st.subheader("Maintenance Schedule")
        # Color coding for priorities
        def color_priority(val):
            colors = {'High': 'background-color: #ffcccc', 
                     'Medium': 'background-color: #ffffcc', 
                     'Low': 'background-color: #ccffcc'}
            return colors.get(val, '')  
        styled_df = predictions_df.style.applymap(color_priority, subset=['priority'])
        st.dataframe(styled_df, use_container_width=True)
        
        # Advanced Maintenance Analytics
        st.subheader("📊 Advanced Maintenance Analytics")
        
        if trainsets:
            # Maintenance predictions
            maintenance_predictions = system_manager.ml_model.predict_maintenance(trainsets)
            
            if not maintenance_predictions.empty:
                # Additional analytics metrics
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
                
                # Severity analysis
                st.write("**Severity Level Analysis:**")
                severity_counts = maintenance_predictions['severity_level'].value_counts()
                fig = px.pie(values=severity_counts.values, names=severity_counts.index,
                            title="Maintenance Severity Distribution")
                st.plotly_chart(fig, use_container_width=True)
                
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
        
        # Maintenance cost trends
        st.subheader("💰 Maintenance Cost Trends")
        
        # Generate sample cost trend data
        months = pd.date_range(start='2024-01-01', periods=12, freq='M')
        sample_costs = np.random.normal(50000, 10000, 12)
        
        cost_trend_df = pd.DataFrame({
            'month': months,
            'cost': sample_costs
        })
        
        fig = px.line(cost_trend_df, x='month', y='cost',
                     title="Monthly Maintenance Cost Trends")
        st.plotly_chart(fig, use_container_width=True)
        
        # Maintenance efficiency metrics
        st.subheader("⚡ Maintenance Efficiency Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Preventive vs Reactive Maintenance**")
            maintenance_types = ['Preventive', 'Reactive', 'Emergency']
            maintenance_counts = [65, 25, 10]  # Sample data
            
            fig = px.pie(values=maintenance_counts, names=maintenance_types,
                        title="Maintenance Type Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Maintenance Completion Rates**")
            completion_data = {
                'On Time': 78,
                'Delayed': 15,
                'Overdue': 7
            }
            
            fig = px.bar(x=list(completion_data.keys()), y=list(completion_data.values()),
                        title="Maintenance Completion Rates")
            st.plotly_chart(fig, use_container_width=True)
        
        # Export functionality
        st.subheader("📤 Export Maintenance Data")
        
        if st.button("📊 Export Maintenance Report"):
            # Create comprehensive maintenance report
            report_data = {
                'total_trainsets': len(trainsets),
                'critical_maintenance': critical_count,
                'avg_risk_score': avg_risk,
                'immediate_actions': immediate_action,
                'avg_days_to_maintenance': avg_days,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            report_df = pd.DataFrame([report_data])
            csv_data = report_df.to_csv(index=False)
            
            st.download_button(
                label="Download Maintenance Report",
                data=csv_data,
                file_name=f"maintenance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("Run AI optimization to generate maintenance predictions")

