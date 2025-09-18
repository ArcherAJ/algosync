from common_imports import *

class EnergyConsumptionOptimizer:
    """
    ML-powered energy consumption optimization system
    Uses multiple algorithms for energy prediction and optimization
    """
    
    def __init__(self):
        self.energy_model = None
        self.cost_model = None
        self.renewable_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = None
        self.label_encoders = {}
        self.data = None
        self.feature_data = None
        self.feature_columns = []
        
    def load_data(self):
        """Load energy consumption data from CSV"""
        try:
            csv_path = os.path.join(os.path.dirname(__file__), "energy_consumption.csv")
            self.data = pd.read_csv(csv_path)
            
            # Create additional features
            self.data['month'] = pd.to_datetime(self.data[['year', 'month']].assign(day=1))
            self.data['season'] = self.data['month'].dt.month.map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
            })
            
            return True
        except Exception as e:
            st.error(f"Error loading energy consumption data: {e}")
            return False
    
    def preprocess_data(self):
        """Preprocess data for ML models"""
        if self.data is None:
            return False
            
        # Create feature columns
        self.feature_data = self.data.copy()
        
        # Encode categorical variables
        le = LabelEncoder()
        self.feature_data['season_encoded'] = le.fit_transform(self.feature_data['season'])
        self.label_encoders['season'] = le
        
        # Create additional features
        self.feature_data['efficiency_score'] = self.feature_data['passengers_carried'] / self.feature_data['energy_consumption_kwh']
        self.feature_data['renewable_energy'] = self.feature_data['energy_consumption_kwh'] * self.feature_data['renewable_percentage'] / 100
        self.feature_data['non_renewable_energy'] = self.feature_data['energy_consumption_kwh'] * (1 - self.feature_data['renewable_percentage'] / 100)
        
        # Define feature columns for ML (exclude datetime columns)
        self.feature_columns = [
            'distance_traveled_km', 'passengers_carried', 'season_encoded',
            'maintenance_impact', 'efficiency_score', 'renewable_percentage'
        ]
        
        return True
    
    def train_models(self):
        """Train multiple ML models for energy optimization"""
        if not self.preprocess_data():
            return False
        
        # Prepare features and targets
        X = self.feature_data[self.feature_columns]
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train energy consumption prediction model
        y_energy = self.feature_data['energy_consumption_kwh']
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_energy, test_size=0.2, random_state=42)
        
        # Use SVR for energy prediction
        self.energy_model = SVR(kernel='rbf', C=100, gamma='scale')
        self.energy_model.fit(X_train, y_train)
        
        # Train cost optimization model
        y_cost = self.feature_data['energy_consumption_kwh'] * self.feature_data['cost_per_kwh']
        X_train_cost, X_test_cost, y_train_cost, y_test_cost = train_test_split(X_scaled, y_cost, test_size=0.2, random_state=42)
        
        self.cost_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.cost_model.fit(X_train_cost, y_train_cost)
        
        # Train renewable energy optimization model
        y_renewable = self.feature_data['renewable_percentage']
        X_train_renewable, X_test_renewable, y_train_renewable, y_test_renewable = train_test_split(
            X_scaled, y_renewable, test_size=0.2, random_state=42
        )
        
        self.renewable_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.renewable_model.fit(X_train_renewable, y_train_renewable)
        
        # Store feature importance
        if hasattr(self.cost_model, 'feature_importances_'):
            self.feature_importance = self.cost_model.feature_importances_
        
        self.is_trained = True
        return True
    
    def predict_energy_consumption(self, distance_km, passengers, month, maintenance_impact=1.0):
        """Predict energy consumption for given parameters"""
        if not self.is_trained:
            return None
        
        try:
            # Prepare input features (matching the feature_columns order)
            features = []
            features.append(distance_km)  # distance_traveled_km
            features.append(passengers)  # passengers_carried
            
            # Season encoding
            season_map = {12: 'Winter', 1: 'Winter', 2: 'Winter',
                         3: 'Spring', 4: 'Spring', 5: 'Spring',
                         6: 'Summer', 7: 'Summer', 8: 'Summer',
                         9: 'Autumn', 10: 'Autumn', 11: 'Autumn'}
            season = season_map.get(month, 'Spring')
            
            if 'season' in self.label_encoders:
                season_encoded = self.label_encoders['season'].transform([season])[0]
            else:
                season_encoded = 0
            features.append(season_encoded)  # season_encoded
            
            features.append(maintenance_impact)  # maintenance_impact
            
            # Efficiency score (estimated)
            efficiency_score = passengers / max(distance_km, 1)
            features.append(efficiency_score)  # efficiency_score
            
            # Renewable percentage (estimated based on month - higher in summer)
            renewable_pct = 30 + (month - 6) * 2 if 6 <= month <= 8 else 30
            features.append(renewable_pct)  # renewable_percentage
            
            # Scale and predict
            features_scaled = self.scaler.transform([features])
            predicted_energy = self.energy_model.predict(features_scaled)[0]
            
            return max(0, predicted_energy)
            
        except Exception as e:
            print(f"Energy prediction error: {e}")
            return None
    
    def predict_cost(self, distance_km, passengers, month, maintenance_impact=1.0, cost_per_kwh=7.0):
        """Predict energy cost for given parameters"""
        if not self.is_trained:
            return None
        
        try:
            # Get energy prediction first
            predicted_energy = self.predict_energy_consumption(distance_km, passengers, month, maintenance_impact)
            if predicted_energy is None:
                return None
            
            # Prepare features for cost model (matching feature_columns order)
            features = []
            features.append(distance_km)  # distance_traveled_km
            features.append(passengers)  # passengers_carried
            
            # Season encoding
            season_map = {12: 'Winter', 1: 'Winter', 2: 'Winter',
                         3: 'Spring', 4: 'Spring', 5: 'Spring',
                         6: 'Summer', 7: 'Summer', 8: 'Summer',
                         9: 'Autumn', 10: 'Autumn', 11: 'Autumn'}
            season = season_map.get(month, 'Spring')
            
            if 'season' in self.label_encoders:
                season_encoded = self.label_encoders['season'].transform([season])[0]
            else:
                season_encoded = 0
            features.append(season_encoded)  # season_encoded
            
            features.append(maintenance_impact)  # maintenance_impact
            features.append(passengers / max(distance_km, 1))  # efficiency_score
            features.append(30 + (month - 6) * 2 if 6 <= month <= 8 else 30)  # renewable_percentage
            
            features_scaled = self.scaler.transform([features])
            predicted_cost = self.cost_model.predict(features_scaled)[0]
            
            return max(0, predicted_cost)
            
        except Exception as e:
            print(f"Cost prediction error: {e}")
            return None
    
    def optimize_renewable_energy(self, distance_km, passengers, month):
        """Optimize renewable energy percentage"""
        if not self.is_trained:
            return None
        
        try:
            # Prepare features (matching feature_columns order)
            features = []
            features.append(distance_km)  # distance_traveled_km
            features.append(passengers)  # passengers_carried
            
            # Season encoding
            season_map = {12: 'Winter', 1: 'Winter', 2: 'Winter',
                         3: 'Spring', 4: 'Spring', 5: 'Spring',
                         6: 'Summer', 7: 'Summer', 8: 'Summer',
                         9: 'Autumn', 10: 'Autumn', 11: 'Autumn'}
            season = season_map.get(month, 'Spring')
            
            if 'season' in self.label_encoders:
                season_encoded = self.label_encoders['season'].transform([season])[0]
            else:
                season_encoded = 0
            features.append(season_encoded)  # season_encoded
            
            features.append(1.0)  # maintenance_impact
            features.append(passengers / max(distance_km, 1))  # efficiency_score
            features.append(30)  # renewable_percentage
            
            features_scaled = self.scaler.transform([features])
            optimal_renewable = self.renewable_model.predict(features_scaled)[0]
            
            return max(0, min(100, optimal_renewable))
            
        except Exception as e:
            print(f"Renewable optimization error: {e}")
            return None
    
    def get_energy_optimization_recommendations(self, distance_km, passengers, month):
        """Get comprehensive energy optimization recommendations"""
        if not self.is_trained:
            return None
        
        # Get predictions
        predicted_energy = self.predict_energy_consumption(distance_km, passengers, month)
        predicted_cost = self.predict_cost(distance_km, passengers, month)
        optimal_renewable = self.optimize_renewable_energy(distance_km, passengers, month)
        
        if any(x is None for x in [predicted_energy, predicted_cost, optimal_renewable]):
            return None
        
        # Calculate efficiency metrics
        efficiency_score = passengers / max(distance_km, 1)
        energy_per_passenger = predicted_energy / max(passengers, 1)
        energy_per_km = predicted_energy / max(distance_km, 1)
        
        # Generate recommendations
        recommendations = []
        
        if energy_per_passenger > 0.08:
            recommendations.append("High energy per passenger - consider optimizing passenger capacity")
        
        if energy_per_km > 1.5:
            recommendations.append("High energy per km - check train efficiency and maintenance")
        
        if optimal_renewable > 40:
            recommendations.append(f"Increase renewable energy to {optimal_renewable:.1f}% for better efficiency")
        
        if efficiency_score < 0.5:
            recommendations.append("Low efficiency score - review operational parameters")
        
        return {
            'predicted_energy_kwh': predicted_energy,
            'predicted_cost': predicted_cost,
            'optimal_renewable_percentage': optimal_renewable,
            'efficiency_score': efficiency_score,
            'energy_per_passenger': energy_per_passenger,
            'energy_per_km': energy_per_km,
            'recommendations': recommendations,
            'savings_potential': {
                'renewable_optimization': predicted_cost * 0.1,  # 10% savings potential
                'efficiency_improvement': predicted_cost * 0.15,  # 15% savings potential
                'maintenance_optimization': predicted_cost * 0.05  # 5% savings potential
            }
        }
    
    def get_model_performance(self):
        """Get model performance metrics"""
        if not self.is_trained:
            return None
        
        # Calculate performance for energy model
        X = self.feature_data[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        
        y_energy = self.feature_data['energy_consumption_kwh']
        energy_pred = self.energy_model.predict(X_scaled)
        energy_r2 = r2_score(y_energy, energy_pred)
        energy_rmse = np.sqrt(mean_squared_error(y_energy, energy_pred))
        
        # Calculate performance for cost model
        y_cost = self.feature_data['energy_consumption_kwh'] * self.feature_data['cost_per_kwh']
        cost_pred = self.cost_model.predict(X_scaled)
        cost_r2 = r2_score(y_cost, cost_pred)
        cost_rmse = np.sqrt(mean_squared_error(y_cost, cost_pred))
        
        # Calculate performance for renewable model
        y_renewable = self.feature_data['renewable_percentage']
        renewable_pred = self.renewable_model.predict(X_scaled)
        renewable_r2 = r2_score(y_renewable, renewable_pred)
        renewable_rmse = np.sqrt(mean_squared_error(y_renewable, renewable_pred))
        
        return {
            'energy_prediction': {
                'r2': energy_r2,
                'rmse': energy_rmse,
                'model_type': 'Support Vector Regression'
            },
            'cost_prediction': {
                'r2': cost_r2,
                'rmse': cost_rmse,
                'model_type': 'Random Forest'
            },
            'renewable_optimization': {
                'r2': renewable_r2,
                'rmse': renewable_rmse,
                'model_type': 'Gradient Boosting'
            },
            'feature_importance': self.feature_importance.tolist() if self.feature_importance is not None else None
        }
    
    def get_monthly_forecast(self, year, month):
        """Get energy forecast for a specific month"""
        if not self.is_trained:
            return None
        
        # Use historical data to estimate monthly parameters
        monthly_data = self.data[self.data['month'] == month]
        if monthly_data.empty:
            return None
        
        avg_distance = monthly_data['distance_traveled_km'].mean()
        avg_passengers = monthly_data['passengers_carried'].mean()
        
        # Get predictions
        predicted_energy = self.predict_energy_consumption(avg_distance, avg_passengers, month)
        predicted_cost = self.predict_cost(avg_distance, avg_passengers, month)
        optimal_renewable = self.optimize_renewable_energy(avg_distance, avg_passengers, month)
        
        if any(x is None for x in [predicted_energy, predicted_cost, optimal_renewable]):
            return None
        
        return {
            'month': month,
            'year': year,
            'predicted_energy_kwh': predicted_energy,
            'predicted_cost': predicted_cost,
            'optimal_renewable_percentage': optimal_renewable,
            'estimated_distance_km': avg_distance,
            'estimated_passengers': avg_passengers,
            'efficiency_score': avg_passengers / max(avg_distance, 1)
        }
