"""
Enhanced KMRL AI Induction Planning Platform
Comprehensive AI-powered decision support with multi-objective optimization 
"""

from common_imports import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
warnings.filterwarnings('ignore')


def calculate_ai_score(trainset):
    """
    Calculate an AI score for a trainset based on multiple factors.
    Returns: (score: int, reasons: list of str)
    """
    score = 100
    reasons = []

    # Fitness
    if not trainset['fitness']['overall_valid']:
        score -= 30
        reasons.append("Invalid fitness certificate")

    # Job cards (open maintenance issues reduce score)
    open_jobs = trainset['job_cards']['open']
    if open_jobs > 0:
        penalty = min(20, open_jobs * 5)
        score -= penalty
        reasons.append(f"{open_jobs} open job cards")

    # Mileage & wear
    wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
    if wear_avg > 70:
        score -= 20
        reasons.append("High component wear")

    # Cleaning
    if trainset['cleaning']['interior_status'] != "Clean" or trainset['cleaning']['exterior_status'] != "Clean":
        score -= 10
        reasons.append("Requires cleaning")

    # Operational reliability
    reliability = trainset['operational']['reliability_score']
    score += (reliability - 70) // 2  # add some positive impact
    reasons.append(f"Reliability score {reliability}")

    # Branding
    if trainset['branding']['exposure_deficit'] > 10:
        score -= 10
        reasons.append("Branding exposure deficit")

    # Clamp between 0–100
    score = max(0, min(100, score))

    return score, reasons

# -----------------------
# Enhanced Data Generation & Simulation
# -----------------------
# -----------------------
# Enhanced Data Simulation
# -----------------------
class KMRLDataSimulator:
    def __init__(self, n_trainsets=25):
        self.n_trainsets = n_trainsets
        self.brands = ['Coca Cola', 'Pepsi', 'Samsung', 'Apple', 'Toyota', 'Flipkart', 'BSNL', 'Airtel', None]
        self.depots = ['Aluva Depot', 'Petta Depot']
        self.maintenance_types = ['Routine', 'Preventive', 'Corrective', 'Emergency']
        
    def simulate_real_time_updates(self, trainsets):
        """Simulate real-time data updates from various sources"""
        updated_count = 0
        for train in trainsets:
            # Simulate occasional status changes
            if random.random() < 0.1:  # 10% chance of update
                if train['operational']['status'] == 'Available' and random.random() < 0.3:
                    train['operational']['status'] = 'Maintenance'
                    updated_count += 1
                # Simulate job card updates
                if random.random() < 0.2:
                    change = random.randint(-1, 2)
                    train['job_cards']['open'] = max(0, train['job_cards']['open'] + change)
                    updated_count += 1
                # Simulate fitness certificate updates
                if random.random() < 0.15:
                    department = random.choice(['rolling_stock', 'signalling', 'telecom'])
                    train['fitness'][department] = random.random() > 0.1
                    updated_count += 1
                    
        return trainsets, updated_count
    
    def generate_synthetic_trainset(self, trainset_id, historical_data=None):
        """
        Generate a synthetic trainset with realistic patterns based on historical data
        """
        now = datetime.now()
        
        # Base patterns from historical data if available
        if historical_data and not historical_data.empty:
            # Extract patterns from historical data
            pass  # Would implement ML-based pattern extraction in real system
        
        # Generate realistic expiry dates (clustered around maintenance cycles)
        maintenance_cycle = random.choice([30, 60, 90])  # Days between maintenance
        days_since_maintenance = random.randint(0, maintenance_cycle)
        
        fitness_expiry = now + timedelta(days=random.randint(-2, maintenance_cycle - days_since_maintenance))
        
        # Correlated features - higher mileage trains tend to have more issues
        total_km = random.randint(20000, 100000)
        wear_factor = total_km / 100000  # 0-1 scale
        
        # Generate correlated probabilities
        maintenance_prob = min(0.7, 0.1 + wear_factor * 0.6)
        cleaning_prob = min(0.8, 0.2 + wear_factor * 0.6)
        
        trainset = {
            'id': trainset_id,
            'depot': random.choice(self.depots),
            'fitness': {
                'rolling_stock': random.random() > (0.05 + wear_factor * 0.1),
                'signalling': random.random() > (0.03 + wear_factor * 0.08),
                'telecom': random.random() > (0.04 + wear_factor * 0.09),
                'expires_at': fitness_expiry,
                'days_until_expiry': max(0, (fitness_expiry - now).days),
                'overall_valid': True  # Will be set after generation
            },
            'job_cards': {
                'open': random.randint(0, min(4, int(wear_factor * 6))),
                'closed_today': random.randint(0, 2),
                'priority': random.choice(['Low', 'Medium', 'High', 'Critical']),
                'maintenance_type': random.choice(self.maintenance_types),
                'estimated_hours': random.randint(1, 8)
            },
            'branding': {
                'advertiser': random.choice(self.brands),
                'contract_start': now - timedelta(days=random.randint(0, 60)),
                'hours_required_today': random.randint(4, 15) if random.random() > 0.6 else 0,
                'contract_value': random.randint(20000, 120000) if random.random() > 0.6 else 0,
                'exposure_deficit': random.randint(1, 20) if random.random() > 0.7 else 0
            },
            'mileage': {
                'total_km': total_km,
                'since_maintenance': random.randint(1000, 9000),
                'daily_target': random.randint(150, 450),
                'balance_deviation': int((random.random() - 0.5) * 5000),
                'component_wear': {
                    'brake_pads': min(100, int(30 + wear_factor * 70)),
                    'bogies': min(100, int(25 + wear_factor * 75)),
                    'hvac': min(100, int(20 + wear_factor * 80))
                }
            },
            'cleaning': {
                'interior_status': 'Clean' if random.random() > (0.2 + wear_factor * 0.2) else 'Requires Cleaning',
                'exterior_status': 'Clean' if random.random() > (0.3 + wear_factor * 0.2) else 'Requires Cleaning',
                'last_cleaned': now - timedelta(days=random.randint(0, 7)),
                'deep_clean_due': random.random() > (0.8 - wear_factor * 0.3),
                'cleaning_slot_assigned': f"Bay {random.randint(1,5)}" if random.random() > 0.5 else None,
                'estimated_duration': random.randint(2, 5)
            },
            'stabling': {
                'current_bay': f"Bay-{random.randint(1,15)}",
                'optimal_bay': f"Bay-{random.randint(1,15)}",
                'shunting_moves_required': random.randint(0,3),
                'turn_out_time_minutes': random.randint(10,40),
                'energy_cost_shunting': random.randint(100,600)
            },
            'operational': {
                'status': 'Available' if random.random() > (0.15 + wear_factor * 0.2) else ('IBL' if random.random() > 0.7 else 'Maintenance'),
                'last_service': now - timedelta(days=days_since_maintenance),
                'next_scheduled_maintenance': now + timedelta(days=maintenance_cycle - days_since_maintenance),
                'reliability_score': max(70, 100 - int(wear_factor * 30)),
                'punctuality_impact': random.random() * 5
            },
            'manual_override': None,
            'override_reason': ''
        }
        
        # Set overall fitness validity
        trainset['fitness']['overall_valid'] = (
            trainset['fitness']['rolling_stock'] and 
            trainset['fitness']['signalling'] and 
            trainset['fitness']['telecom']
        )
        
        return trainset
    def generate_realistic_dataset(self, n=25, historical_patterns=None):
        """
        Generate a more realistic dataset with correlated patterns
        """
        trainsets = []
        simulator = KMRLDataSimulator(n)
        
        for i in range(1, n + 1):
            trainset_id = f"KMRL-{str(i).zfill(3)}"
            trainset = simulator.generate_synthetic_trainset(trainset_id, historical_patterns)
            
            # AI scoring
            ai_score, reasons = calculate_ai_score(trainset)
            trainset['ai_score'] = ai_score
            trainset['score_reasons'] = reasons

            # Recommendation assignment
            if ai_score < 30 or trainset['operational']['status'] == 'IBL' or trainset['job_cards']['open'] > 2:
                trainset['recommendation'] = 'IBL'
            elif ai_score > 70 and trainset['fitness']['overall_valid']:
                trainset['recommendation'] = 'Service'
            else:
                trainset['recommendation'] = 'Standby'

            trainsets.append(trainset)

        # Sort descending by ai_score
        trainsets.sort(key=lambda x: x['ai_score'], reverse=True)
        return trainsets

