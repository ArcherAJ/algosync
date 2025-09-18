from common_imports import *
from data_config import config

from system_manager import SystemIntegrationManager
from frontend.dashboard import create_dashboard_tab
from frontend.fleet_status import create_fleet_status_tab
from frontend.maintenance import create_maintenance_tab
from frontend.branding import create_branding_tab
from frontend.alerts_tab import create_alerts_tab
from frontend.analytics import create_analytics_tab
from frontend.maps import create_map
from frontend.timetable_f import create_timetable_tab
from frontend.passenger_demand import create_passenger_demand_tab



def create_streamlit_frontend():
    """ Create a comprehensive Streamlit frontend for the KMRL AI Induction Planning Platform"""
    # Initialize session state
    if 'system_manager' not in st.session_state:
        st.session_state.system_manager = SystemIntegrationManager()
        st.session_state.trainsets = st.session_state.system_manager.initialize_system(config.DEFAULT_TRAINSET_COUNT)
        st.session_state.last_refresh = datetime.now()
        st.session_state.auto_refresh = False
    # Page configuration
    st.set_page_config(
        page_title="KMRL AI Induction Planning Platform",
        page_icon="🚇",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Enhanced Custom CSS with modern design
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: none;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    /* Alert Cards */
    .alert-high { 
        border-left: 4px solid #ff4757;
        background: linear-gradient(145deg, #fff5f5 0%, #ffe6e6 100%);
    }
    .alert-medium { 
        border-left: 4px solid #ffa502;
        background: linear-gradient(145deg, #fff8e1 0%, #ffecb3 100%);
    }
    .alert-low { 
        border-left: 4px solid #2ed573;
        background: linear-gradient(145deg, #f0fff4 0%, #d4edda 100%);
    }
    
    /* Trainset Cards */
    .trainset-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .trainset-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* Status Colors */
    .status-service { 
        background: linear-gradient(145deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 4px solid #28a745;
    }
    .status-standby { 
        background: linear-gradient(145deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid #ffc107;
    }
    .status-ibl { 
        background: linear-gradient(145deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 4px solid #dc3545;
    }
    
    /* Sidebar Enhancement */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Tab Enhancement */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(145deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* Chart Containers */
    .stPlotlyChart {
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        overflow: hidden;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(145deg, #d4edda 0%, #c3e6cb 100%);
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    
    .stError {
        background: linear-gradient(145deg, #f8d7da 0%, #f5c6cb 100%);
        border-radius: 10px;
        border-left: 4px solid #dc3545;
    }
    
    .stWarning {
        background: linear-gradient(145deg, #fff3cd 0%, #ffeaa7 100%);
        border-radius: 10px;
        border-left: 4px solid #ffc107;
    }
    
    /* Info Messages */
    .stInfo {
        background: linear-gradient(145deg, #d1ecf1 0%, #bee5eb 100%);
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
    }
    
    /* Loading Spinner */
    .stSpinner {
        border-radius: 50%;
    }
    
    /* Custom Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        .main-header p {
            font-size: 1rem;
        }
        .metric-card {
            padding: 1rem;
        }
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #5a6fd8 0%, #6a4190 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    # Enhanced Main Header
    st.markdown("""
    <div class="main-header fade-in-up">
        <h1>🚇 KMRL AI Induction Planning Platform</h1>
        <p>Enhanced AI-powered decision support with multi-objective optimization</p>
        <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                🤖 AI-Powered
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                📊 Real-time Analytics
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                ⚡ Smart Optimization
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # Enhanced Sidebar - Control Panel
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 15px; margin-bottom: 1rem; color: white;">
            <h2 style="margin: 0; font-size: 1.5rem; text-align: center;">⚙️ Control Panel</h2>
        </div>
        """, unsafe_allow_html=True)
        # Auto-refresh toggle
        st.session_state.auto_refresh = st.checkbox("Auto-refresh (30s)", value=st.session_state.auto_refresh)
        if st.session_state.auto_refresh:
            time.sleep(30)
            st.rerun()
        # Manual refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            with st.spinner("Refreshing real-time data..."):
                st.session_state.trainsets, update_count = st.session_state.system_manager.data_integrator.refresh_all_data(
                    st.session_state.trainsets
                )
                st.success(f"Updated {update_count} records")
                st.session_state.last_refresh = datetime.now()
        st.write(f"Last refresh: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
        # Optimization constraints
        st.subheader("🎯 Optimization Settings")
        service_target = st.slider("Service Target", 10, 20, 15)
        max_ibl = st.slider("Max IBL", 3, 8, 5)
        constraints = {
            'service_target': service_target,
            'max_ibl': max_ibl,
            'branding_priority': st.selectbox("Branding Priority", ["Low", "Medium", "High"]),
            'maintenance_buffer': st.slider("Maintenance Buffer (days)", 1, 7, 3)
        }
        # Run optimization
        if st.button("🚀 Run AI Optimization", type="primary"):
            with st.spinner("Running AI optimization..."):
                optimized_trainsets, metrics, alerts, maintenance_pred = st.session_state.system_manager.run_complete_optimization(
                    st.session_state.trainsets, constraints
                )
                # Generate and store timetable
                timetable = st.session_state.system_manager.generate_timetable(optimized_trainsets, constraints)
                
                st.session_state.trainsets = optimized_trainsets
                st.session_state.current_metrics = metrics
                st.session_state.current_alerts = alerts
                st.session_state.maintenance_predictions = maintenance_pred
                st.session_state.timetable = timetable  # Store timetable in session state
                
                st.success("Optimization completed!")
        # Data source status
        st.subheader("🔗 Data Sources")
        for source, status in st.session_state.system_manager.data_integrator.data_sources.items():
            status_icon = "🟢" if status['connected'] else "🔴"
            st.write(f"{status_icon} {source.replace('_', ' ').title()}")
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "📊 Dashboard", "🚆 Fleet Status", "🔧 Maintenance", 
        "📢 Branding", "⚠️ Alerts", "📈 Analytics", "🗺️ Map", "🕒 Timetable", "🚆 Passenger Demand"
    ])
    with tab1:
        create_dashboard_tab()
    with tab2:
        create_fleet_status_tab()
    with tab3:
        create_maintenance_tab()
    with tab4:
        create_branding_tab()
    with tab5:
        create_alerts_tab()
    with tab6:
        create_analytics_tab()
    with tab7:
        create_map()
    with tab8:
        create_timetable_tab()
    with tab9:
        create_passenger_demand_tab()