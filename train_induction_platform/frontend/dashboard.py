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

def create_dashboard_tab():
    """Create the main dashboard tab with hover cards."""
    
    # Add custom CSS for hover effect and card size
    st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        text-align: center;
        width: 130px;
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
        color: #007bff;
    }
    .metric-delta {
        font-size: 14px;
        color: #28a745;
    }
    </style>
    """, unsafe_allow_html=True)

    
    # Header of the Dashboard
    st.header("📊 Real-time Fleet Dashboard")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    trainsets = st.session_state.trainsets

    with col1:
        service_count = sum(1 for t in trainsets if t['recommendation'] == 'Service')
        delta_service = f"{service_count/len(trainsets)*100:.1f}%"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Service Ready</div>
            <div class="metric-value">{service_count}</div>
            <div class="metric-delta">↑ {delta_service}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        standby_count = sum(1 for t in trainsets if t['recommendation'] == 'Standby')
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Standby</div>
            <div class="metric-value">{standby_count}</div>
            <div class="metric-delta">&nbsp;</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        ibl_count = sum(1 for t in trainsets if t['recommendation'] == 'IBL')
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">IBL/Maintenance</div>
            <div class="metric-value">{ibl_count}</div>
            <div class="metric-delta">&nbsp;</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        fitness_valid = sum(1 for t in trainsets if t['fitness']['overall_valid'])
        delta_fitness = f"{fitness_valid/len(trainsets)*100:.1f}%"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Fitness Valid</div>
            <div class="metric-value">{fitness_valid}</div>
            <div class="metric-delta">↑ {delta_fitness}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        avg_score = sum(t['ai_score'] for t in trainsets) / len(trainsets)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Avg AI Score</div>
            <div class="metric-value">{avg_score:.1f}</div>
            <div class="metric-delta">&nbsp;</div>
        </div>
        """, unsafe_allow_html=True)

    # Fleet status visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Fleet Status Distribution")
        
        # Create status distribution chart
        status_data = pd.DataFrame([
            {'Status': 'Service', 'Count': service_count, 'Color': '#28a745'},
            {'Status': 'Standby', 'Count': standby_count, 'Color': '#ffc107'},
            {'Status': 'IBL', 'Count': ibl_count, 'Color': '#dc3545'}
        ])
        
        fig = px.pie(status_data, values='Count', names='Status', 
                    color='Status', 
                    color_discrete_map={'Service': '#28a745', 'Standby': '#ffc107', 'IBL': '#dc3545'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Top Performers")
        top_trains = sorted(trainsets, key=lambda x: x['ai_score'], reverse=True)[:5]
        
        for i, train in enumerate(top_trains, 1):
            status_class = f"status-{train['recommendation'].lower()}"
            st.markdown(f"""
            <div class="trainset-card {status_class}">
                <strong>#{i} {train['id']}</strong><br>
                Score: {train['ai_score']}<br>
                Status: {train['recommendation']}
            </div>
            """, unsafe_allow_html=True)
    
    # Recent activity timeline
    st.subheader("Recent System Activity")
    activity_data = []
    
    # Simulate recent activities
    for i in range(5):
        activity_data.append({
            'Time': datetime.now() - timedelta(minutes=random.randint(1, 60)),
            'Activity': random.choice([
                'Fitness certificate updated',
                'Job card closed',
                'Maintenance scheduled',
                'Branding assignment changed',
                'IOT sensor data received'
            ]),
            'Trainset': random.choice([t['id'] for t in trainsets[:10]])
        })
    
    activity_df = pd.DataFrame(activity_data)
    st.dataframe(activity_df, use_container_width=True)

if __name__ == "__main__":
    create_dashboard_tab()