# -----------------------
# Advanced AI Optimization Engine
# -----------------------
class MultiObjectiveOptimizer:
    def __init__(self):
        self.weights = {
            'punctuality': 0.25,
            'cost_efficiency': 0.20,
            'branding_compliance': 0.15,
            'maintenance_risk': 0.20,
            'energy_efficiency': 0.10,
            'operational_flexibility': 0.10
        }
        
    def calculate_objective_scores(self, trainset):
        """Calculate individual objective scores for a trainset"""
        scores = {}
        
        # Punctuality score (based on fitness and reliability)
        scores['punctuality'] = (
            (1.0 if trainset['fitness']['overall_valid'] else 0.3) *
            (trainset['operational']['reliability_score'] / 100)
        )
        
        # Cost efficiency (lower maintenance needs = better)
        maintenance_penalty = min(1.0, trainset['job_cards']['open'] * 0.2 + 
                                 (0.5 if trainset['cleaning']['deep_clean_due'] else 0))
        scores['cost_efficiency'] = 1.0 - maintenance_penalty
        
        # Branding compliance
        branding_score = 0.5  # Base score
        if trainset['branding']['hours_required_today'] > 0:
            branding_score += 0.3
        if trainset['branding']['exposure_deficit'] > 10:
            branding_score += 0.2
        scores['branding_compliance'] = min(1.0, branding_score)
        
        # Maintenance risk (based on component wear and mileage)
        wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3 / 100
        mileage_risk = min(1.0, trainset['mileage']['since_maintenance'] / 10000)
        scores['maintenance_risk'] = 1.0 - max(wear_avg, mileage_risk)
        
        # Energy efficiency (less shunting = better)
        energy_score = 1.0 - (trainset['stabling']['shunting_moves_required'] * 0.2)
        scores['energy_efficiency'] = energy_score
        
        # Operational flexibility (status and availability)
        if trainset['operational']['status'] == 'Available':
            flexibility = 0.8
        elif trainset['operational']['status'] == 'Standby':
            flexibility = 0.5
        else:
            flexibility = 0.2
        scores['operational_flexibility'] = flexibility
        
        return scores
    
    def calculate_overall_score(self, trainset):
        """Calculate weighted overall score for optimization"""
        objective_scores = self.calculate_objective_scores(trainset)
        weighted_score = sum(
            objective_scores[obj] * self.weights[obj] 
            for obj in self.weights
        )
        return weighted_score, objective_scores
    
    def optimize_fleet_assignment(self, trainsets, constraints):
        """
        Optimize fleet assignment using a weighted multi-objective approach
        """
        optimized_trainsets = trainsets.copy()
        
        # Calculate scores for all trainsets
        for trainset in optimized_trainsets:
            overall_score, objective_scores = self.calculate_overall_score(trainset)
            trainset['optimization_score'] = overall_score
            trainset['objective_scores'] = objective_scores
        
        # Sort by optimization score
        optimized_trainsets.sort(key=lambda x: x['optimization_score'], reverse=True)
        
        # Apply constraints
        service_count = sum(1 for t in optimized_trainsets if t['recommendation'] == 'Service')
        target_service = constraints.get('service_target', min(15, len(optimized_trainsets)))
        max_ibl = constraints.get('max_ibl', 5)
        
        # Reset all recommendations first
        for trainset in optimized_trainsets:
            trainset['recommendation'] = 'Standby'  # Default
        
        # Assign Service status to top trainsets
        service_candidates = [t for t in optimized_trainsets 
                             if t['fitness']['overall_valid'] and 
                             t['operational']['status'] != 'IBL']
        
        for i in range(min(target_service, len(service_candidates))):
            service_candidates[i]['recommendation'] = 'Service'
            service_candidates[i]['optimization_note'] = 'Optimized for service'
        
        # Assign IBL status based on constraints and needs
        ibl_candidates = [t for t in optimized_trainsets 
                         if not t['fitness']['overall_valid'] or 
                         t['operational']['status'] == 'IBL' or
                         t['job_cards']['open'] > 2]
        
        ibl_candidates.sort(key=lambda x: x['optimization_score'])  # Worst first
        
        for i in range(min(max_ibl, len(ibl_candidates))):
            ibl_candidates[i]['recommendation'] = 'IBL'
            ibl_candidates[i]['optimization_note'] = 'Required maintenance'
        
        # Check for conflicts
        conflicts = []
        for t in optimized_trainsets:
            if t['recommendation'] == 'Service' and not t['fitness']['overall_valid']:
                conflicts.append(f"{t['id']} recommended for service but has invalid fitness")
            if t['recommendation'] == 'Service' and t['operational']['status'] == 'IBL':
                conflicts.append(f"{t['id']} recommended for service but is in IBL")
        
        # Calculate overall metrics
        service_ready = sum(1 for t in optimized_trainsets if t['recommendation'] == 'Service')
        standby = sum(1 for t in optimized_trainsets if t['recommendation'] == 'Standby')
        ibl = sum(1 for t in optimized_trainsets if t['recommendation'] == 'IBL')
        
        return optimized_trainsets, conflicts, service_ready, standby, ibl

