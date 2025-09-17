import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import json
import time

# Initialize session state variables
if 'system_manager' not in st.session_state:
    # Mock system manager for demonstration
    class MockSystemManager:
        def __init__(self):
            self.data_integrator = MockDataIntegrator()
            
        def run_complete_optimization(self, trainsets, constraints):
            # Mock optimization process
            for train in trainsets:
                # Update AI score based on various factors
                fitness_factor = 0.8 if train['fitness']['overall_valid'] else 0.2
                reliability_factor = train['operational']['reliability_score'] / 100
                wear_values = train['mileage']['component_wear'].values()
                wear_factor = 1 - (sum(wear_values) / (100 * len(wear_values)))  # Normalize to 0-1
                
                # Calculate AI score (0-100)
                train['ai_score'] = round((fitness_factor * 0.4 + reliability_factor * 0.3 + wear_factor * 0.3) * 100, 1)
                
                # Set recommendation based on score and constraints
                if train['ai_score'] >= 80:
                    train['recommendation'] = 'Service'
                elif train['ai_score'] >= 60:
                    train['recommendation'] = 'Standby'
                else:
                    train['recommendation'] = 'IBL'
            
            # Mock metrics and alerts
            valid_fitness_count = sum(1 for t in trainsets if t['fitness']['overall_valid'])
            metrics = {
                'fitness_compliance': round(valid_fitness_count / len(trainsets) * 100),
                'avg_reliability': round(sum(t['operational']['reliability_score'] for t in trainsets) / len(trainsets)),
                'maintenance_backlog': sum(t['job_cards']['open'] for t in trainsets),
                'processing_time': round(random.uniform(2.5, 5.5), 1),
                'estimated_savings': random.randint(50000, 200000),
                'energy_efficiency': random.randint(75, 92)
            }
            
            alerts = []
            for train in trainsets:
                if train['fitness']['days_until_expiry'] < 7:
                    alerts.append({
                        'type': 'fitness_expiry',
                        'priority': 'High',
                        'message': f"Trainset {train['id']} fitness expires in {train['fitness']['days_until_expiry']} days",
                        'timestamp': datetime.now()
                    })
                if train['job_cards']['open'] > 3:
                    alerts.append({
                        'type': 'maintenance_backlog',
                        'priority': 'Medium',
                        'message': f"Trainset {train['id']} has {train['job_cards']['open']} open job cards",
                        'timestamp': datetime.now()
                    })
            
            # Mock maintenance predictions
            maintenance_pred = pd.DataFrame([
                {
                    'trainset_id': train['id'],
                    'component': random.choice(['Brakes', 'Engines', 'Doors', 'HVAC']),
                    'risk_score': round(random.uniform(0.1, 0.9), 2),
                    'days_until_maintenance': random.randint(1, 30),
                    'priority': random.choice(['High', 'Medium', 'Low']),
                    'recommended_action': random.choice(['Schedule Immediately', 'Monitor Closely', 'Routine Check'])
                }
                for train in random.sample(trainsets, min(10, len(trainsets)))
            ])
            
            return trainsets, metrics, alerts, maintenance_pred
        
        def get_optimization_trends(self):
            # Mock trend data
            timestamps = [datetime.now() - timedelta(hours=i) for i in range(24, 0, -2)]
            return {
                'timestamps': timestamps,
                'service_readiness': [random.randint(10, 20) for _ in timestamps],
                'fitness_compliance': [random.randint(70, 95) for _ in timestamps],
                'alert_counts': [random.randint(0, 8) for _ in timestamps],
                'processing_times': [round(random.uniform(2.0, 6.0), 1) for _ in timestamps]
            }
        
        def generate_comprehensive_report(self, trainsets, metrics, alerts, report_type):
            # Mock report generation
            service_ready = sum(1 for t in trainsets if t['recommendation'] == 'Service')
            standby = sum(1 for t in trainsets if t['recommendation'] == 'Standby')
            in_maintenance = sum(1 for t in trainsets if t['recommendation'] == 'IBL')
            
            return {
                'generated_at': datetime.now(),
                'report_type': report_type,
                'summary': {
                    'total_trainsets': len(trainsets),
                    'service_ready': service_ready,
                    'standby': standby,
                    'in_maintenance': in_maintenance,
                },
                'metrics': metrics,
                'alert_count': len(alerts),
                'top_concerns': [alert['message'] for alert in alerts[:3]] if alerts else ["No critical concerns"]
            }
    
    class MockDataIntegrator:
        def __init__(self):
            self.data_sources = {
                'maintenance_system': {'connected': True},
                'fitness_records': {'connected': True},
                'branding_database': {'connected': True},
                'operational_metrics': {'connected': True}
            }
            
        def refresh_all_data(self, trainsets):
            # Mock data refresh - just update some random values
            update_count = 0
            for train in trainsets:
                # Update fitness days randomly
                train['fitness']['days_until_expiry'] = max(0, train['fitness']['days_until_expiry'] - random.randint(0, 2))
                
                # Randomly change some job cards
                if random.random() < 0.2:
                    change = random.randint(-1, 2)
                    train['job_cards']['open'] = max(0, train['job_cards']['open'] + change)
                    train['job_cards']['closed'] = max(0, train['job_cards']['closed'] - change)
                    update_count += 1
            
            return trainsets, update_count
    
    st.session_state.system_manager = MockSystemManager()

