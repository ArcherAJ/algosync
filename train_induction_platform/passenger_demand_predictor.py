from common_imports import *

class PassengerDemandPredictor:
    """
    Advanced ML-powered passenger demand forecasting system
    Uses multiple algorithms for accurate demand prediction
    """
    
    def __init__(self):
        self.demand_model = None
        self.peak_classifier = None
        self.seasonal_model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.is_trained = False
        self.feature_importance = None
        
    def load_data(self):
        """Load passenger demand data from CSV"""
        try:
            csv_path = os.path.join(os.path.dirname(__file__), "passenger_demand_data.csv")
            self.data = pd.read_csv(csv_path)
            
            # Convert time_slot to datetime for better processing
            self.data['datetime'] = pd.to_datetime(self.data['time_slot'].str.split('-').str[0], format='%H:%M')
            self.data['hour'] = self.data['datetime'].dt.hour
            self.data['day_of_week'] = pd.to_datetime('2024-01-01').dt.dayofweek  # Placeholder
            
            return True
        except Exception as e:
            st.error(f"Error loading passenger demand data: {e}")
            return False
    
    def preprocess_data(self):
        """Preprocess data for ML models"""
        if self.data is None:
            return False
            
        # Create feature columns
        self.feature_data = self.data.copy()
        
        # Encode categorical variables
        categorical_columns = ['station_name', 'day_type']
        for col in categorical_columns:
            if col in self.feature_data.columns:
                le = LabelEncoder()
                self.feature_data[f'{col}_encoded'] = le.fit_transform(self.feature_data[col].astype(str))
                self.label_encoders[col] = le
        
        # Create additional features
        self.feature_data['peak_hour'] = ((self.feature_data['hour'] >= 7) & (self.feature_data['hour'] <= 9)) | \
                                        ((self.feature_data['hour'] >= 17) & (self.feature_data['hour'] <= 19))
        self.feature_data['peak_hour'] = self.feature_data['peak_hour'].astype(int)
        
        # Define feature columns for ML
        self.feature_columns = [
            'hour', 'peak_hour', 'peak_factor', 'weather_impact', 'event_impact'
        ]
        
        # Add encoded categorical features
        for col in categorical_columns:
            if f'{col}_encoded' in self.feature_data.columns:
                self.feature_columns.append(f'{col}_encoded')
        
        return True
    
    def train_models(self):
        """Train multiple ML models for demand prediction"""
        if not self.preprocess_data():
            return False
        
        # Prepare features and targets
        X = self.feature_data[self.feature_columns]
        y_demand = self.feature_data['passenger_count']
        y_peak = self.feature_data['peak_hour']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train demand prediction model
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_demand, test_size=0.2, random_state=42)
        
        # Use XGBoost if available, otherwise Gradient Boosting
        if XGBOOST_AVAILABLE:
            self.demand_model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        else:
            self.demand_model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        
        self.demand_model.fit(X_train, y_train)
        
        # Train peak hour classifier
        X_train_peak, X_test_peak, y_train_peak, y_test_peak = train_test_split(
            X_scaled, y_peak, test_size=0.2, random_state=42
        )
        
        self.peak_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.peak_classifier.fit(X_train_peak, y_train_peak)
        
        # Store feature importance
        if hasattr(self.demand_model, 'feature_importances_'):
            self.feature_importance = self.demand_model.feature_importances_
        
        self.is_trained = True
        return True
    
    def predict_demand(self, station_name, hour, day_type='Weekday', weather_impact=0.95, event_impact=1.0):
        """Predict passenger demand for given parameters"""
        if not self.is_trained:
            return None
        
        try:
            # Prepare input features
            features = []
            
            # Hour
            features.append(hour)
            
            # Peak hour classification
            peak_hour = 1 if ((hour >= 7 and hour <= 9) or (hour >= 17 and hour <= 19)) else 0
            features.append(peak_hour)
            
            # Peak factor (estimated based on hour)
            if peak_hour:
                peak_factor = 1.5 + (hour % 2) * 0.3
            else:
                peak_factor = 0.7 + (hour % 3) * 0.2
            features.append(peak_factor)
            
            # Weather and event impact
            features.append(weather_impact)
            features.append(event_impact)
            
            # Categorical features
            if 'station_name' in self.label_encoders:
                try:
                    station_encoded = self.label_encoders['station_name'].transform([station_name])[0]
                except:
                    station_encoded = 0
                features.append(station_encoded)
            
            if 'day_type' in self.label_encoders:
                try:
                    day_encoded = self.label_encoders['day_type'].transform([day_type])[0]
                except:
                    day_encoded = 0
                features.append(day_encoded)
            
            # Scale and predict
            features_scaled = self.scaler.transform([features])
            predicted_demand = self.demand_model.predict(features_scaled)[0]
            
            return max(0, int(predicted_demand))
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    
    def predict_peak_hour(self, station_name, hour, day_type='Weekday'):
        """Predict if given hour is peak hour"""
        if not self.is_trained:
            return None
        
        try:
            # Prepare features (same as demand prediction)
            features = []
            features.append(hour)
            peak_hour = 1 if ((hour >= 7 and hour <= 9) or (hour >= 17 and hour <= 19)) else 0
            features.append(peak_hour)
            
            peak_factor = 1.5 if peak_hour else 0.7
            features.append(peak_factor)
            features.append(0.95)  # weather_impact
            features.append(1.0)   # event_impact
            
            # Categorical features
            if 'station_name' in self.label_encoders:
                try:
                    station_encoded = self.label_encoders['station_name'].transform([station_name])[0]
                except:
                    station_encoded = 0
                features.append(station_encoded)
            
            if 'day_type' in self.label_encoders:
                try:
                    day_encoded = self.label_encoders['day_type'].transform([day_type])[0]
                except:
                    day_encoded = 0
                features.append(day_encoded)
            
            features_scaled = self.scaler.transform([features])
            peak_probability = self.peak_classifier.predict_proba(features_scaled)[0][1]
            
            return peak_probability > 0.5, peak_probability
            
        except Exception as e:
            print(f"Peak hour prediction error: {e}")
            return None, None
    
    def get_demand_forecast(self, station_name, hours_ahead=24):
        """Get demand forecast for next N hours"""
        if not self.is_trained:
            return None
        
        forecast = []
        current_hour = datetime.now().hour
        
        for i in range(hours_ahead):
            hour = (current_hour + i) % 24
            predicted_demand = self.predict_demand(station_name, hour)
            is_peak, peak_prob = self.predict_peak_hour(station_name, hour)
            
            if predicted_demand is not None:
                forecast.append({
                    'hour': hour,
                    'predicted_demand': predicted_demand,
                    'is_peak_hour': is_peak,
                    'peak_probability': peak_prob,
                    'time_slot': f"{hour:02d}:00-{(hour+1)%24:02d}:00"
                })
        
        return forecast
    
    def get_model_performance(self):
        """Get model performance metrics"""
        if not self.is_trained:
            return None
        
        # Calculate performance for demand model
        X = self.feature_data[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        y_demand = self.feature_data['passenger_count']
        
        demand_pred = self.demand_model.predict(X_scaled)
        demand_r2 = r2_score(y_demand, demand_pred)
        demand_rmse = np.sqrt(mean_squared_error(y_demand, demand_pred))
        
        # Calculate performance for peak classifier
        y_peak = self.feature_data['peak_hour']
        peak_pred = self.peak_classifier.predict(X_scaled)
        peak_accuracy = (peak_pred == y_peak).mean()
        
        return {
            'demand_prediction': {
                'r2': demand_r2,
                'rmse': demand_rmse,
                'model_type': 'XGBoost' if XGBOOST_AVAILABLE else 'Gradient Boosting'
            },
            'peak_classification': {
                'accuracy': peak_accuracy,
                'model_type': 'Random Forest'
            },
            'feature_importance': self.feature_importance.tolist() if self.feature_importance is not None else None
        }
    
    def get_station_insights(self, station_name):
        """Get insights for a specific station"""
        if not self.is_trained:
            return None
        
        station_data = self.data[self.data['station_name'] == station_name]
        if station_data.empty:
            return None
        
        insights = {
            'station_name': station_name,
            'avg_daily_passengers': station_data['passenger_count'].mean(),
            'peak_hour_demand': station_data[station_data['peak_factor'] > 1.5]['passenger_count'].mean(),
            'off_peak_demand': station_data[station_data['peak_factor'] <= 1.5]['passenger_count'].mean(),
            'busiest_hour': station_data.loc[station_data['passenger_count'].idxmax(), 'time_slot'],
            'weather_sensitivity': station_data.groupby('weather_impact')['passenger_count'].mean().to_dict()
        }
        
        return insights