# -----------------------
# Predictive Maintenance with ML
# -----------------------
class PredictiveMaintenanceModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_training_data(self, historical_data):
        """Prepare training data from historical records"""
        features = []
        labels = []
        
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
            
            features.append(feature_vector)
            labels.append(label)
            
        return np.array(features), np.array(labels)
    
    def train_model(self, historical_data):
        """Train the predictive maintenance model"""
        try:
            features, labels = self.prepare_training_data(historical_data)
            
            if len(features) < 10:
                # Not enough data for proper training
                self.is_trained = False
                return False
                
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train Random Forest model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(features_scaled, labels)
            self.is_trained = True
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
                
                predictions.append({
                    'trainset_id': trainset['id'],
                    'risk_score': round(risk_score, 1),
                    'days_until_maintenance': round(max(0, days_until_maintenance), 1),
                    'recommended_action': action,
                    'priority': priority,
                    'confidence': 'High' if self.is_trained else 'Low'
                })
                
            except Exception as e:
                # Fallback if prediction fails
                predictions.append(self._fallback_prediction(trainset))
                
        return pd.DataFrame(predictions)
    
    def _fallback_predictions(self, trainsets):
        """Fallback predictions when model is not trained"""
        return pd.DataFrame([self._fallback_prediction(t) for t in trainsets])
    
    def _fallback_prediction(self, trainset):
        """Simple heuristic-based fallback prediction"""
        wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
        mileage_ratio = trainset['mileage']['since_maintenance'] / 10000
        risk_score = min(100, max(0, wear_avg * 0.7 + mileage_ratio * 30))
        
        days_until_maintenance = max(0, 30 - (risk_score / 100 * 30))
        
        if risk_score > 70:
            action = 'Schedule Soon'
            priority = 'High'
        elif risk_score > 40:
            action = 'Monitor'
            priority = 'Medium'
        else:
            action = 'OK'
            priority = 'Low'
            
        return {
            'trainset_id': trainset['id'],
            'risk_score': round(risk_score, 1),
            'days_until_maintenance': round(days_until_maintenance, 1),
            'recommended_action': action,
            'priority': priority,
            'confidence': 'Low (Heuristic)'
        }
