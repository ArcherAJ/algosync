from common_imports import *

def create_analytics_tab():
    """Create the analytics and trends tab"""
    st.header("📈 Analytics & Performance Trends")
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