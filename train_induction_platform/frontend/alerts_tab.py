from common_imports import *

def create_alerts_tab():
    """Create the alerts and notifications tab"""
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
        margin-bottom: 10px;
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
    }
    .metric-delta {
        font-size: 14px;
        color: #28a745;
    }
    </style>
    """, unsafe_allow_html=True)

    st.header("⚠️ Alerts & Notifications")
    if 'current_alerts' in st.session_state:
        alerts = st.session_state.current_alerts
        if not alerts:
            st.success("🎉 No active alerts!")
            return
        # Alert summary
        critical_alerts = [a for a in alerts if a['priority'] == 'Critical']
        high_alerts = [a for a in alerts if a['priority'] == 'High']
        medium_alerts = [a for a in alerts if a['priority'] == 'Medium']
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #f8d7da; color: #721c24;">
                <div class="metric-title">Critical Alerts</div>
                <div class="metric-value">{len(critical_alerts)}</div>
                <div class="metric-delta">&nbsp;</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #fff3cd; color: #856404;">
                <div class="metric-title">High Priority</div>
                <div class="metric-value">{len(high_alerts)}</div>
                <div class="metric-delta">&nbsp;</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #d1ecf1; color: #0c5460;">
                <div class="metric-title">Medium Priority</div>
                <div class="metric-value">{len(medium_alerts)}</div>
                <div class="metric-delta">&nbsp;</div>
            </div>
            """, unsafe_allow_html=True)

        # Display alerts by priority
        for priority, alert_list in [('Critical', critical_alerts), ('High', high_alerts), ('Medium', medium_alerts)]:
            if alert_list:
                st.subheader(f"{priority} Priority Alerts")
                
                for alert in alert_list:
                    alert_class = f"alert-{priority.lower()}"
                    st.markdown(f"""
                    <div class="metric-card {alert_class}">
                        <strong>{alert['type'].replace('_', ' ').title()}</strong><br>
                        {alert['message']}<br>
                        <small>Time: {alert['timestamp'].strftime('%H:%M:%S')}</small>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Run AI optimization to generate alerts")