# -----------------------
# Real-time Data Integration
# -----------------------
class RealTimeDataIntegrator:
    def __init__(self):
        self.data_sources = {
            'maximo': {'connected': False, 'last_update': None},
            'iot_sensors': {'connected': False, 'last_update': None},
            'fitness_certs': {'connected': False, 'last_update': None}
        }
        
    def connect_to_maximo(self, trainsets):
        """Simulate connecting to IBM Maximo and updating job card status"""
        updated_count = 0
        for trainset in trainsets:
            if random.random() < 0.3:  # 30% chance of update from Maximo
                # Simulate job card updates
                change = random.randint(-1, 2)
                new_count = max(0, trainset['job_cards']['open'] + change)
                if new_count != trainset['job_cards']['open']:
                    trainset['job_cards']['open'] = new_count
                    updated_count += 1
                    
                # Simulate priority changes
                if random.random() < 0.2:
                    trainset['job_cards']['priority'] = random.choice(['Low', 'Medium', 'High', 'Critical'])
                    updated_count += 1
                    
        self.data_sources['maximo']['last_update'] = datetime.now()
        self.data_sources['maximo']['connected'] = True
        return trainsets, updated_count
    
    def connect_to_iot_sensors(self, trainsets):
        """Simulate IoT sensor data updates"""
        updated_count = 0
        for trainset in trainsets:
            if random.random() < 0.4:  # 40% chance of sensor update
                # Update component wear based on recent operation
                wear_increase = random.uniform(0.1, 2.0)
                for component in trainset['mileage']['component_wear']:
                    trainset['mileage']['component_wear'][component] = min(
                        100, trainset['mileage']['component_wear'][component] + wear_increase
                    )
                
                # Update mileage
                daily_km = random.randint(50, 300)
                trainset['mileage']['total_km'] += daily_km
                trainset['mileage']['since_maintenance'] += daily_km
                updated_count += 1
                
        self.data_sources['iot_sensors']['last_update'] = datetime.now()
        self.data_sources['iot_sensors']['connected'] = True
        return trainsets, updated_count

    def connect_to_fitness_db(self, trainsets):
        """Simulate fitness certificate database updates"""
        updated_count = 0
        for trainset in trainsets:
            if random.random() < 0.25:  # 25% chance of fitness update
                # Simulate certificate expiry/extension
                if random.random() < 0.1:  # 10% chance of expiry
                    department = random.choice(['rolling_stock', 'signalling', 'telecom'])
                    trainset['fitness'][department] = False
                    updated_count += 1
                
                # Simplicate certificate renewal
                if random.random() < 0.15 and not all([trainset['fitness']['rolling_stock'], 
                                                     trainset['fitness']['signalling'], 
                                                     trainset['fitness']['telecom']]):
                    # Renew expired certificates
                    for dept in ['rolling_stock', 'signalling', 'telecom']:
                        if not trainset['fitness'][dept]:
                            trainset['fitness'][dept] = True
                            updated_count += 1
                
                # Update expiry dates
                if random.random() < 0.2:
                    days_change = random.randint(-2, 7)
                    new_expiry = trainset['fitness']['expires_at'] + timedelta(days=days_change)
                    trainset['fitness']['expires_at'] = new_expiry
                    trainset['fitness']['days_until_expiry'] = max(0, (new_expiry - datetime.now()).days)
                    updated_count += 1
                    
        self.data_sources['fitness_certs']['last_update'] = datetime.now()
        self.data_sources['fitness_certs']['connected'] = True
        return trainsets, updated_count

    def refresh_all_data(self, trainsets):
        """Refresh data from all sources"""
        total_updates = 0
        
        trainsets, updates = self.connect_to_maximo(trainsets)
        total_updates += updates
        
        trainsets, updates = self.connect_to_iot_sensors(trainsets)
        total_updates += updates
        
        trainsets, updates = self.connect_to_fitness_db(trainsets)
        total_updates += updates
        
        # Recalculate scores after updates
        for trainset in trainsets:
            score, reasons = calculate_ai_score(trainset)
            trainset['ai_score'] = score
            trainset['score_reasons'] = reasons
            
        return trainsets, total_updates
