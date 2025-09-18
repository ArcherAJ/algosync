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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Animated Background */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.3) 0%, transparent 50%);
        animation: backgroundShift 20s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes backgroundShift {
        0%, 100% { transform: translateX(0) translateY(0); }
        25% { transform: translateX(-20px) translateY(-10px); }
        50% { transform: translateX(20px) translateY(10px); }
        75% { transform: translateX(-10px) translateY(20px); }
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .main-header h1 {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #fff, #f0f0f0, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: textGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes textGlow {
        0% { filter: drop-shadow(0 0 5px rgba(255,255,255,0.5)); }
        100% { filter: drop-shadow(0 0 20px rgba(255,255,255,0.8)); }
    }
    
    .main-header p {
        font-size: 1.4rem;
        opacity: 0.95;
        font-weight: 400;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        text-align: center;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover::before {
        transform: scaleX(1);
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 0 0 1px rgba(255,255,255,0.2),
            inset 0 1px 0 rgba(255,255,255,0.3);
    }
    
    .metric-card .metric-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #6c757d;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-card .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card .metric-delta {
        font-size: 0.85rem;
        color: #28a745;
        font-weight: 600;
        background: rgba(40, 167, 69, 0.1);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        display: inline-block;
        border: 1px solid rgba(40, 167, 69, 0.2);
    }
    
    .metric-card .metric-delta.negative {
        color: #dc3545;
        background: rgba(220, 53, 69, 0.1);
        border-color: rgba(220, 53, 69, 0.2);
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
        gap: 12px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #6c757d;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        opacity: 1;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        color: #495057;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 
            0 10px 30px rgba(102, 126, 234, 0.3),
            0 0 0 1px rgba(255,255,255,0.2);
        transform: translateY(-3px);
    }
    
    .stTabs [aria-selected="true"]::before {
        opacity: 0;
    }
    
    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.8rem 2rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 8px 25px rgba(102, 126, 234, 0.3),
            0 0 0 1px rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 
            0 15px 35px rgba(102, 126, 234, 0.4),
            0 0 0 1px rgba(255,255,255,0.2);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Chart Containers */
    .stPlotlyChart {
        border-radius: 20px;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.1);
        overflow: hidden;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.1);
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
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
    @media (max-width: 1200px) {
        .main-header h1 {
            font-size: 3rem;
        }
        .main-header p {
            font-size: 1.2rem;
        }
    }
    
    @media (max-width: 768px) {
        .main-header {
            padding: 2rem 1rem;
            border-radius: 20px;
        }
        
        .main-header h1 {
            font-size: 2.2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .metric-card {
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .metric-card .metric-value {
            font-size: 2.2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.6rem 1rem;
            font-size: 0.85rem;
        }
        
        .stButton > button {
            padding: 0.6rem 1.5rem;
            font-size: 0.9rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 1.5rem 0.8rem;
        }
        
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .main-header p {
            font-size: 0.9rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-card .metric-value {
            font-size: 1.8rem;
        }
        
        .metric-card .metric-title {
            font-size: 0.8rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 0.8rem;
            font-size: 0.8rem;
        }
    }
    
    /* Tablet Landscape */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-header h1 {
            font-size: 2.8rem;
        }
        
        .metric-card {
            padding: 1.8rem;
        }
        
        .metric-card .metric-value {
            font-size: 2.5rem;
        }
    }
    
    /* Large Desktop */
    @media (min-width: 1400px) {
        .main-header h1 {
            font-size: 4rem;
        }
        
        .main-header p {
            font-size: 1.5rem;
        }
        
        .metric-card {
            padding: 2.5rem;
        }
        
        .metric-card .metric-value {
            font-size: 3.5rem;
        }
    }
    
    /* Dark Mode Styles */
    .dark-mode {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #e0e0e0;
    }
    
    .dark-mode .main-header {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 50%, #718096 100%);
    }
    
    .dark-mode .metric-card {
        background: rgba(45, 55, 72, 0.95);
        border-color: rgba(255, 255, 255, 0.1);
        color: #e0e0e0;
    }
    
    .dark-mode .stTabs [data-baseweb="tab"] {
        background: rgba(45, 55, 72, 0.8);
        color: #e0e0e0;
    }
    
    /* Loading States and Skeleton Screens */
    .skeleton {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
        border-radius: 8px;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    .skeleton-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    .skeleton-title {
        height: 20px;
        width: 60%;
        margin-bottom: 1rem;
    }
    
    .skeleton-value {
        height: 40px;
        width: 80%;
        margin-bottom: 0.5rem;
    }
    
    .skeleton-delta {
        height: 16px;
        width: 40%;
    }
    
    /* Enhanced Loading Spinner */
    .modern-spinner {
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 4px solid rgba(102, 126, 234, 0.1);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: modernSpin 1s ease-in-out infinite;
    }
    
    @keyframes modernSpin {
        to { transform: rotate(360deg); }
    }
    
    /* Progress Bar */
    .progress-bar {
        width: 100%;
        height: 6px;
        background: rgba(102, 126, 234, 0.1);
        border-radius: 3px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 3px;
        animation: progressFill 2s ease-in-out infinite;
    }
    
    @keyframes progressFill {
        0% { width: 0%; }
        50% { width: 70%; }
        100% { width: 100%; }
    }
    
    /* Notification Toast */
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 1rem 1.5rem;
        border-radius: 15px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .toast-success {
        border-left: 4px solid #4ade80;
    }
    
    .toast-error {
        border-left: 4px solid #ef4444;
    }
    
    .toast-warning {
        border-left: 4px solid #fbbf24;
    }
    
    .toast-info {
        border-left: 4px solid #3b82f6;
    }
    
    /* Pulse Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Floating Elements */
    .floating-element {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Interactive Hover Effects */
    .interactive-card {
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .interactive-card:hover {
        transform: translateY(-5px) rotateX(5deg);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    .status-online { background: #4ade80; }
    .status-warning { background: #fbbf24; }
    .status-offline { background: #ef4444; }
    
    /* Custom Scrollbar for Dark Mode */
    .dark-mode ::-webkit-scrollbar-track {
        background: #2d3748;
    }
    
    .dark-mode ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #4a5568 0%, #718096 100%);
    }
    
    .dark-mode ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    # Enhanced Main Header
    st.markdown("""
    <div class="main-header fade-in-up">
        <h1>🚇 KMRL AI Induction Planning Platform</h1>
        <p>Next-Generation AI-Powered Metro Fleet Management & Optimization</p>
        <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;">
            <span style="background: rgba(255,255,255,0.25); padding: 0.8rem 1.5rem; border-radius: 25px; font-size: 1rem; font-weight: 600; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                🤖 Advanced AI Analytics
            </span>
            <span style="background: rgba(255,255,255,0.25); padding: 0.8rem 1.5rem; border-radius: 25px; font-size: 1rem; font-weight: 600; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                📊 Real-time Intelligence
            </span>
            <span style="background: rgba(255,255,255,0.25); padding: 0.8rem 1.5rem; border-radius: 25px; font-size: 1rem; font-weight: 600; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                ⚡ Smart Optimization
            </span>
            <span style="background: rgba(255,255,255,0.25); padding: 0.8rem 1.5rem; border-radius: 25px; font-size: 1rem; font-weight: 600; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">
                🔮 Predictive Analytics
            </span>
        </div>
        <div style="margin-top: 1.5rem; font-size: 0.9rem; opacity: 0.8;">
            <span style="display: inline-flex; align-items: center; gap: 0.5rem;">
                <span style="width: 8px; height: 8px; background: #4ade80; border-radius: 50%; animation: pulse 2s infinite;"></span>
                System Status: Operational
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # Enhanced Sidebar - Control Panel
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); 
                    padding: 2rem; border-radius: 20px; margin-bottom: 1.5rem; color: white;
                    box-shadow: 0 15px 35px rgba(0,0,0,0.1); backdrop-filter: blur(10px);
                    border: 1px solid rgba(255,255,255,0.2);">
            <h2 style="margin: 0; font-size: 1.6rem; text-align: center; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">⚙️ Control Center</h2>
            <p style="margin: 0.5rem 0 0 0; text-align: center; opacity: 0.9; font-size: 0.9rem;">AI-Powered Fleet Management</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Dark Mode Toggle
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
        
        dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        # Auto-refresh toggle
        st.session_state.auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=st.session_state.auto_refresh)
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