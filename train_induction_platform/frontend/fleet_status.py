from common_imports import *

def create_fleet_status_tab():
    """Create the fleet status tab"""
    st.header("🚆 Fleet Status Overview")
    trainsets = st.session_state.trainsets
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        depot_filter = st.selectbox("Filter by Depot", ["All"] + list(set(t['depot'] for t in trainsets)))
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Service", "Standby", "IBL"])
    with col3:
        sort_by = st.selectbox("Sort by", ["AI Score", "ID", "Fitness Expiry"])
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
    # Display trainsets in a grid
    cols_per_row = 3
    for i in range(0, len(filtered_trainsets), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, train in enumerate(filtered_trainsets[i:i+cols_per_row]):
            with cols[j]:
                create_trainset_card(train)

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