# -----------------------
# Alert & Notification System
# -----------------------
class AlertManager:
    def __init__(self):
        self.alerts = []
        self.alert_rules = {
            'fitness_expiry': {'threshold': 2, 'priority': 'High'},
            'high_risk_maintenance': {'threshold': 75, 'priority': 'Critical'},
            'branding_deficit': {'threshold': 15, 'priority': 'Medium'},
            'service_readiness': {'threshold': 12, 'priority': 'High'},
            'conflict_detection': {'priority': 'High'}
        }
        
    def check_alerts(self, trainsets, optimization_results=None):
        """Check all alert conditions"""
        self.alerts = []
        
        self._check_fitness_alerts(trainsets)
        self._check_maintenance_alerts(trainsets)
        self._check_branding_alerts(trainsets)
        self._check_service_alerts(trainsets, optimization_results)
        self._check_conflict_alerts(optimization_results)
        
        return self.alerts
    
    def _check_fitness_alerts(self, trainsets):
        """Check fitness certificate alerts"""
        for trainset in trainsets:
            if trainset['fitness']['days_until_expiry'] <= self.alert_rules['fitness_expiry']['threshold']:
                self.alerts.append({
                    'type': 'fitness_expiry',
                    'priority': self.alert_rules['fitness_expiry']['priority'],
                    'message': f"{trainset['id']}: Fitness expires in {trainset['fitness']['days_until_expiry']} days",
                    'trainset_id': trainset['id'],
                    'timestamp': datetime.now()
                })
    def _check_maintenance_alerts(self, trainsets):
        """Check maintenance risk alerts"""
        for trainset in trainsets:
            wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
            if wear_avg >= self.alert_rules['high_risk_maintenance']['threshold']:
                self.alerts.append({
                    'type': 'high_risk_maintenance',
                    'priority': self.alert_rules['high_risk_maintenance']['priority'],
                    'message': f"{trainset['id']}: High component wear ({wear_avg:.1f}%)",
                    'trainset_id': trainset['id'],
                    'timestamp': datetime.now()
                })
    
    def _check_branding_alerts(self, trainsets):
        """Check branding commitment alerts"""
        for trainset in trainsets:
            if trainset['branding']['exposure_deficit'] >= self.alert_rules['branding_deficit']['threshold']:
                self.alerts.append({
                    'type': 'branding_deficit',
                    'priority': self.alert_rules['branding_deficit']['priority'],
                    'message': f"{trainset['id']}: High exposure deficit ({trainset['branding']['exposure_deficit']} hours)",
                    'trainset_id': trainset['id'],
                    'timestamp': datetime.now()
                })
    
    def _check_service_alerts(self, trainsets, optimization_results):
        """Check service readiness alerts"""
        if optimization_results and optimization_results.get('service_ready', 0) < self.alert_rules['service_readiness']['threshold']:
            self.alerts.append({
                'type': 'service_readiness',
                'priority': self.alert_rules['service_readiness']['priority'],
                'message': f"Low service readiness: Only {optimization_results['service_ready']} trains available",
                'trainset_id': None,
                'timestamp': datetime.now()
            })
    
    def _check_conflict_alerts(self, optimization_results):
        """Check optimization conflict alerts"""
        if optimization_results and optimization_results.get('conflicts'):
            self.alerts.append({
                'type': 'conflict_detection',
                'priority': self.alert_rules['conflict_detection']['priority'],
                'message': f"Found {len(optimization_results['conflicts'])} optimization conflicts",
                'trainset_id': None,
                'timestamp': datetime.now()
            })
    
    def get_priority_alerts(self, priority_level='Critical'):
        """Get alerts filtered by priority"""
        return [alert for alert in self.alerts if alert['priority'] == priority_level]

# -----------------------
# Report Generation System
# -----------------------
class ReportGenerator:
    def __init__(self):
        self.report_templates = {
            'daily_operations': self._generate_daily_operations_report,
            'maintenance_plan': self._generate_maintenance_report,
            'branding_compliance': self._generate_branding_report,
            'optimization_summary': self._generate_optimization_report
        }
    
    def generate_report(self, report_type, trainsets, optimization_results=None, alerts=None):
        """Generate a specific type of report"""
        if report_type in self.report_templates:
            return self.report_templates[report_type](trainsets, optimization_results, alerts)
        return None
    
    def _generate_daily_operations_report(self, trainsets, optimization_results, alerts):
        """Generate daily operations report"""
        service_ready = sum(1 for t in trainsets if t.get('manual_override') or t['recommendation'] == 'Service')
        standby = sum(1 for t in trainsets if t.get('manual_override') or t['recommendation'] == 'Standby')
        ibl = sum(1 for t in trainsets if t.get('manual_override') or t['recommendation'] == 'IBL')
        
        report = {
            'title': 'Daily Operations Report',
            'timestamp': datetime.now(),
            'summary': {
                'total_trainsets': len(trainsets),
                'service_ready': service_ready,
                'standby': standby,
                'ibl_maintenance': ibl,
                'availability_rate': round(service_ready / len(trainsets) * 100, 1) if trainsets else 0
            },
            'fitness_status': {
                'all_valid': sum(1 for t in trainsets if t['fitness']['overall_valid']),
                'expiring_soon': sum(1 for t in trainsets if t['fitness']['days_until_expiry'] <= 2)
            },
            'maintenance_status': {
                'open_job_cards': sum(t['job_cards']['open'] for t in trainsets),
                'critical_priority': sum(1 for t in trainsets if t['job_cards']['priority'] == 'Critical')
            }
        }
        
        return report
    def _generate_maintenance_report(self, trainsets, optimization_results, alerts):
        """Generate maintenance planning report"""
        high_risk_trains = []
        for t in trainsets:
            wear_avg = sum(t['mileage']['component_wear'].values()) / 3
            if wear_avg > 70 or t['job_cards']['open'] > 2:
                high_risk_trains.append({
                    'id': t['id'],
                    'wear_score': wear_avg,
                    'open_jobs': t['job_cards']['open'],
                    'priority': t['job_cards']['priority']
                })
        
        report = {
            'title': 'Maintenance Planning Report',
            'timestamp': datetime.now(),
            'high_risk_trains': sorted(high_risk_trains, key=lambda x: x['wear_score'], reverse=True),
            'total_open_jobs': sum(t['job_cards']['open'] for t in trainsets),
            'preventive_maintenance_needed': sum(1 for t in trainsets if t['mileage']['since_maintenance'] > 8000),
            'critical_issues': sum(1 for t in trainsets if t['job_cards']['priority'] == 'Critical')
        }
        
        return report
    
    def _generate_branding_report(self, trainsets, optimization_results, alerts):
        """Generate branding compliance report"""
        branding_stats = {}
        for t in trainsets:
            advertiser = t['branding']['advertiser'] or 'Unbranded'
            if advertiser not in branding_stats:
                branding_stats[advertiser] = {
                    'total_hours_required': 0,
                    'total_deficit': 0,
                    'train_count': 0,
                    'total_value': 0
                }
            branding_stats[advertiser]['total_hours_required'] += t['branding']['hours_required_today']
            branding_stats[advertiser]['total_deficit'] += t['branding']['exposure_deficit']
            branding_stats[advertiser]['train_count'] += 1
            branding_stats[advertiser]['total_value'] += t['branding']['contract_value']
        
        report = {
            'title': 'Branding Compliance Report',
            'timestamp': datetime.now(),
            'advertiser_stats': branding_stats,
            'total_exposure_deficit': sum(t['branding']['exposure_deficit'] for t in trainsets),
            'total_contract_value': sum(t['branding']['contract_value'] for t in trainsets),
            'trains_requiring_exposure': sum(1 for t in trainsets if t['branding']['hours_required_today'] > 0)
        }
        
        return report
    
    def _generate_optimization_report(self, trainsets, optimization_results, alerts):
        """Generate optimization performance report"""
        if not optimization_results:
            return None
            
        report = {
            'title': 'Optimization Performance Report',
            'timestamp': datetime.now(),
            'optimization_results': optimization_results,
            'constraint_compliance': {
                'service_target_met': optimization_results.get('service_ready', 0) >= optimization_results.get('target_service', 0),
                'ibl_within_limit': optimization_results.get('ibl_maintenance', 0) <= optimization_results.get('max_ibl', 5)
            },
            'conflict_resolution': len(optimization_results.get('conflicts', [])),
            'predicted_impact': {
                'punctuality_improvement': max(0, (optimization_results.get('punctuality_score', 0) - 98.5)),
                'cost_savings': optimization_results.get('cost_optimization', 0),
                'energy_savings': optimization_results.get('energy_savings', 0)
            }
        }
        
        return report
    
    def export_report_to_csv(self, report, filename_prefix):
        """Export report data to CSV format"""
        if not report:
            return None
            
        df_data = []
        if 'advertiser_stats' in report:
            for advertiser, stats in report['advertiser_stats'].items():
                df_data.append({
                    'advertiser': advertiser,
                    'trains_count': stats['train_count'],
                    'hours_required': stats['total_hours_required'],
                    'exposure_deficit': stats['total_deficit'],
                    'contract_value': stats['total_value']
                })
        elif 'high_risk_trains' in report:
            for train in report['high_risk_trains']:
                df_data.append(train)
                
        if df_data:
            df = pd.DataFrame(df_data)
            return df.to_csv(index=False)
        return None