if 'trainsets' not in st.session_state:
    # Generate mock trainset data
    trainsets = []
    advertisers = ['Coca-Cola', 'Pepsi', 'Amazon', 'Google', 'Microsoft', 'Apple', None, None, None]
    depots = ['Depot A', 'Depot B', 'Depot C']
    
    for i in range(1, 31):
        depot = random.choice(depots)
        reliability = random.randint(85, 98)
        advertiser = random.choice(advertisers)
        
        trainsets.append({
            'id': f"TS{str(i).zfill(3)}",
            'depot': depot,
            'fitness': {
                'certificate_id': f"FIT-{depot.replace(' ', '')}-{str(i).zfill(3)}",
                'valid_until': datetime.now() + timedelta(days=random.randint(1, 60)),
                'overall_valid': random.random() > 0.2,
                'days_until_expiry': random.randint(1, 60)
            },
            'job_cards': {
                'open': random.randint(0, 5),
                'closed': random.randint(10, 50)
            },
            'operational': {
                'reliability_score': reliability,
                'last_maintenance': datetime.now() - timedelta(days=random.randint(1, 30)),
                'energy_efficiency': random.randint(75, 95)
            },
            'mileage': {
                'total_km': random.randint(50000, 250000),
                'component_wear': {
                    'brakes': random.randint(10, 90),
                    'engines': random.randint(5, 80),
                    'doors': random.randint(15, 85)
                }
            },
            'branding': {
                'advertiser': advertiser,
                'contract_value': random.randint(500000, 2000000) if advertiser else 0,
                'hours_required_today': random.randint(0, 12),
                'exposure_deficit': random.randint(0, 48)
            },
            'ai_score': 0,  # Will be calculated during optimization
            'recommendation': 'Pending'  # Will be set during optimization
        })
    
    st.session_state.trainsets = trainsets

if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()

if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False

if 'theme' not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

def create_theme_toggle():
    # Button styling
    button_style = f"""
    <style>
    .theme-toggle {{
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 9999;
        background: transparent;
        border: none;
        cursor: pointer;
        font-size: 24px;
        padding: 8px;
        border-radius: 50%;
        transition: all 0.3s ease;
    }}
    .theme-toggle:hover {{
        transform: scale(1.1);
    }}
    </style>
    """
    
    st.markdown(button_style, unsafe_allow_html=True)
    
    # Create the toggle button
    if st.button(f"{'🌙' if st.session_state.theme == 'light' else '☀️'}", 
                 key="theme_toggle", 
                 on_click=toggle_theme,
                 help="Toggle between light and dark mode"):
        pass

