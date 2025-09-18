from common_imports import *

class PredictiveMaintenanceModel:
    def __init__(self):
        self.model = None
        self.cost_model = None
        self.severity_model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = None
        
    def prepare_training_data(self, historical_data):
        """Prepare training data from historical records"""
        features = []
        labels = []
        cost_labels = []
        severity_labels = []
        
        for record in historical_data:
            # Feature engineering
            feature_vector = [
                record['mileage']['total_km'],
                record['mileage']['since_maintenance'],
                sum(record['mileage']['component_wear'].values()) / 3,  # Average wear
                record['job_cards']['open'],
                1 if record['fitness']['rolling_stock'] else 0,
                1 if record['fitness']['signalling'] else 0,
                1 if record['fitness']['telecom'] else 0,
                (record['operational']['last_service'] - datetime.now()).days if record['operational']['last_service'] else 30,
                record['operational']['reliability_score']
            ]
            
            # Label: days until next maintenance (simplified)
            maintenance_urgency = (
                (100 - record['operational']['reliability_score']) / 10 +
                record['job_cards']['open'] * 2 +
                sum(record['mileage']['component_wear'].values()) / 30
            )
            label = max(1, min(30, 30 - maintenance_urgency))
            
            # Cost prediction label (estimated based on wear and urgency)
            cost_label = (
                sum(record['mileage']['component_wear'].values()) * 100 +
                record['job_cards']['open'] * 5000 +
                maintenance_urgency * 2000
            )
            
            # Severity classification (0: Low, 1: Medium, 2: High, 3: Critical)
            if maintenance_urgency > 20:
                severity_label = 3  # Critical
            elif maintenance_urgency > 15:
                severity_label = 2  # High
            elif maintenance_urgency > 10:
                severity_label = 1  # Medium
            else:
                severity_label = 0  # Low
            
            features.append(feature_vector)
            labels.append(label)
            cost_labels.append(cost_label)
            severity_labels.append(severity_label)
            
        return np.array(features), np.array(labels), np.array(cost_labels), np.array(severity_labels)
        
    def train_model(self, historical_data):
        """Train the predictive maintenance model"""
        try:
            features, labels, cost_labels, severity_labels = self.prepare_training_data(historical_data)
            if len(features) < 10:
                # Not enough data for proper training
                self.is_trained = False
                return False
                
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train maintenance prediction model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(features_scaled, labels)
            
            # Train cost prediction model
            self.cost_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
            self.cost_model.fit(features_scaled, cost_labels)
            
            # Train severity classification model
            self.severity_model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.severity_model.fit(features_scaled, severity_labels)
            
            self.is_trained = True
            
            # Store feature importance
            self.feature_importance = self.model.feature_importances_
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            self.is_trained = False
            return False
            
    def predict_maintenance(self, trainsets):
        """Predict maintenance needs for all trainsets"""
        if not self.is_trained or self.model is None:
            return self._fallback_predictions(trainsets)
        predictions = []
        for trainset in trainsets:
            try:
                # Prepare features for prediction
                features = np.array([[
                    trainset['mileage']['total_km'],
                    trainset['mileage']['since_maintenance'],
                    sum(trainset['mileage']['component_wear'].values()) / 3,
                    trainset['job_cards']['open'],
                    1 if trainset['fitness']['rolling_stock'] else 0,
                    1 if trainset['fitness']['signalling'] else 0,
                    1 if trainset['fitness']['telecom'] else 0,
                    (trainset['operational']['last_service'] - datetime.now()).days if trainset['operational']['last_service'] else 30,
                    trainset['operational']['reliability_score']
                ]])
                
                # Scale and predict
                features_scaled = self.scaler.transform(features)
                days_until_maintenance = self.model.predict(features_scaled)[0]
                predicted_cost = self.cost_model.predict(features_scaled)[0]
                severity_pred = self.severity_model.predict(features_scaled)[0]
                severity_prob = self.severity_model.predict_proba(features_scaled)[0]
                
                # Calculate risk score
                risk_score = min(100, max(0, 100 - (days_until_maintenance / 30 * 100)))
                
                # Determine recommendation
                if risk_score > 75:
                    action = 'Schedule Immediately'
                    priority = 'High'
                elif risk_score > 50:
                    action = 'Schedule Soon'
                    priority = 'Medium'
                elif risk_score > 25:
                    action = 'Monitor Closely'
                    priority = 'Low'
                else:
                    action = 'OK'
                    priority = 'None'
                
                # Severity mapping
                severity_map = {0: 'Low', 1: 'Medium', 2: 'High', 3: 'Critical'}
                severity_level = severity_map.get(severity_pred, 'Low')
                
                predictions.append({
                    'trainset_id': trainset['id'],
                    'risk_score': round(risk_score, 1),
                    'days_until_maintenance': round(max(0, days_until_maintenance), 1),
                    'predicted_cost': round(predicted_cost, 2),
                    'severity_level': severity_level,
                    'severity_probability': round(max(severity_prob), 3),
                    'recommended_action': action,
                    'priority': priority,
                    'confidence': 'High' if self.is_trained else 'Low'
                })
            except Exception as e:
                # Fallback if prediction fails
                predictions.append(self._fallback_prediction(trainset))
        return pd.DataFrame(predictions)
        
    def predict_maintenance_cost(self, trainset):
        """Predict maintenance cost for a specific trainset"""
        if not self.is_trained or self.cost_model is None:
            return None
        
        try:
            features = np.array([[
                trainset['mileage']['total_km'],
                trainset['mileage']['since_maintenance'],
                sum(trainset['mileage']['component_wear'].values()) / 3,
                trainset['job_cards']['open'],
                1 if trainset['fitness']['rolling_stock'] else 0,
                1 if trainset['fitness']['signalling'] else 0,
                1 if trainset['fitness']['telecom'] else 0,
                (trainset['operational']['last_service'] - datetime.now()).days if trainset['operational']['last_service'] else 30,
                trainset['operational']['reliability_score']
            ]])
            
            features_scaled = self.scaler.transform(features)
            predicted_cost = self.cost_model.predict(features_scaled)[0]
            
            return max(0, predicted_cost)
        except Exception as e:
            print(f"Cost prediction error: {e}")
            return None
    
    def predict_failure_severity(self, trainset):
        """Predict failure severity for a specific trainset"""
        if not self.is_trained or self.severity_model is None:
            return None
        
        try:
            features = np.array([[
                trainset['mileage']['total_km'],
                trainset['mileage']['since_maintenance'],
                sum(trainset['mileage']['component_wear'].values()) / 3,
                trainset['job_cards']['open'],
                1 if trainset['fitness']['rolling_stock'] else 0,
                1 if trainset['fitness']['signalling'] else 0,
                1 if trainset['fitness']['telecom'] else 0,
                (trainset['operational']['last_service'] - datetime.now()).days if trainset['operational']['last_service'] else 30,
                trainset['operational']['reliability_score']
            ]])
            
            features_scaled = self.scaler.transform(features)
            severity_pred = self.severity_model.predict(features_scaled)[0]
            severity_prob = self.severity_model.predict_proba(features_scaled)[0]
            
            severity_map = {0: 'Low', 1: 'Medium', 2: 'High', 3: 'Critical'}
            severity_level = severity_map.get(severity_pred, 'Low')
            
            return {
                'severity_level': severity_level,
                'confidence': round(max(severity_prob), 3),
                'probabilities': {
                    'Low': round(severity_prob[0], 3),
                    'Medium': round(severity_prob[1], 3),
                    'High': round(severity_prob[2], 3),
                    'Critical': round(severity_prob[3], 3)
                }
            }
        except Exception as e:
            print(f"Severity prediction error: {e}")
            return None
        
    def get_model_performance(self):
        """Get model performance metrics"""
        if not self.is_trained:
            return None
        return {
            'is_trained': self.is_trained,
            'feature_importance': self.feature_importance.tolist() if self.feature_importance is not None else None,
            'model_type': 'Random Forest Regressor',
            'cost_model_type': 'Gradient Boosting Regressor',
            'severity_model_type': 'Random Forest Classifier'
        }
        
    def _fallback_predictions(self, trainsets):
        """Fallback predictions when model is not trained"""
        return pd.DataFrame([self._fallback_prediction(t) for t in trainsets])
        
    def _fallback_prediction(self, trainset):
        """Simple heuristic-based fallback prediction"""
        wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
        mileage_ratio = trainset['mileage']['since_maintenance'] / 10000
        risk_score = min(100, max(0, wear_avg * 0.7 + mileage_ratio * 30))
        days_until_maintenance = max(0, 30 - (risk_score / 100 * 30))
        
        # Estimate cost
        estimated_cost = wear_avg * 100 + trainset['job_cards']['open'] * 5000
        
        if risk_score > 70:
            action = 'Schedule Soon'
            priority = 'High'
            severity = 'High'
        elif risk_score > 40:
            action = 'Monitor'
            priority = 'Medium'
            severity = 'Medium'
        else:
            action = 'OK'
            priority = 'Low'
            severity = 'Low'
            
        return {
            'trainset_id': trainset['id'],
            'risk_score': round(risk_score, 1),
            'days_until_maintenance': round(days_until_maintenance, 1),
            'predicted_cost': round(estimated_cost, 2),
            'severity_level': severity,
            'severity_probability': 0.7,
            'recommended_action': action,
            'priority': priority,
            'confidence': 'Low (Heuristic)'
        }