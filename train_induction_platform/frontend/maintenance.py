from common_imports import *

def create_maintenance_tab():
    """Create the maintenance planning tab"""
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

    st.header("🔧 Predictive Maintenance Dashboard")

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
    else:
        st.info("Run AI optimization to generate maintenance predictions")