def get_theme_styles():
    if st.session_state.theme == "light":
        return """
        <style>
        :root {
            --bg-primary: #f8f9fa;
            --bg-secondary: #ffffff;
            --text-primary: #212529;
            --text-secondary: #6c757d;
            --accent-primary: #1f77b4;
            --accent-secondary: #ff7f0e;
            --border-color: #dee2e6;
            --card-bg: #f0f2f6;
            --metric-bg: #f8f9fa;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --shadow: rgba(0, 0, 0, 0.1);
        }
        
        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            transition: all 0.3s ease;
        }
        
        .stApp {
            background-color: var(--bg-primary);
        }
        
        .main .block-container {
            background-color: var(--bg-primary);
        }
        
        .metric-card {
            background-color: var(--card-bg);
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid var(--accent-primary);
            transition: all 0.3s ease;
        }
        
        .trainset-card {
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 0.5rem;
            margin: 0.25rem 0;
            transition: all 0.3s ease;
        }
        
        .status-service { background-color: #d4edda; }
        .status-standby { background-color: #fff3cd; }
        .status-ibl { background-color: #f8d7da; }
        
        .alert-high { border-left-color: var(--danger); }
        .alert-medium { border-left-color: var(--warning); }
        .alert-low { border-left-color: var(--success); }
        
        /* Streamlit component overrides */
        .stButton>button {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: var(--accent-primary);
            color: white;
        }
        
        .stSelectbox div div {
            background-color: var(--bg-secondary);
        }
        
        .stSlider div div {
            background-color: var(--accent-primary);
        }
        
        .stDataFrame {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: var(--bg-secondary);
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: var(--bg-secondary);
            color: var(--text-secondary);
            padding: 10px 16px;
            border-radius: 4px 4px 0 0;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--accent-primary);
            color: white;
        }
        </style>
        """
    else:
        return """
        <style>
        :root {
            --bg-primary: #121212;
            --bg-secondary: #1e1e1e;
            --text-primary: #e0e0e0;
            --text-secondary: #a0a0a0;
            --accent-primary: #4fc3f7;
            --accent-secondary: #ffb74d;
            --border-color: #424242;
            --card-bg: #2d2d2d;
            --metric-bg: #1e1e1e;
            --success: #81c784;
            --warning: #ffd54f;
            --danger: #e57373;
            --shadow: rgba(0, 0, 0, 0.3);
        }
        
        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            transition: all 0.3s ease;
        }
        
        .stApp {
            background-color: var(--bg-primary);
        }
        
        .main .block-container {
            background-color: var(--bg-primary);
        }
        
        .metric-card {
            background-color: var(--card-bg);
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid var(--accent-primary);
            transition: all 0.3s ease;
        }
        
        .trainset-card {
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 0.5rem;
            margin: 0.25rem 0;
            transition: all 0.3s ease;
        }
        
        .status-service { background-color: #2e7d32; color: white; }
        .status-standby { background-color: #f9a825; color: black; }
        .status-ibl { background-color: #c62828; color: white; }
        
        .alert-high { border-left-color: var(--danger); }
        .alert-medium { border-left-color: var(--warning); }
        .alert-low { border-left-color: var(--success); }
        
        /* Streamlit component overrides */
        .stButton>button {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
        }
        
        .stButton>button:hover {
            background-color: var(--accent-primary);
            color: white;
        }
        
        .stSelectbox div div {
            background-color: var(--bg-secondary);
        }
        
        .stSlider div div {
            background-color: var(--accent-primary);
        }
        
        .stDataFrame {
            background-color: var(--bg-secondary);
            color: var(--text-primary);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            background-color: var(--bg-secondary);
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: var(--bg-secondary);
            color: var(--text-secondary);
            padding: 10px 16px;
            border-radius: 4px 4px 0 0;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--accent-primary);
            color: white;
        }
        
        /* Plotly chart styling */
        .js-plotly-plot .plotly, .modebar {
            background-color: var(--bg-secondary) !important;
        }
        
        .js-plotly-plot .plotly .main-svg {
            background-color: var(--bg-secondary) !important;
        }
        
        .js-plotly-plot .plotly .gridlayer bg {
            fill: var(--bg-secondary) !important;
        }
        
        .js-plotly-plot .plotly text {
            fill: var(--text-primary) !important;
        }
        </style>
        """

