from common_imports import *

def create_fleet_status_tab():
    """Create the fleet status tab with integrated performance analytics"""
    st.header("🚆 Fleet Status & Performance Overview")
    trainsets = st.session_state.trainsets
    
    # Initialize system manager
    if 'system_manager' not in st.session_state:
        st.error("System not initialized. Please refresh the page.")
        return
    
    system_manager = st.session_state.system_manager
    
    # Get fleet insights
    fleet_insights = system_manager.get_fleet_insights()
    
    if fleet_insights:
        # Overall metrics
        overall = fleet_insights['overall_metrics']
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Total Trainsets", overall['total_trainsets'])
        with col2:
            st.metric("Avg Performance", f"{overall['avg_performance']:.1f}")
        with col3:
            st.metric("High Performers", overall['high_performers'])
        with col4:
            st.metric("Anomalies Detected", overall['anomaly_count'])
        with col5:
            st.metric("⏰ Avg Punctuality", f"{overall['avg_punctuality']:.2f}%")
        with col6:
            st.metric("🚀 On-Time Performance", f"{overall['avg_on_time']:.2f}%")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        depot_filter = st.selectbox("Filter by Depot", ["All"] + list(set(t['depot'] for t in trainsets)))
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Service", "Standby", "IBL"])
    with col3:
        sort_by = st.selectbox("Sort by", ["AI Score", "ID", "Fitness Expiry", "Performance", "Punctuality"])
    
    # Apply filters
    filtered_trainsets = trainsets.copy()
    if depot_filter != "All":
        filtered_trainsets = [t for t in filtered_trainsets if t['depot'] == depot_filter]
    if status_filter != "All":
        filtered_trainsets = [t for t in filtered_trainsets if t['recommendation'] == status_filter]
    
    # Sort
    if sort_by == "AI Score":
        filtered_trainsets.sort(key=lambda x: x['ai_score'], reverse=True)
    elif sort_by == "Fitness Expiry":
        filtered_trainsets.sort(key=lambda x: x['fitness']['days_until_expiry'])
    elif sort_by == "Performance":
        # Sort by performance score if available
        filtered_trainsets.sort(key=lambda x: x.get('performance_score', 0), reverse=True)
    elif sort_by == "Punctuality":
        # Sort by punctuality score
        filtered_trainsets.sort(key=lambda x: x['operational'].get('punctuality_score', 99.5), reverse=True)
    
    # Performance clusters section
    if fleet_insights and fleet_insights.get('clusters'):
        st.subheader("📈 Performance Clusters")
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
    
    # Display trainsets in a grid
    st.subheader("🚆 Fleet Overview")
    cols_per_row = 3
    for i in range(0, len(filtered_trainsets), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, train in enumerate(filtered_trainsets[i:i+cols_per_row]):
            with cols[j]:
                create_trainset_card(train)
    
    # Top performers section
    if fleet_insights and fleet_insights.get('top_performers'):
        st.subheader("🏆 Top Performers")
        top_performers = fleet_insights['top_performers'][:10]
        top_df = pd.DataFrame([{
            'trainset_id': p['trainset_id'],
            'performance_score': p['performance_score'],
            'depot': p['depot'],
            'status': p['status']
        } for p in top_performers])
        st.dataframe(top_df, use_container_width=True)
    
    # Anomalies section
    if fleet_insights and fleet_insights.get('anomalies'):
        st.subheader("⚠️ Detected Anomalies")
        anomalies = fleet_insights['anomalies'][:5]
        anomaly_df = pd.DataFrame([{
            'trainset_id': a['trainset_id'],
            'performance_score': a['performance_score'],
            'depot': a['depot'],
            'status': a['status']
        } for a in anomalies])
        st.dataframe(anomaly_df, use_container_width=True)
    
    # Depot analysis
    if fleet_insights and fleet_insights.get('depot_analysis'):
        st.subheader("🏢 Depot Performance Analysis")
        depot_analysis = fleet_insights['depot_analysis']
        depot_df = pd.DataFrame([{
            'depot': depot,
            'count': data['count'],
            'avg_performance': data['avg_performance']
        } for depot, data in depot_analysis.items()])
        
        fig = px.bar(depot_df, x='depot', y='avg_performance',
                    title="Average Performance by Depot")
        st.plotly_chart(fig, use_container_width=True)
    
    # Punctuality Analysis Section
    if fleet_insights:
        st.subheader("⏰ Punctuality Analysis")
        overall = fleet_insights['overall_metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Excellent (≥99.7%)", overall['punctuality_excellent'])
        with col2:
            st.metric("Good (99.5-99.7%)", overall['punctuality_good'])
        with col3:
            st.metric("Average Punctuality", f"{overall['avg_punctuality']:.2f}%")
        with col4:
            st.metric("On-Time Performance", f"{overall['avg_on_time']:.2f}%")
        
        # Punctuality distribution chart
        punctuality_data = []
        for trainset in filtered_trainsets:
            punctuality_data.append({
                'trainset_id': trainset['id'],
                'punctuality': trainset['operational'].get('punctuality_score', 99.5),
                'depot': trainset['depot'],
                'status': trainset['recommendation']
            })
        
        if punctuality_data:
            punct_df = pd.DataFrame(punctuality_data)
            
            # Create punctuality distribution chart
            fig = px.histogram(punct_df, x='punctuality', 
                             title="Punctuality Score Distribution",
                             labels={'punctuality': 'Punctuality Score (%)', 'count': 'Number of Trainsets'},
                             nbins=20)
            fig.add_vline(x=99.5, line_dash="dash", line_color="green", 
                         annotation_text="Target: 99.5%")
            fig.add_vline(x=99.7, line_dash="dash", line_color="blue", 
                         annotation_text="Excellent: 99.7%")
            st.plotly_chart(fig, use_container_width=True)
            
            # Top punctuality performers
            st.write("**🏆 Top Punctuality Performers:**")
            top_punctuality = punct_df.nlargest(10, 'punctuality')
            st.dataframe(top_punctuality[['trainset_id', 'punctuality', 'depot', 'status']], 
                        use_container_width=True)
    
    # AI Recommendations
    if fleet_insights and fleet_insights.get('recommendations'):
        st.subheader("🤖 AI Recommendations")
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

def create_trainset_card(train):
    """Create a detailed trainset card"""
    status_colors = {
        'Service': "#31ee5d",
        'Standby': "#e4c560",
        'IBL': "#f74957"
    }
    bg_color = status_colors.get(train['recommendation'], '#f8f9fa')
    # Override controls
    with st.expander(f"🚆 {train['id']} (Score: {train['ai_score']})"):
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <strong>Current Recommendation: {train['recommendation']}</strong>
        </div>
        """, unsafe_allow_html=True)
        # Key details
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Depot:** {train['depot']}")
            st.write(f"**Fitness:** {'✅' if train['fitness']['overall_valid'] else '❌'}")
            st.write(f"**Open Jobs:** {train['job_cards']['open']}")
        with col2:
            st.write(f"**Reliability:** {train['operational']['reliability_score']}%")
            wear_avg = sum(train['mileage']['component_wear'].values()) / 3
            st.write(f"**Avg Wear:** {wear_avg:.1f}%")
            st.write(f"**Days to Fitness Expiry:** {train['fitness']['days_until_expiry']}")
            st.write(f"**⏰ Punctuality:** {train['operational'].get('punctuality_score', 99.5):.2f}%")
        # Manual override
        st.subheader("Manual Override")
        override_status = st.selectbox(
            "Override Recommendation", 
            ["None", "Service", "Standby", "IBL"], 
            key=f"override_{train['id']}",
            index=0 if not train.get('manual_override') else ["None", "Service", "Standby", "IBL"].index(train.get('manual_override'))
        )
        override_reason = st.text_area(
            "Reason for Override", 
            value=train.get('override_reason', ''),
            key=f"reason_{train['id']}"
        )
        if st.button(f"Apply Override", key=f"apply_{train['id']}"):
            if override_status != "None":
                train['manual_override'] = override_status
                train['override_reason'] = override_reason
                st.success(f"Override applied: {train['id']} → {override_status}")
            else:
                train['manual_override'] = None
                train['override_reason'] = ''
                st.info("Override removed")