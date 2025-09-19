from common_imports import *
from maximo_data_connector import MaximoDataConnector
from ibm_maximo_integration import IBMMaximoIntegration
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_maximo_dashboard():
    """Create comprehensive IBM Maximo integration dashboard"""
    st.markdown("""
    <style>
    .maximo-header {
        background: linear-gradient(90deg, #1f4e79, #2e5984);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-card-maximo {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        border-left: 4px solid #1f4e79;
        transition: transform 0.2s ease;
    }
    .metric-card-maximo:hover {
        transform: scale(1.02);
    }
    .status-connected {
        color: #28a745;
        font-weight: bold;
    }
    .status-disconnected {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="maximo-header">
        <h1>🔧 IBM Maximo Integration Dashboard</h1>
        <p>Comprehensive Asset Management & Maintenance Planning</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize Maximo data connector
    if 'maximo_connector' not in st.session_state:
        st.session_state.maximo_connector = MaximoDataConnector()
    
    connector = st.session_state.maximo_connector

    # Connection Status Section
    st.subheader("🔗 Connection Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔗 Connect to Maximo", key="connect_maximo_dashboard", type="primary"):
            with st.spinner("Connecting to IBM Maximo..."):
                connected = connector.connect_to_maximo()
                if connected:
                    st.success("✅ Connected to IBM Maximo")
                    st.session_state.maximo_connected = True
                else:
                    st.error("❌ Failed to connect to Maximo")
                    st.session_state.maximo_connected = False
    
    with col2:
        if st.button("📊 Load Datasets", key="load_datasets"):
            with st.spinner("Loading datasets..."):
                datasets = connector.load_existing_datasets()
                if datasets:
                    st.success(f"✅ Loaded {len(datasets)} datasets")
                    st.session_state.maximo_datasets = datasets
                else:
                    st.error("❌ Failed to load datasets")
    
    with col3:
        if st.button("🔄 Generate Results", key="generate_results"):
            with st.spinner("Generating comprehensive results..."):
                results = connector.generate_comprehensive_results()
                if results:
                    st.success("✅ Results generated successfully")
                    st.session_state.maximo_results = results
                else:
                    st.error("❌ Failed to generate results")

    # Show connection status
    if hasattr(connector, 'maximo_connected'):
        if connector.maximo_connected:
            if hasattr(connector, 'mock_server') and connector.mock_server:
                st.markdown('<p class="status-connected">✅ Mock IBM Maximo Connected (Demo Mode)</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p class="status-connected">✅ IBM Maximo Connected</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-disconnected">❌ IBM Maximo Disconnected</p>', unsafe_allow_html=True)

    # Results Display Section
    if 'maximo_results' in st.session_state:
        results = st.session_state.maximo_results
        
        # Summary Metrics
        st.subheader("📊 Summary Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if 'analytics' in results and 'fleet' in results['analytics']:
                fleet = results['analytics']['fleet']
                st.metric("Total Trainsets", fleet['total_trainsets'])
        
        with col2:
            if 'analytics' in results and 'fleet' in results['analytics']:
                fleet = results['analytics']['fleet']
                st.metric("Available Trainsets", fleet['available_trainsets'])
        
        with col3:
            if 'analytics' in results and 'fleet' in results['analytics']:
                fleet = results['analytics']['fleet']
                st.metric("Avg Reliability", f"{fleet['average_reliability']:.1f}%")
        
        with col4:
            if 'analytics' in results and 'maintenance' in results['analytics']:
                maint = results['analytics']['maintenance']
                st.metric("Total Job Cards", maint['high_priority_jobs'])

        # Sync Results
        if 'sync_results' in results:
            st.subheader("🔄 Synchronization Results")
            
            sync_tabs = st.tabs(["Trainsets", "Stations", "Summary"])
            
            with sync_tabs[0]:
                if 'trainsets' in results['sync_results']:
                    sync_data = results['sync_results']['trainsets']
                    if 'error' not in sync_data:
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Assets Created", sync_data['assets_created'])
                        with col2:
                            st.metric("Work Orders Created", sync_data['work_orders_created'])
                        with col3:
                            st.metric("Assets Updated", sync_data['assets_updated'])
                        
                        if sync_data['errors']:
                            st.error(f"Errors: {len(sync_data['errors'])}")
                            for error in sync_data['errors']:
                                st.error(f"• {error}")
                    else:
                        st.error(f"Sync Error: {sync_data['error']}")
            
            with sync_tabs[1]:
                if 'stations' in results['sync_results']:
                    sync_data = results['sync_results']['stations']
                    if 'error' not in sync_data:
                        st.metric("Facilities Created", sync_data['facilities_created'])
                        if sync_data['errors']:
                            st.error(f"Errors: {len(sync_data['errors'])}")
                            for error in sync_data['errors']:
                                st.error(f"• {error}")
                    else:
                        st.error(f"Sync Error: {sync_data['error']}")
            
            with sync_tabs[2]:
                total_assets = 0
                total_work_orders = 0
                
                for dataset, sync_data in results['sync_results'].items():
                    if 'error' not in sync_data:
                        if 'assets_created' in sync_data:
                            total_assets += sync_data['assets_created']
                        if 'facilities_created' in sync_data:
                            total_assets += sync_data['facilities_created']
                        if 'work_orders_created' in sync_data:
                            total_work_orders += sync_data['work_orders_created']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Assets Synced", total_assets)
                with col2:
                    st.metric("Total Work Orders", total_work_orders)

        # Analytics Visualization
        if 'analytics' in results:
            st.subheader("📈 Analytics Dashboard")
            
            analytics_tabs = st.tabs(["Fleet Analytics", "Maintenance Analytics", "Depot Analysis", "Station Analytics"])
            
            with analytics_tabs[0]:
                if 'fleet' in results['analytics']:
                    fleet = results['analytics']['fleet']
                    
                    # Fleet status pie chart
                    status_data = {
                        'Available': fleet['available_trainsets'],
                        'Maintenance': fleet['maintenance_trainsets'],
                        'IBL': fleet['ibl_trainsets']
                    }
                    
                    fig = px.pie(
                        values=list(status_data.values()),
                        names=list(status_data.keys()),
                        title="Fleet Status Distribution",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Reliability distribution
                    if 'maximo_datasets' in st.session_state:
                        trainsets_df = st.session_state.maximo_datasets['trainsets']
                        fig = px.histogram(
                            trainsets_df,
                            x='operational_reliability_score',
                            nbins=20,
                            title="Reliability Score Distribution",
                            labels={'operational_reliability_score': 'Reliability Score', 'count': 'Number of Trainsets'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            with analytics_tabs[1]:
                if 'maintenance' in results['analytics']:
                    maint = results['analytics']['maintenance']
                    
                    # Maintenance priority chart
                    priority_data = {
                        'Critical': maint['critical_maintenance'],
                        'High Priority': maint['high_priority_jobs'],
                        'Preventive': maint['preventive_maintenance'],
                        'Corrective': maint['corrective_maintenance']
                    }
                    
                    fig = px.bar(
                        x=list(priority_data.keys()),
                        y=list(priority_data.values()),
                        title="Maintenance Priority Distribution",
                        color=list(priority_data.values()),
                        color_continuous_scale='Reds'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Cost analysis
                    st.metric("Estimated Total Cost", f"₹{maint['estimated_total_cost']:,.0f}")
            
            with analytics_tabs[2]:
                if 'depots' in results['analytics']:
                    depots = results['analytics']['depots']
                    
                    # Depot comparison
                    depot_names = list(depots.keys())
                    depot_counts = [depots[depot]['trainset_id'] for depot in depot_names]
                    depot_reliability = [depots[depot]['operational_reliability_score'] for depot in depot_names]
                    
                    fig = make_subplots(
                        rows=1, cols=2,
                        subplot_titles=('Trainsets per Depot', 'Average Reliability per Depot'),
                        specs=[[{"type": "bar"}, {"type": "bar"}]]
                    )
                    
                    fig.add_trace(
                        go.Bar(x=depot_names, y=depot_counts, name="Trainsets"),
                        row=1, col=1
                    )
                    
                    fig.add_trace(
                        go.Bar(x=depot_names, y=depot_reliability, name="Reliability"),
                        row=1, col=2
                    )
                    
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            
            with analytics_tabs[3]:
                if 'stations' in results['analytics']:
                    stations = results['analytics']['stations']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Stations", stations['total_stations'])
                        st.metric("Total Daily Passengers", f"{stations['total_passengers']:,}")
                    with col2:
                        st.metric("Average Accessibility", f"{stations['average_accessibility']:.2f}")
                        st.metric("Total Parking Capacity", f"{stations['total_parking']:,}")

        # Recommendations Section
        if 'recommendations' in results and results['recommendations']:
            st.subheader("💡 Recommendations")
            
            for i, recommendation in enumerate(results['recommendations'], 1):
                st.info(f"{i}. {recommendation}")

        # Export Section
        st.subheader("📤 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export Results CSV", key="export_csv"):
                filename = connector.export_results_to_csv()
                if filename:
                    st.success(f"✅ Results exported to {filename}")
        
        with col2:
            if st.button("📋 Generate Report", key="generate_report"):
                report = connector.get_summary_report()
                st.text_area("Summary Report", report, height=400)
        
        with col3:
            if st.button("🔄 Refresh Data", key="refresh_data"):
                st.rerun()

    else:
        st.info("👆 Click 'Generate Results' to load and analyze your data with IBM Maximo integration")

    # Quick Actions Section
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 View Assets", key="view_assets"):
            st.info("Asset management view would open here")
    
    with col2:
        if st.button("📋 Work Orders", key="view_work_orders"):
            st.info("Work order management view would open here")
    
    with col3:
        if st.button("💰 Cost Analysis", key="cost_analysis"):
            st.info("Cost analysis view would open here")
    
    with col4:
        if st.button("📈 Reports", key="reports"):
            st.info("Reports view would open here")

def create_maximo_integration_tab():
    """Create a dedicated Maximo integration tab"""
    create_maximo_dashboard()
