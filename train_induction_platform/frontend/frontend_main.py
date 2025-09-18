import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import io
import time
import math
import threading
import queue
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import warnings



from system_manager import SystemIntegrationManager
from frontend.dashboard import create_dashboard_tab
from frontend.fleet_status import create_fleet_status_tab
from frontend.maintenance import create_maintenance_tab
from frontend.branding import create_branding_tab
from frontend.alerts_tab import create_alerts_tab
from frontend.analytics import create_analytics_tab
from frontend.maps import create_map
from frontend.timetable_f import create_timetable_tab



def create_streamlit_frontend():
    """ Create a comprehensive Streamlit frontend for the KMRL AI Induction Planning Platform"""
    # Initialize session state
    if 'system_manager' not in st.session_state:
        st.session_state.system_manager = SystemIntegrationManager()
        st.session_state.trainsets = st.session_state.system_manager.initialize_system(25)
        st.session_state.last_refresh = datetime.now()
        st.session_state.auto_refresh = False
    # Page configuration
    st.set_page_config(
        page_title="KMRL AI Induction Planning Platform",
        page_icon="🚇",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    # Custom CSS
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-high { border-left-color: #ff4b4b; }
    .alert-medium { border-left-color: #ffa500; }
    .alert-low { border-left-color: #00cc88; }
    .trainset-card {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
    .status-service { background-color: #d4edda; }
    .status-standby { background-color: #fff3cd; }
    .status-ibl { background-color: #f8d7da; }
    </style>
    """, unsafe_allow_html=True)
    # Main title and header
    st.title("🚇 KMRL AI Induction Planning Platform")
    st.markdown("**Enhanced AI-powered decision support with multi-objective optimization**")
    # Sidebar - Control Panel
    with st.sidebar:
        st.header("⚙️ Control Panel")
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
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8= st.tabs([
        "📊 Dashboard", "🚆 Fleet Status", "🔧 Maintenance", 
        "📢 Branding", "⚠️ Alerts", "📈 Analytics", "🗺️ Map", "🕒 Timetable"
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