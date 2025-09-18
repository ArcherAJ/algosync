from common_imports import *

# ML Model Classes
class AdvertisementMLPredictor:
    def __init__(self):
        self.revenue_model = None
        self.engagement_model = None
        self.roi_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        
    def load_data(self):
        """Load advertisement performance data from CSV"""
        try:
            csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "advertisement_performance.csv")
            self.data = pd.read_csv(csv_path)
            return True
        except Exception as e:
            st.error(f"Error loading CSV data: {e}")
            return False
    
    def preprocess_data(self):
        """Preprocess data for ML models"""
        if self.data is None:
            return False
            
        # Create feature columns
        self.feature_data = self.data.copy()
        
        # Encode categorical variables
        categorical_columns = ['advertiser', 'category', 'subcategory', 'target_demographic', 'compartment_type']
        for col in categorical_columns:
            if col in self.feature_data.columns:
                le = LabelEncoder()
                self.feature_data[f'{col}_encoded'] = le.fit_transform(self.feature_data[col].astype(str))
                self.label_encoders[col] = le
        
        # Create additional features
        self.feature_data['investment_per_day'] = self.feature_data['investment'] / self.feature_data['duration_days']
        self.feature_data['impressions_per_day'] = self.feature_data['impressions'] / self.feature_data['duration_days']
        self.feature_data['revenue_per_day'] = self.feature_data['revenue_generated'] / self.feature_data['duration_days']
        
        # Define feature columns for ML
        self.feature_columns = [
            'duration_days', 'investment', 'impressions', 'engagement_rate',
            'investment_per_day', 'impressions_per_day'
        ]
        
        # Add encoded categorical features
        for col in categorical_columns:
            if f'{col}_encoded' in self.feature_data.columns:
                self.feature_columns.append(f'{col}_encoded')
        
        return True
    
    def train_models(self):
        """Train ML models for different predictions"""
        if not self.preprocess_data():
            return False
        
        # Prepare features and targets
        X = self.feature_data[self.feature_columns]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train revenue prediction model
        y_revenue = self.feature_data['revenue_generated']
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_revenue, test_size=0.2, random_state=42)
        
        self.revenue_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.revenue_model.fit(X_train, y_train)
        
        # Train engagement prediction model
        y_engagement = self.feature_data['engagement_rate']
        X_train_eng, X_test_eng, y_train_eng, y_test_eng = train_test_split(X_scaled, y_engagement, test_size=0.2, random_state=42)
        
        self.engagement_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.engagement_model.fit(X_train_eng, y_train_eng)
        
        # Train ROI prediction model
        y_roi = self.feature_data['roi']
        X_train_roi, X_test_roi, y_train_roi, y_test_roi = train_test_split(X_scaled, y_roi, test_size=0.2, random_state=42)
        
        self.roi_model = Ridge(alpha=1.0)
        self.roi_model.fit(X_train_roi, y_train_roi)
        
        self.is_trained = True
        return True
    
    def predict_revenue(self, campaign_data):
        """Predict revenue for a campaign"""
        if not self.is_trained:
            return None
        
        # Prepare input features
        features = self._prepare_features(campaign_data)
        if features is None:
            return None
        
        features_scaled = self.scaler.transform([features])
        return self.revenue_model.predict(features_scaled)[0]
    
    def predict_engagement(self, campaign_data):
        """Predict engagement rate for a campaign"""
        if not self.is_trained:
            return None
        
        features = self._prepare_features(campaign_data)
        if features is None:
            return None
        
        features_scaled = self.scaler.transform([features])
        return self.engagement_model.predict(features_scaled)[0]
    
    def predict_roi(self, campaign_data):
        """Predict ROI for a campaign"""
        if not self.is_trained:
            return None
        
        features = self._prepare_features(campaign_data)
        if features is None:
            return None
        
        features_scaled = self.scaler.transform([features])
        return self.roi_model.predict(features_scaled)[0]
    
    def _prepare_features(self, campaign_data):
        """Prepare features for prediction"""
        try:
            features = []
            
            # Numerical features
            for col in ['duration_days', 'investment', 'impressions', 'engagement_rate']:
                if col in campaign_data:
                    features.append(campaign_data[col])
                else:
                    return None
            
            # Calculate derived features
            investment_per_day = campaign_data['investment'] / campaign_data['duration_days']
            impressions_per_day = campaign_data['impressions'] / campaign_data['duration_days']
            features.extend([investment_per_day, impressions_per_day])
            
            # Categorical features
            categorical_columns = ['advertiser', 'category', 'subcategory', 'target_demographic', 'compartment_type']
            for col in categorical_columns:
                if col in campaign_data and col in self.label_encoders:
                    try:
                        encoded_value = self.label_encoders[col].transform([campaign_data[col]])[0]
                        features.append(encoded_value)
                    except:
                        # If value not seen during training, use 0
                        features.append(0)
                else:
                    features.append(0)
            
            return features
        except:
            return None
    
    def get_model_performance(self):
        """Get model performance metrics"""
        if not self.is_trained:
            return None
        
        # Calculate performance for each model
        X = self.feature_data[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        
        # Revenue model performance
        y_revenue = self.feature_data['revenue_generated']
        revenue_pred = self.revenue_model.predict(X_scaled)
        revenue_r2 = r2_score(y_revenue, revenue_pred)
        revenue_rmse = np.sqrt(mean_squared_error(y_revenue, revenue_pred))
        
        # Engagement model performance
        y_engagement = self.feature_data['engagement_rate']
        engagement_pred = self.engagement_model.predict(X_scaled)
        engagement_r2 = r2_score(y_engagement, engagement_pred)
        engagement_rmse = np.sqrt(mean_squared_error(y_engagement, engagement_pred))
        
        # ROI model performance
        y_roi = self.feature_data['roi']
        roi_pred = self.roi_model.predict(X_scaled)
        roi_r2 = r2_score(y_roi, roi_pred)
        roi_rmse = np.sqrt(mean_squared_error(y_roi, roi_pred))
        
        return {
            'revenue': {'r2': revenue_r2, 'rmse': revenue_rmse},
            'engagement': {'r2': engagement_r2, 'rmse': engagement_rmse},
            'roi': {'r2': roi_r2, 'rmse': roi_rmse}
        }

def create_branding_tab():
    st.markdown("""
    <style>
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        text-align: center;
        width: 100%;
        height: 180px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
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
        transform: translateY(-8px) scale(1.05);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.15),
            0 0 0 1px rgba(255,255,255,0.2),
            inset 0 1px 0 rgba(255,255,255,0.3);
    }
    
    .metric-title {
        font-size: 1rem;
        font-weight: 700;
        color: #333;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        color: #28a745;
        font-weight: 600;
        background: rgba(40, 167, 69, 0.1);
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        border: 1px solid rgba(40, 167, 69, 0.2);
    }
    
    .ml-section {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            0 0 0 1px rgba(255,255,255,0.1),
            inset 0 1px 0 rgba(255,255,255,0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    """Create the ML-powered branding & revenue management tab"""
    st.header("🤖 AI-Powered Branding & Revenue Management") 
    
    # Initialize ML predictor
    if 'ml_predictor' not in st.session_state:
        st.session_state.ml_predictor = AdvertisementMLPredictor()
    
    ml_predictor = st.session_state.ml_predictor
    
    # Load and train models
    if not ml_predictor.is_trained:
        with st.spinner("Loading advertisement data and training ML models..."):
            if ml_predictor.load_data():
                if ml_predictor.train_models():
                    st.success("✅ ML models trained successfully!")
                else:
                    st.error("❌ Failed to train ML models")
            else:
                st.error("❌ Failed to load advertisement data")
    
    if ml_predictor.is_trained:
        # Display ML model performance
        st.markdown('<div class="ml-section">', unsafe_allow_html=True)
        st.subheader("🧠 ML Model Performance")
        
        performance = ml_predictor.get_model_performance()
        if performance:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Revenue Prediction", f"R² = {performance['revenue']['r2']:.3f}", 
                         f"RMSE = {performance['revenue']['rmse']:.0f}")
            with col2:
                st.metric("Engagement Prediction", f"R² = {performance['engagement']['r2']:.3f}", 
                         f"RMSE = {performance['engagement']['rmse']:.4f}")
            with col3:
                st.metric("ROI Prediction", f"R² = {performance['roi']['r2']:.3f}", 
                         f"RMSE = {performance['roi']['rmse']:.3f}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Load advertisement data for analysis
        data = ml_predictor.data
        
        # Key metrics from CSV data
        total_revenue = data['revenue_generated'].sum()
        total_investment = data['investment'].sum()
        avg_roi = data['roi'].mean()
        total_campaigns = len(data)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #d4edda; color: #155724;">
                <div class="metric-title">Total Revenue Generated</div>
                <div class="metric-value">₹{total_revenue:,.0f}</div>
                <div class="metric-delta">From {total_campaigns} campaigns</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #fff3cd; color: #856404;">
                <div class="metric-title">Total Investment</div>
                <div class="metric-value">₹{total_investment:,.0f}</div>
                <div class="metric-delta">Campaign budget</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card" style="background-color: #d1ecf1; color: #0c5460;">
                <div class="metric-title">Average ROI</div>
                <div class="metric-value">{avg_roi:.2f}</div>
                <div class="metric-delta">Return on investment</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            top_performer = data.loc[data['roi'].idxmax()]
            st.markdown(f"""
            <div class="metric-card" style="background-color: #f8d7da; color: #721c24;">
                <div class="metric-title">Best Performer</div>
                <div class="metric-value">{top_performer['advertiser']}</div>
                <div class="metric-delta">ROI: {top_performer['roi']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        # ML-powered insights and predictions
        st.markdown('<div class="ml-section">', unsafe_allow_html=True)
        st.subheader("🔮 ML-Powered Campaign Predictions")
        
        # Campaign prediction interface
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Predict New Campaign")
            
            # Input fields for campaign prediction
            advertiser = st.selectbox("Advertiser", data['advertiser'].unique())
            category = st.selectbox("Category", data['category'].unique())
            subcategory = st.selectbox("Subcategory", data['subcategory'].unique())
            duration_days = st.slider("Duration (days)", 1, 365, 30)
            investment = st.number_input("Investment (₹)", min_value=1000, value=100000, step=1000)
            impressions = st.number_input("Expected Impressions", min_value=1000, value=50000, step=1000)
            target_demographic = st.selectbox("Target Demographic", data['target_demographic'].unique())
            compartment_type = st.selectbox("Compartment Type", data['compartment_type'].unique())
            
            if st.button("🔮 Predict Performance", type="primary"):
                campaign_data = {
                    'advertiser': advertiser,
                    'category': category,
                    'subcategory': subcategory,
                    'duration_days': duration_days,
                    'investment': investment,
                    'impressions': impressions,
                    'engagement_rate': data[data['advertiser'] == advertiser]['engagement_rate'].mean(),
                    'target_demographic': target_demographic,
                    'compartment_type': compartment_type
                }
                
                # Make predictions
                predicted_revenue = ml_predictor.predict_revenue(campaign_data)
                predicted_engagement = ml_predictor.predict_engagement(campaign_data)
                predicted_roi = ml_predictor.predict_roi(campaign_data)
                
                if predicted_revenue is not None:
                    st.success("✅ Predictions Generated!")
                    
                    col_pred1, col_pred2, col_pred3 = st.columns(3)
                    with col_pred1:
                        st.metric("Predicted Revenue", f"₹{predicted_revenue:,.0f}")
                    with col_pred2:
                        st.metric("Predicted Engagement", f"{predicted_engagement:.3f}")
                    with col_pred3:
                        st.metric("Predicted ROI", f"{predicted_roi:.3f}")
                    
                    # ROI Analysis
                    if predicted_roi > 0.5:
                        st.success("🎯 Excellent ROI potential! This campaign is highly recommended.")
                    elif predicted_roi > 0.2:
                        st.info("👍 Good ROI potential. Consider this campaign.")
                    elif predicted_roi > 0:
                        st.warning("⚠️ Low ROI potential. Review campaign parameters.")
                    else:
                        st.error("❌ Negative ROI predicted. Not recommended.")
        
        with col2:
            st.subheader("Top Performing Campaigns")
            
            # Display top performing campaigns
            top_campaigns = data.nlargest(10, 'roi')[['advertiser', 'category', 'revenue_generated', 'roi', 'engagement_rate']]
            
            fig = px.bar(top_campaigns, x='advertiser', y='roi', 
                        title="Top 10 Campaigns by ROI",
                        color='engagement_rate',
                        color_continuous_scale='Viridis')
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Advanced analytics
        st.subheader("📊 Advanced Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Revenue by category
            category_revenue = data.groupby('category')['revenue_generated'].sum().reset_index()
            fig = px.pie(category_revenue, values='revenue_generated', names='category',
                        title="Revenue Distribution by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # ROI vs Investment scatter plot
            fig = px.scatter(data, x='investment', y='roi', color='category',
                           title="ROI vs Investment by Category",
                           hover_data=['advertiser', 'engagement_rate'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Engagement rate analysis
        st.subheader("📈 Engagement Rate Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Engagement by demographic
            demo_engagement = data.groupby('target_demographic')['engagement_rate'].mean().reset_index()
            fig = px.bar(demo_engagement, x='target_demographic', y='engagement_rate',
                        title="Average Engagement Rate by Demographic")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Peak hour performance analysis
            fig = px.box(data, x='compartment_type', y='peak_hour_performance',
                        title="Peak Hour Performance by Compartment Type")
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed campaign data
        st.subheader("📋 Campaign Performance Data")
        
        # Add filters
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_advertiser = st.selectbox("Filter by Advertiser", ["All"] + list(data['advertiser'].unique()))
        with col2:
            selected_category = st.selectbox("Filter by Category", ["All"] + list(data['category'].unique()))
        with col3:
            min_roi = st.slider("Minimum ROI", float(data['roi'].min()), float(data['roi'].max()), 0.0)
        
        # Apply filters
        filtered_data = data.copy()
        if selected_advertiser != "All":
            filtered_data = filtered_data[filtered_data['advertiser'] == selected_advertiser]
        if selected_category != "All":
            filtered_data = filtered_data[filtered_data['category'] == selected_category]
        filtered_data = filtered_data[filtered_data['roi'] >= min_roi]
        
        # Display filtered data
        st.dataframe(filtered_data[['campaign_id', 'advertiser', 'category', 'subcategory', 
                                  'revenue_generated', 'roi', 'engagement_rate', 'target_demographic']], 
                    use_container_width=True)
        
        # Export functionality
        st.subheader("📤 Export Data")
        
        col1, col2 = st.columns(2)
        with col1:
            csv_data = filtered_data.to_csv(index=False)
            st.download_button(
                label="Download Filtered Data as CSV",
                data=csv_data,
                file_name="filtered_campaign_data.csv",
                mime="text/csv"
            )
        
        with col2:
            # Export ML predictions
            if st.button("Export ML Model Performance"):
                model_perf = ml_predictor.get_model_performance()
                perf_df = pd.DataFrame.from_dict(model_perf, orient='index')
                csv_perf = perf_df.to_csv()
                st.download_button(
                    label="Download Model Performance",
                    data=csv_perf,
                    file_name="ml_model_performance.csv",
                    mime="text/csv"
                )
    
    else:
        st.error("❌ Unable to load advertisement data. Please check if the CSV file exists and is accessible.")