def create_dashboard_tab():
    """Create the main dashboard tab"""
    st.header("📊 Real-time Fleet Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    trainsets = st.session_state.trainsets
    
    with col1:
        service_count = sum(1 for t in trainsets if t.get('recommendation') == 'Service')
        st.metric("Service Ready", service_count, 
                 delta=f"{service_count/len(trainsets)*100:.1f}%" if trainsets else "0%")
    
    with col2:
        standby_count = sum(1 for t in trainsets if t.get('recommendation') == 'Standby')
        st.metric("Standby", standby_count)
    
    with col3:
        ibl_count = sum(1 for t in trainsets if t.get('recommendation') == 'IBL')
        st.metric("IBL/Maintenance", ibl_count)
    
    with col4:
        fitness_valid = sum(1 for t in trainsets if t['fitness']['overall_valid'])
        st.metric("Fitness Valid", fitness_valid, 
                 delta=f"{fitness_valid/len(trainsets)*100:.1f}%" if trainsets else "0%")
    
    with col5:
        avg_score = sum(t['ai_score'] for t in trainsets) / len(trainsets) if trainsets else 0
        st.metric("Avg AI Score", f"{avg_score:.1f}")
    
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
        
        if service_count + standby_count + ibl_count > 0:
            fig = px.pie(status_data, values='Count', names='Status', 
                        color='Status', 
                        color_discrete_map={'Service': '#28a745', 'Standby': '#ffc107', 'IBL': '#dc3545'})
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No status data available. Run optimization first.")
    
    with col2:
        st.subheader("Top Performers")
        if trainsets and 'ai_score' in trainsets[0]:
            top_trains = sorted(trainsets, key=lambda x: x['ai_score'], reverse=True)[:5]
            
            for i, train in enumerate(top_trains, 1):
                status_class = f"status-{train.get('recommendation', 'pending').lower()}"
                st.markdown(f"""
                <div class="trainset-card {status_class}">
                    <strong>#{i} {train['id']}</strong><br>
                    Score: {train['ai_score']}<br>
                    Status: {train.get('recommendation', 'Pending')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Run optimization to see top performers")
    
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
            'Trainset': random.choice([t['id'] for t in trainsets[:10]]) if trainsets and len(trainsets) > 0 else "N/A"
        })
    
    activity_df = pd.DataFrame(activity_data)
    st.dataframe(activity_df, use_container_width=True)

def create_fleet_status_tab():
    """Create the fleet status tab"""
    st.header("🚆 Fleet Status Overview")
    
    trainsets = st.session_state.trainsets
    
    if not trainsets:
        st.info("No trainset data available")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        depot_options = list(set(t['depot'] for t in trainsets))
        depot_filter = st.selectbox("Filter by Depot", ["All"] + depot_options)
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Service", "Standby", "IBL"])
    with col3:
        sort_by = st.selectbox("Sort by", ["AI Score", "ID", "Fitness Expiry"])
    
    # Apply filters
    filtered_trainsets = trainsets.copy()
    if depot_filter != "All":
        filtered_trainsets = [t for t in filtered_trainsets if t['depot'] == depot_filter]
    if status_filter != "All":
        filtered_trainsets = [t for t in filtered_trainsets if t.get('recommendation') == status_filter]
    
    # Sort
    if sort_by == "AI Score":
        filtered_trainsets.sort(key=lambda x: x['ai_score'], reverse=True)
    elif sort_by == "Fitness Expiry":
        filtered_trainsets.sort(key=lambda x: x['fitness']['days_until_expiry'])
    
    # Display trainsets in a grid
    if filtered_trainsets:
        cols_per_row = 3
        for i in range(0, len(filtered_trainsets), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, train in enumerate(filtered_trainsets[i:i+cols_per_row]):
                with cols[j]:
                    create_trainset_card(train)
    else:
        st.info("No trainsets match the selected filters")

def create_trainset_card(train):
    """Create a detailed trainset card"""
    status_colors = {
        'Service': "#31ee5d",
        'Standby': "#e4c560",
        'IBL': "#f74957"
    }
    
    bg_color = status_colors.get(train.get('recommendation', 'Pending'), '#f8f9fa')
    
    # Override controls
    with st.expander(f"🚆 {train['id']} (Score: {train.get('ai_score', 0)})"):
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <strong>Current Recommendation: {train.get('recommendation', 'Pending')}</strong>
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
            wear_avg = sum(train['mileage']['component_wear'].values()) / len(train['mileage']['component_wear'])
            st.write(f"**Avg Wear:** {wear_avg:.1f}%")
            st.write(f"**Days to Fitness Expiry:** {train['fitness']['days_until_expiry']}")
        
        # Manual override
        st.subheader("Manual Override")
        current_override = train.get('manual_override', 'None')
        override_options = ["None", "Service", "Standby", "IBL"]
        override_index = override_options.index(current_override) if current_override in override_options else 0
        
        override_status = st.selectbox(
            "Override Recommendation", 
            override_options, 
            key=f"override_{train['id']}",
            index=override_index
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
                if 'manual_override' in train:
                    del train['manual_override']
                if 'override_reason' in train:
                    del train['override_reason']
                st.info("Override removed")

def create_maintenance_tab():
    """Create the maintenance planning tab"""
    st.header("🔧 Predictive Maintenance Dashboard")
    
    if 'maintenance_predictions' in st.session_state:
        predictions_df = st.session_state.maintenance_predictions
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            critical_count = len(predictions_df[predictions_df['priority'] == 'High']) if not predictions_df.empty else 0
            st.metric("Critical Maintenance", critical_count)
        
        with col2:
            avg_risk = predictions_df['risk_score'].mean() if not predictions_df.empty else 0
            st.metric("Avg Risk Score", f"{avg_risk:.1f}")
        
        with col3:
            immediate_action = len(predictions_df[predictions_df['recommended_action'] == 'Schedule Immediately']) if not predictions_df.empty else 0
            st.metric("Immediate Action", immediate_action)
        
        with col4:
            avg_days = predictions_df['days_until_maintenance'].mean() if not predictions_df.empty else 0
            st.metric("Avg Days to Maintenance", f"{avg_days:.1f}")
        
        if not predictions_df.empty:
            # Risk distribution chart
            fig = px.histogram(predictions_df, x='risk_score', nbins=10, 
                              title="Maintenance Risk Distribution")
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

def create_branding_tab():
    """Create the branding compliance tab"""
    st.header("📢 Branding & Revenue Management")
    
    trainsets = st.session_state.trainsets
    
    if not trainsets:
        st.info("No trainset data available")
        return
    
    # Branding summary
    total_contract_value = sum(t['branding']['contract_value'] for t in trainsets)
    total_exposure_deficit = sum(t['branding']['exposure_deficit'] for t in trainsets)
    branded_trains = sum(1 for t in trainsets if t['branding']['advertiser'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Contract Value", f"₹{total_contract_value:,}")
    with col2:
        st.metric("Branded Trains", branded_trains)
    with col3:
        st.metric("Exposure Deficit", f"{total_exposure_deficit} hrs")
    with col4:
        revenue_at_risk = total_exposure_deficit * 500  # Assume ₹500 per hour
        st.metric("Revenue at Risk", f"₹{revenue_at_risk:,}")
    
    # Advertiser breakdown
    advertiser_data = {}
    for train in trainsets:
        advertiser = train['branding']['advertiser'] or 'Unbranded'
        if advertiser not in advertiser_data:
            advertiser_data[advertiser] = {
                'trains': 0, 'contract_value': 0, 'deficit': 0, 'required_hours': 0
            }
        advertiser_data[advertiser]['trains'] += 1
        advertiser_data[advertiser]['contract_value'] += train['branding']['contract_value']
        advertiser_data[advertiser]['deficit'] += train['branding']['exposure_deficit']
        advertiser_data[advertiser]['required_hours'] += train['branding']['hours_required_today']
    
    # Convert to DataFrame for visualization
    if advertiser_data:
        advertiser_df = pd.DataFrame.from_dict(advertiser_data, orient='index').reset_index()
        advertiser_df.rename(columns={'index': 'Advertiser'}, inplace=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Contract Value by Advertiser")
            fig = px.bar(advertiser_df, x='Advertiser', y='contract_value', 
                        title="Contract Value Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Exposure Deficit by Advertiser")
            fig = px.bar(advertiser_df, x='Advertiser', y='deficit', 
                        title="Exposure Deficit by Advertiser", color='deficit')
            st.plotly_chart(fig, use_container_width=True)
    
    # Detailed branding table
    st.subheader("Detailed Branding Status")
    branding_details = []
    for train in trainsets:
        branding_details.append({
            'Trainset': train['id'],
            'Advertiser': train['branding']['advertiser'] or 'None',
            'Contract Value': train['branding']['contract_value'],
            'Hours Required Today': train['branding']['hours_required_today'],
            'Exposure Deficit': train['branding']['exposure_deficit'],
            'Status': train.get('recommendation', 'Pending')
        })
    
    branding_df = pd.DataFrame(branding_details)
    st.dataframe(branding_df, use_container_width=True)

def create_alerts_tab():
    """Create the alerts and notifications tab"""
    st.header("⚠️ Alerts & Notifications")
    
    if 'current_alerts' in st.session_state:
        alerts = st.session_state.current_alerts
        
        if not alerts:
            st.success("🎉 No active alerts!")
            return
        
        # Alert summary
        critical_alerts = [a for a in alerts if a.get('priority') == 'High']
        high_alerts = [a for a in alerts if a.get('priority') == 'High']
        medium_alerts = [a for a in alerts if a.get('priority') == 'Medium']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Critical Alerts", len(critical_alerts))
        with col2:
            st.metric("High Priority", len(high_alerts))
        with col3:
            st.metric("Medium Priority", len(medium_alerts))
        
        # Display alerts by priority
        for priority, alert_list in [('Critical', critical_alerts), ('High', high_alerts), ('Medium', medium_alerts)]:
            if alert_list:
                st.subheader(f"{priority} Priority Alerts")
                
                for alert in alert_list:
                    alert_class = f"alert-{priority.lower()}"
                    st.markdown(f"""
                    <div class="metric-card {alert_class}">
                        <strong>{alert.get('type', 'Unknown').replace('_', ' ').title()}</strong><br>
                        {alert.get('message', 'No message')}<br>
                        <small>Time: {alert.get('timestamp', datetime.now()).strftime('%H:%M:%S')}</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    else:
        st.info("Run AI optimization to generate alerts")

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
                    'AI_Score': t.get('ai_score', 0),
                    'Recommendation': t.get('recommendation', 'Pending'),
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

def create_streamlit_frontend():
    # Add theme toggle button
    create_theme_toggle()
    
    # Apply theme styles
    st.markdown(get_theme_styles(), unsafe_allow_html=True)
    
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
                st.session_state.trainsets = optimized_trainsets
                st.session_state.current_metrics = metrics
                st.session_state.current_alerts = alerts
                st.session_state.maintenance_predictions = maintenance_pred
                st.success("Optimization completed!")
        
        # Data source status
        st.subheader("🔗 Data Sources")
        for source, status in st.session_state.system_manager.data_integrator.data_sources.items():
            status_icon = "🟢" if status['connected'] else "🔴"
            st.write(f"{status_icon} {source.replace('_', ' ').title()}")
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard", "🚆 Fleet Status", "🔧 Maintenance", 
        "📢 Branding", "⚠️ Alerts", "📈 Analytics"
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

# Run the application
if __name__ == "__main__":
    create_streamlit_frontend()