# -----------------------
# System Integration Manager
# -----------------------
class SystemIntegrationManager:
    def __init__(self):
        self.data_simulator = KMRLDataSimulator()
        self.optimizer = MultiObjectiveOptimizer()
        self.ml_model = PredictiveMaintenanceModel()
        self.data_integrator = RealTimeDataIntegrator()
        self.alert_manager = AlertManager()
        self.report_generator = ReportGenerator()
        self.last_optimization_time = None
        self.optimization_history = []
        
    def initialize_system(self, n_trainsets=25):
        """Initialize the complete system with data"""
        trainsets = self.data_simulator.generate_realistic_dataset(n_trainsets)
        
        # Train ML model with initial data
        self.ml_model.train_model(trainsets)
        
        return trainsets
    
    def run_complete_optimization(self, trainsets, constraints):
        """Run complete optimization pipeline"""
        start_time = time.time()
        
        # Refresh real-time data
        trainsets, update_count = self.data_integrator.refresh_all_data(trainsets)
        
        # Run optimization
        optimized_trainsets, conflicts, service_ready, standby, ibl = self.optimizer.optimize_fleet_assignment(
            trainsets, constraints
        )
        
        # Generate maintenance predictions
        maintenance_predictions = self.ml_model.predict_maintenance(optimized_trainsets)
        
        # Calculate performance metrics
        performance_metrics = self._calculate_performance_metrics(optimized_trainsets, constraints)
        performance_metrics.update({
            'service_ready': service_ready,
            'standby': standby,
            'ibl_maintenance': ibl,
            'conflicts': conflicts,
            'data_updates': update_count,
            'processing_time': round(time.time() - start_time, 2)
        })
        
        # Check for alerts
        alerts = self.alert_manager.check_alerts(optimized_trainsets, performance_metrics)
        
        # Store in history
        optimization_record = {
            'timestamp': datetime.now(),
            'metrics': performance_metrics,
            'constraints': constraints,
            'alert_count': len(alerts)
        }
        self.optimization_history.append(optimization_record)
        self.last_optimization_time = datetime.now()
        
        return optimized_trainsets, performance_metrics, alerts, maintenance_predictions
    
    def _calculate_performance_metrics(self, trainsets, constraints):
        """Calculate comprehensive performance metrics"""
        metrics = {}
        
        # Fitness metrics
        metrics['fitness_compliance'] = round(sum(1 for t in trainsets if t['fitness']['overall_valid']) / len(trainsets) * 100, 1)
        
        # Maintenance metrics
        metrics['maintenance_backlog'] = sum(t['job_cards']['open'] for t in trainsets)
        
        # Branding metrics
        metrics['branding_compliance'] = round(sum(1 for t in trainsets if t['branding']['exposure_deficit'] == 0) / len(trainsets) * 100, 1)
        
        # Operational metrics
        metrics['avg_reliability'] = round(sum(t['operational']['reliability_score'] for t in trainsets) / len(trainsets), 1)
        
        # Economic metrics (simulated)
        metrics['estimated_savings'] = random.randint(5000, 20000)
        metrics['energy_efficiency'] = random.randint(85, 98)
        
        return metrics
    def generate_comprehensive_report(self, trainsets, metrics, alerts, report_type='daily_operations'):
        """Generate comprehensive report for management"""
        report = self.report_generator.generate_report(
            report_type, trainsets, metrics, alerts
        )
        
        # Add system performance data
        if report:
            report['system_performance'] = {
                'last_optimization': self.last_optimization_time,
                'total_optimizations': len(self.optimization_history),
                'ml_model_status': 'Trained' if self.ml_model.is_trained else 'Not Trained',
                'data_sources_connected': {
                    source: status['connected'] 
                    for source, status in self.data_integrator.data_sources.items()
                }
            }
        
        return report
    
    def get_optimization_trends(self):
        """Get historical optimization trends for analytics"""
        if not self.optimization_history:
            return None
            
        trends = {
            'timestamps': [record['timestamp'] for record in self.optimization_history],
            'service_readiness': [record['metrics'].get('service_ready', 0) for record in self.optimization_history],
            'fitness_compliance': [record['metrics'].get('fitness_compliance', 0) for record in self.optimization_history],
            'alert_counts': [record['alert_count'] for record in self.optimization_history],
            'processing_times': [record['metrics'].get('processing_time', 0) for record in self.optimization_history]
        }
        
        return trends
    
    def simulate_operational_day(self, trainsets, constraints):
        """Simulate a full operational day with multiple optimizations"""
        results = []
        
        # Morning optimization (05:00)
        morning_result = self.run_complete_optimization(trainsets, constraints)
        results.append(('morning', morning_result))
        
        # Mid-day check (12:00) - simulate some changes
        updated_trainsets, _ = self.data_integrator.connect_to_iot_sensors(trainsets)
        mid_day_result = self.run_complete_optimization(updated_trainsets, constraints)
        results.append(('mid_day', mid_day_result))
        
        # Evening optimization (18:00) - more changes
        updated_trainsets, _ = self.data_integrator.connect_to_maximo(trainsets)
        evening_result = self.run_complete_optimization(updated_trainsets, constraints)
        results.append(('evening', evening_result))
        
        return results
    
    def reset_system(self):
        """Reset the system to initial state"""
        self.ml_model = PredictiveMaintenanceModel()
        self.optimization_history = []
        self.last_optimization_time = None
        self.data_integrator = RealTimeDataIntegrator()
def create_streamlit_frontend():
    """
    Create a comprehensive Streamlit frontend for the KMRL AI Induction Planning Platform
    """
    st.set_page_config(
        page_title="KMRL AI Induction Planning Platform",
        page_icon="🚇",
        layout="wide",
        initial_sidebar_state="expanded",
        theme={
            "primaryColor": "#1f77b4",
            "backgroundColor": "#ffffff",
            "secondaryBackgroundColor": "#f0f2f6",
            "textColor": "#31333F",
        }
    )
    # Custom CSS - Light theme version
    st.markdown("""
    <style>
    .metric-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-card h3 {
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #4A5568;
    }
    .metric-card h1 {
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #2D3748;
    }
    .metric-card p {
        font-size: 0.8rem;
        font-weight: 500;
        color: #718096;
    }
    .alert-high { border-left-color: #ff4b4b; }
    .alert-medium { border-left-color: #ffa500; }
    .alert-low { border-left-color: #00cc88; }
    .trainset-card {
        border: 1px solid #E2E8F0;
        border-radius: 0.5rem;
        padding: 0.5rem;
        margin: 0.25rem 0;
        background: #ffffff;
    }
    .status-service { background-color: #f0f9f0; border-left: 4px solid #28a745; }
    .status-standby { background-color: #fffaf0; border-left: 4px solid #ffc107; }
    .status-ibl { background-color: #fef5f5; border-left: 4px solid #dc3545; }
    </style>
    """, unsafe_allow_html=True)
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
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-card h3 {
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-card h1 {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-card p {
        font-size: 0.8rem;
        font-weight: 500;
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


def create_dashboard_tab():
    """Create the main dashboard tab"""
    st.header("📊 Real-time Fleet Dashboard")
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    trainsets = st.session_state.trainsets
    
    # Custom CSS for cards with gradient colors and hover effects
    st.markdown("""
    <style>
    .dashboard-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: all 0.3s ease;
        color: white;
        border: none;
    }
    .dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.3);
    }
    .dashboard-card h3 {
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: white;
        font-weight: 600;
    }
    .dashboard-card h1 {
        font-weight: bold;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
        color: white;
    }
    .dashboard-card p {
        font-size: 0.8rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.9);
    }
    .service-card {
        background: linear-gradient(135deg, #28A745, #22C55E);
    }
    .standby-card {
        background: linear-gradient(135deg, #FFC107, #F59E0B);
    }
    .ibl-card {
        background: linear-gradient(135deg, #DC3545, #EF4444);
    }
    .fitness-card {
        background: linear-gradient(135deg, #A855F7, #8B5CF6);
    }
    .score-card {
        background: linear-gradient(135deg, #3B8276, #10B981);
    }
    </style>
    """, unsafe_allow_html=True)
    
    with col1:
        service_count = sum(1 for t in trainsets if t['recommendation'] == 'Service')
        st.markdown(f"""
        <div class="dashboard-card service-card">
            <br>
            <h3>SERVICE READY</h3>
            <h1>{service_count}</h1>
            <p>+{service_count/len(trainsets)*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        standby_count = sum(1 for t in trainsets if t['recommendation'] == 'Standby')
        st.markdown(f"""
        <div class="dashboard-card standby-card">
            <br>
            <h3>STANDBY</h3>
            <h1>{standby_count}</h1>
            <p>+1.2%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        ibl_count = sum(1 for t in trainsets if t['recommendation'] == 'IBL')
        st.markdown(f"""
        <div class="dashboard-card ibl-card">
            <br>
            <h3>IBL/MAINTENANCE</h3>
            <h1>{ibl_count}</h1>
            <p>+1.7%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        fitness_valid = sum(1 for t in trainsets if t['fitness']['overall_valid'])
        st.markdown(f"""
        <div class="dashboard-card fitness-card">
            <br>
            <h3>FITNESS VALID</h3>
            <h1>{fitness_valid}</h1>
            <p>+{fitness_valid/len(trainsets)*100:.1f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        avg_score = sum(t['ai_score'] for t in trainsets) / len(trainsets)
        st.markdown(f"""
        <div class="dashboard-card score-card">
            <br>
            <h3>AVG AI SCORE</h3>
            <h1>{avg_score:.1f}</h1>
            <p>&nbsp;</p>
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


def create_fleet_status_tab():
    """Create the fleet status tab"""
    st.header("🚆 Fleet Status Overview")
    
    trainsets = st.session_state.trainsets
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        depot_filter = st.selectbox("Filter by Depot", ["All"] + list(set(t['depot'] for t in trainsets)))
    with col2:
        status_filter = st.selectbox("Filter by Status", ["All", "Service", "Standby", "IBL"])
    with col3:
        sort_by = st.selectbox("Sort by", ["AI Score", "ID", "Fitness Expiry"])
    
    # Apply filters
    filtered_trainsets = trainsets.copy()
    if depot_filter != "All":
        filtered_trainsets = [t for t in filtered_trainsets if t['depot'] == depot_filter]
    if status_filter != "All":
        filtered_trainsets = [t for t in filtered_trainsets if t['recommendation'] == status_filter]
    
    # Sort
    if sort_by == "AI Score":
        filtered_trainsets.sort(key=lambda x: x['ai_score'], reverse=True)
    elif sort_by == "Fitness Expiry":
        filtered_trainsets.sort(key=lambda x: x['fitness']['days_until_expiry'])
    
    # Display trainsets in a grid
    cols_per_row = 3
    for i in range(0, len(filtered_trainsets), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, train in enumerate(filtered_trainsets[i:i+cols_per_row]):
            with cols[j]:
                create_trainset_card(train)


def create_trainset_card(train):
    """Create a detailed trainset card"""
    status_colors = {
        'Service': "#31ee5d",
        'Standby': "#e4c560",
        'IBL': "#f74957"
    }
    
    bg_color = status_colors.get(train['recommendation'], '#f8f9fa')
    
    # Override controls
    with st.expander(f"🚆 {train['id']} (Score: {train['ai_score']})"):
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <strong>Current Recommendation: {train['recommendation']}</strong>
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
            wear_avg = sum(train['mileage']['component_wear'].values()) / 3
            st.write(f"**Avg Wear:** {wear_avg:.1f}%")
            st.write(f"**Days to Fitness Expiry:** {train['fitness']['days_until_expiry']}")
        
        # Manual override
        st.subheader("Manual Override")
        override_status = st.selectbox(
            "Override Recommendation", 
            ["None", "Service", "Standby", "IBL"], 
            key=f"override_{train['id']}",
            index=0 if not train.get('manual_override') else ["None", "Service", "Standby", "IBL"].index(train.get('manual_override'))
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
                train['manual_override'] = None
                train['override_reason'] = ''
                st.info("Override removed")


def create_maintenance_tab():
    """Create the maintenance planning tab"""
    st.header("🔧 Predictive Maintenance Dashboard")
    
    if 'maintenance_predictions' in st.session_state:
        predictions_df = st.session_state.maintenance_predictions
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            critical_count = len(predictions_df[predictions_df['priority'] == 'High'])
            st.metric("Critical Maintenance", critical_count)
        
        with col2:
            avg_risk = predictions_df['risk_score'].mean()
            st.metric("Avg Risk Score", f"{avg_risk:.1f}")
        
        with col3:
            immediate_action = len(predictions_df[predictions_df['recommended_action'] == 'Schedule Immediately'])
            st.metric("Immediate Action", immediate_action)
        
        with col4:
            avg_days = predictions_df['days_until_maintenance'].mean()
            st.metric("Avg Days to Maintenance", f"{avg_days:.1f}")
        
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
            'Status': train['recommendation']
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
        critical_alerts = [a for a in alerts if a['priority'] == 'Critical']
        high_alerts = [a for a in alerts if a['priority'] == 'High']
        medium_alerts = [a for a in alerts if a['priority'] == 'Medium']
        
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
                        <strong>{alert['type'].replace('_', ' ').title()}</strong><br>
                        {alert['message']}<br>
                        <small>Time: {alert['timestamp'].strftime('%H:%M:%S')}</small>
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
                    'AI_Score': t['ai_score'],
                    'Recommendation': t['recommendation'],
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


# Add this at the end of your existing code to run the Streamlit app
if __name__ == "__main__":
    create_streamlit_frontend()