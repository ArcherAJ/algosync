from common_imports import *
from typing import List, Dict, Any, Tuple

class AITimetableOptimizer:
    """
    Advanced AI-powered timetable optimization system that considers:
    - Train health and fitness status
    - Passenger demand patterns
    - Maintenance constraints
    - Energy efficiency
    - Operational reliability
    """
    
    def __init__(self):
        self.time_slots = self._generate_time_slots()
        self.stations = self._load_station_data()
        self.demand_patterns = self._load_demand_data()
        self.maintenance_constraints = self._load_maintenance_data()
        self.energy_data = self._load_energy_data()
        
        # AI Models for optimization
        self.demand_model = None
        self.energy_model = None
        self.route_optimizer = None
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def _generate_time_slots(self) -> List[str]:
        """Generate 30-minute time slots from 05:00 to 23:30"""
        slots = []
        start_time = datetime.strptime("05:00", "%H:%M")
        end_time = datetime.strptime("23:30", "%H:%M")
        
        while start_time <= end_time:
            slot_end = start_time + timedelta(minutes=30)
            slots.append(f"{start_time.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}")
            start_time = slot_end
            
        return slots
    
    def train_ml_models(self):
        """Train ML models for demand prediction and route optimization"""
        try:
            if self.demand_patterns.empty:
                return False
            
            # Prepare demand prediction features
            demand_features = []
            demand_targets = []
            
            for _, row in self.demand_patterns.iterrows():
                hour = int(row['time_slot'].split('-')[0].split(':')[0])
                features = [
                    hour,
                    1 if row['day_type'] == 'Weekday' else 0,
                    row['peak_factor'],
                    row['weather_impact'],
                    row['event_impact']
                ]
                demand_features.append(features)
                demand_targets.append(row['passenger_count'])
            
            if len(demand_features) < 10:
                return False
            
            # Scale features
            X = np.array(demand_features)
            y = np.array(demand_targets)
            X_scaled = self.scaler.fit_transform(X)
            
            # Train demand prediction model
            if XGBOOST_AVAILABLE:
                self.demand_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
            else:
                self.demand_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
            
            self.demand_model.fit(X_scaled, y)
            
            # Train energy optimization model
            if not self.energy_data.empty:
                energy_features = []
                energy_targets = []
                
                for _, row in self.energy_data.iterrows():
                    features = [
                        row['distance_traveled_km'],
                        row['passengers_carried'],
                        row['month'],
                        row['maintenance_impact'],
                        row['renewable_percentage']
                    ]
                    energy_features.append(features)
                    energy_targets.append(row['energy_consumption_kwh'])
                
                if len(energy_features) >= 5:
                    X_energy = np.array(energy_features)
                    y_energy = np.array(energy_targets)
                    X_energy_scaled = self.scaler.fit_transform(X_energy)
                    
                    self.energy_model = SVR(kernel='rbf', C=100)
                    self.energy_model.fit(X_energy_scaled, y_energy)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error training ML models: {e}")
            return False
    
    def predict_demand(self, station_name, hour, day_type='Weekday'):
        """Predict passenger demand using ML model"""
        if not self.is_trained or self.demand_model is None:
            # Fallback to historical average
            station_data = self.demand_patterns[self.demand_patterns['station_name'] == station_name]
            if not station_data.empty:
                return station_data['passenger_count'].mean()
            return 1000  # Default fallback
        
        try:
            # Prepare features
            features = [
                hour,
                1 if day_type == 'Weekday' else 0,
                1.5 if 7 <= hour <= 9 or 17 <= hour <= 19 else 0.7,  # peak_factor
                0.95,  # weather_impact
                1.0    # event_impact
            ]
            
            features_scaled = self.scaler.transform([features])
            predicted_demand = self.demand_model.predict(features_scaled)[0]
            
            return max(0, predicted_demand)
            
        except Exception as e:
            print(f"Demand prediction error: {e}")
            return 1000
    
    def optimize_route_efficiency(self, trainsets, constraints):
        """Optimize route efficiency using ML insights"""
        if not self.is_trained:
            return self._basic_route_optimization(trainsets, constraints)
        
        optimized_routes = []
        
        for trainset in trainsets:
            # Calculate efficiency score using ML
            efficiency_score = self._calculate_ml_efficiency(trainset)
            
            # Determine optimal route based on efficiency
            optimal_route = self._select_optimal_route(trainset, efficiency_score)
            
            optimized_routes.append({
                'trainset_id': trainset['id'],
                'optimal_route': optimal_route,
                'efficiency_score': efficiency_score,
                'ml_recommendation': self._get_ml_recommendation(trainset, efficiency_score)
            })
        
        return optimized_routes
    
    def _calculate_ml_efficiency(self, trainset):
        """Calculate ML-based efficiency score"""
        try:
            # Use multiple factors for efficiency calculation
            wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
            reliability = trainset['operational']['reliability_score']
            maintenance_urgency = trainset['job_cards']['open']
            
            # ML-weighted efficiency calculation
            efficiency = (
                reliability * 0.4 +
                (100 - wear_avg) * 0.3 +
                (10 - maintenance_urgency) * 0.2 +
                (100 if trainset['fitness']['overall_valid'] else 0) * 0.1
            )
            
            return max(0, min(100, efficiency))
            
        except Exception as e:
            print(f"Efficiency calculation error: {e}")
            return 50  # Default efficiency
    
    def _select_optimal_route(self, trainset, efficiency_score):
        """Select optimal route based on efficiency score"""
        routes = ["Aluva-Kakkanad", "Thrippunithura-Vytilla"]
        
        if efficiency_score > 80:
            return "Aluva-Kakkanad"  # High efficiency trains on main route
        elif efficiency_score > 60:
            return "Aluva-Kakkanad"  # Medium efficiency trains on main route
        else:
            return "Thrippunithura-Vytilla"  # Lower efficiency trains on secondary route
    
    def _get_ml_recommendation(self, trainset, efficiency_score):
        """Get ML-based recommendations"""
        recommendations = []
        
        if efficiency_score < 40:
            recommendations.append("Schedule maintenance immediately")
        elif efficiency_score < 60:
            recommendations.append("Monitor closely, consider maintenance")
        elif efficiency_score > 80:
            recommendations.append("Excellent performance, maintain current operations")
        
        if trainset['job_cards']['open'] > 2:
            recommendations.append("High maintenance backlog - prioritize")
        
        if not trainset['fitness']['overall_valid']:
            recommendations.append("Invalid fitness certificate - ground immediately")
        
        return recommendations
    
    def _basic_route_optimization(self, trainsets, constraints):
        """Basic route optimization without ML"""
        optimized_routes = []
        
        for trainset in trainsets:
            # Simple heuristic-based optimization
            if trainset['operational']['reliability_score'] > 80:
                route = "Aluva-Kakkanad"
            else:
                route = "Thrippunithura-Vytilla"
            
            optimized_routes.append({
                'trainset_id': trainset['id'],
                'optimal_route': route,
                'efficiency_score': trainset['operational']['reliability_score'],
                'ml_recommendation': ['Basic optimization applied']
            })
        
        return optimized_routes

    def _load_station_data(self) -> pd.DataFrame:
        """Load station information"""
        try:
            return pd.read_csv('metro_stations.csv')
        except:
            # Fallback data
            return pd.DataFrame({
                'station_id': ['STN-001', 'STN-002', 'STN-003', 'STN-004', 'STN-005'],
                'station_name': ['Aluva', 'Pulinchodu', 'Companypady', 'Ambattukavu', 'Muttom'],
                'daily_passengers': [16727, 22102, 12757, 24739, 21038]
            })
    
    def _load_demand_data(self) -> pd.DataFrame:
        """Load passenger demand data"""
        try:
            return pd.read_csv('passenger_demand_data.csv')
        except:
            return pd.DataFrame()
    
    def _load_maintenance_data(self) -> pd.DataFrame:
        """Load historical maintenance data"""
        try:
            return pd.read_csv('historical_maintenance.csv')
        except:
            return pd.DataFrame()
    
    def _load_energy_data(self) -> pd.DataFrame:
        """Load energy consumption data"""
        try:
            return pd.read_csv('energy_consumption.csv')
        except:
            return pd.DataFrame()
    
    def calculate_train_health_score(self, train: Dict) -> float:
        """
        Calculate comprehensive train health score considering:
        - Fitness certificates
        - Maintenance status
        - Component wear
        - Operational reliability
        """
        score = 0.0
        
        # Fitness certificates (40% weight)
        fitness_score = 0
        if train.get('fitness_rolling_stock', False):
            fitness_score += 0.4
        if train.get('fitness_signalling', False):
            fitness_score += 0.3
        if train.get('fitness_telecom', False):
            fitness_score += 0.3
        
        score += fitness_score * 0.4
        
        # Maintenance status (25% weight)
        job_cards = train.get('job_cards_open', 0)
        maintenance_score = max(0, 1 - (job_cards * 0.2))
        score += maintenance_score * 0.25
        
        # Component wear (20% weight)
        brake_wear = train.get('mileage_brake_wear', 50) / 100
        bogie_wear = train.get('mileage_bogie_wear', 50) / 100
        hvac_wear = train.get('mileage_hvac_wear', 50) / 100
        avg_wear = (brake_wear + bogie_wear + hvac_wear) / 3
        wear_score = 1 - avg_wear
        score += wear_score * 0.2
        
        # Operational reliability (15% weight)
        reliability = train.get('operational_reliability_score', 80) / 100
        score += reliability * 0.15
        
        return min(100, max(0, score * 100))
    
    def predict_demand_for_timeslot(self, time_slot: str, station_id: str) -> int:
        """
        Predict passenger demand for a specific time slot and station
        """
        if not self.demand_patterns.empty:
            filtered = self.demand_patterns[
                (self.demand_patterns['time_slot'] == time_slot) & 
                (self.demand_patterns['station_id'] == station_id)
            ]
            if not filtered.empty:
                return int(filtered['passenger_count'].mean())
        
        # Fallback prediction based on time patterns
        hour = int(time_slot.split(':')[0])
        if 7 <= hour <= 9 or 17 <= hour <= 19:  # Peak hours
            return random.randint(1500, 2500)
        elif 10 <= hour <= 16:  # Off-peak
            return random.randint(500, 1000)
        else:  # Early morning/late night
            return random.randint(200, 600)
    
    def calculate_route_efficiency(self, route: str, trains: List[Dict]) -> float:
        """
        Calculate route efficiency based on:
        - Train capacity utilization
        - Energy consumption
        - Maintenance requirements
        """
        if not trains:
            return 0.0
        
        total_capacity = sum(self._get_train_capacity(train) for train in trains)
        avg_health = sum(self.calculate_train_health_score(train) for train in trains) / len(trains)
        
        # Efficiency score based on health and capacity
        efficiency = (avg_health / 100) * 0.7 + (min(1.0, total_capacity / 1000) * 0.3)
        
        return efficiency
    
    def _get_train_capacity(self, train: Dict) -> int:
        """Get effective train capacity based on health"""
        base_capacity = 300
        health_score = self.calculate_train_health_score(train) / 100
        
        # Reduce capacity if train has issues
        if train.get('operational_status') == 'Maintenance':
            health_score *= 0.5
        elif train.get('operational_status') == 'IBL':
            health_score *= 0.3
        
        return int(base_capacity * health_score)
    
    def optimize_timetable(self, trainsets: List[Dict], constraints: Dict = None) -> Dict:
        """
        Main optimization function that creates an AI-powered timetable
        """
        if constraints is None:
            constraints = {
                'max_trains_per_slot': 15,
                'min_trains_per_slot': 5,
                'peak_hour_multiplier': 1.5,
                'maintenance_buffer': 0.1
            }
        
        # Filter available trains
        available_trains = [
            train for train in trainsets 
            if train.get('operational_status') in ['Available', 'Standby']
        ]
        
        # Sort trains by health score (highest first)
        available_trains.sort(
            key=lambda x: self.calculate_train_health_score(x), 
            reverse=True
        )
        
        timetable = {}
        
        for time_slot in self.time_slots:
            # Determine if this is a peak hour
            hour = int(time_slot.split(':')[0])
            is_peak = 7 <= hour <= 9 or 17 <= hour <= 19
            
            # Calculate required trains based on demand
            total_demand = sum(
                self.predict_demand_for_timeslot(time_slot, station['station_id'])
                for _, station in self.stations.iterrows()
            )
            
            # Adjust for peak hours
            if is_peak:
                total_demand *= constraints['peak_hour_multiplier']
            
            # Calculate required trains (assuming 300 passengers per train)
            required_trains = max(
                constraints['min_trains_per_slot'],
                min(constraints['max_trains_per_slot'], int(total_demand / 300))
            )
            
            # Select best trains for this slot
            selected_trains = self._select_trains_for_slot(
                available_trains, required_trains, time_slot
            )
            
            # Assign routes
            route_assignments = self._assign_routes(selected_trains)
            
            timetable[time_slot] = {
                'trains': selected_trains,
                'route_assignments': route_assignments,
                'total_capacity': sum(self._get_train_capacity(train) for train in selected_trains),
                'avg_health_score': sum(self.calculate_train_health_score(train) for train in selected_trains) / len(selected_trains) if selected_trains else 0,
                'is_peak_hour': is_peak,
                'predicted_demand': total_demand
            }
        
        return timetable
    
    def _select_trains_for_slot(self, trains: List[Dict], required: int, time_slot: str) -> List[Dict]:
        """
        Select optimal trains for a time slot considering:
        - Health scores
        - Maintenance schedules
        - Energy efficiency
        """
        selected = []
        available = trains.copy()
        
        # Sort by health score and other factors
        available.sort(key=lambda x: (
            self.calculate_train_health_score(x),
            -x.get('job_cards_open', 0),
            x.get('operational_reliability_score', 0)
        ), reverse=True)
        
        for i in range(min(required, len(available))):
            if available:
                train = available.pop(0)
                selected.append(train)
        
        return selected
    
    def _assign_routes(self, trains: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Assign trains to routes based on depot location and demand
        """
        routes = {
            'Aluva-Kakkanad': [],
            'Thrippunithura-Vytilla': []
        }
        
        for train in trains:
            depot = train.get('depot', '')
            
            if 'Aluva' in depot:
                routes['Aluva-Kakkanad'].append(train)
            elif 'Petta' in depot:
                # Assign to either route based on demand
                if len(routes['Thrippunithura-Vytilla']) < len(routes['Aluva-Kakkanad']):
                    routes['Thrippunithura-Vytilla'].append(train)
                else:
                    routes['Aluva-Kakkanad'].append(train)
            else:
                # Default assignment
                routes['Aluva-Kakkanad'].append(train)
        
        return routes
    
    def generate_optimization_report(self, timetable: Dict) -> Dict:
        """
        Generate comprehensive optimization report
        """
        total_trains = sum(len(slot['trains']) for slot in timetable.values())
        total_capacity = sum(slot['total_capacity'] for slot in timetable.values())
        avg_health = sum(slot['avg_health_score'] for slot in timetable.values()) / len(timetable)
        
        peak_slots = [slot for slot in timetable.values() if slot['is_peak_hour']]
        off_peak_slots = [slot for slot in timetable.values() if not slot['is_peak_hour']]
        
        report = {
            'summary': {
                'total_time_slots': len(timetable),
                'total_trains_deployed': total_trains,
                'total_capacity': total_capacity,
                'average_health_score': round(avg_health, 2),
                'peak_hour_slots': len(peak_slots),
                'off_peak_slots': len(off_peak_slots)
            },
            'efficiency_metrics': {
                'capacity_utilization': round(total_capacity / (len(timetable) * 300 * 10), 2),
                'health_distribution': self._analyze_health_distribution(timetable),
                'route_balance': self._analyze_route_balance(timetable)
            },
            'recommendations': self._generate_recommendations(timetable)
        }
        
        return report
    
    def _analyze_health_distribution(self, timetable: Dict) -> Dict:
        """Analyze distribution of train health scores"""
        health_scores = [slot['avg_health_score'] for slot in timetable.values()]
        
        return {
            'min_health': round(min(health_scores), 2),
            'max_health': round(max(health_scores), 2),
            'avg_health': round(sum(health_scores) / len(health_scores), 2),
            'health_variance': round(np.var(health_scores), 2)
        }
    
    def _analyze_route_balance(self, timetable: Dict) -> Dict:
        """Analyze route assignment balance"""
        aluva_trains = sum(len(slot['route_assignments']['Aluva-Kakkanad']) for slot in timetable.values())
        thrippunithura_trains = sum(len(slot['route_assignments']['Thrippunithura-Vytilla']) for slot in timetable.values())
        
        total = aluva_trains + thrippunithura_trains
        
        return {
            'aluva_kakkanad_percentage': round((aluva_trains / total) * 100, 2) if total > 0 else 0,
            'thrippunithura_vytilla_percentage': round((thrippunithura_trains / total) * 100, 2) if total > 0 else 0,
            'balance_ratio': round(aluva_trains / thrippunithura_trains, 2) if thrippunithura_trains > 0 else float('inf')
        }
    
    def _generate_recommendations(self, timetable: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Analyze health scores
        health_scores = [slot['avg_health_score'] for slot in timetable.values()]
        low_health_slots = [slot for slot in timetable.values() if slot['avg_health_score'] < 70]
        
        if low_health_slots:
            recommendations.append(
                f"Consider maintenance for {len(low_health_slots)} time slots with health scores below 70"
            )
        
        # Analyze capacity utilization
        total_capacity = sum(slot['total_capacity'] for slot in timetable.values())
        total_demand = sum(slot['predicted_demand'] for slot in timetable.values())
        
        if total_capacity < total_demand * 0.8:
            recommendations.append("Increase train capacity to meet predicted demand")
        elif total_capacity > total_demand * 1.2:
            recommendations.append("Consider reducing train deployment to improve efficiency")
        
        # Analyze route balance
        route_balance = self._analyze_route_balance(timetable)
        if route_balance['balance_ratio'] > 2 or route_balance['balance_ratio'] < 0.5:
            recommendations.append("Rebalance route assignments for better distribution")
        
        return recommendations

# Example usage and testing
if __name__ == "__main__":
    # Initialize the AI optimizer
    optimizer = AITimetableOptimizer()
    
    # Load trainset data
    try:
        trainsets_df = pd.read_csv('trainsets_ml_ready.csv')
        trainsets = trainsets_df.to_dict('records')
    except:
        print("Could not load trainsets data. Using sample data.")
        trainsets = [
            {
                'trainset_id': 'KMRL-001',
                'depot': 'Muttom Yard',
                'fitness_rolling_stock': True,
                'fitness_signalling': True,
                'fitness_telecom': False,
                'job_cards_open': 0,
                'operational_status': 'Available',
                'operational_reliability_score': 78,
                'mileage_brake_wear': 80,
                'mileage_bogie_wear': 78,
                'mileage_hvac_wear': 81
            }
        ]
    
    # Define constraints
    constraints = {
        'max_trains_per_slot': 12,
        'min_trains_per_slot': 4,
        'peak_hour_multiplier': 1.8,
        'maintenance_buffer': 0.15
    }
    
    # Generate optimized timetable
    print("Generating AI-powered timetable...")
    timetable = optimizer.optimize_timetable(trainsets, constraints)
    
    # Generate report
    report = optimizer.generate_optimization_report(timetable)
    
    print("\n=== AI TIMETABLE OPTIMIZATION REPORT ===")
    print(f"Total time slots: {report['summary']['total_time_slots']}")
    print(f"Total trains deployed: {report['summary']['total_trains_deployed']}")
    print(f"Average health score: {report['summary']['average_health_score']}")
    print(f"Peak hour slots: {report['summary']['peak_hour_slots']}")
    
    print("\n=== EFFICIENCY METRICS ===")
    print(f"Capacity utilization: {report['efficiency_metrics']['capacity_utilization']}")
    print(f"Health distribution: {report['efficiency_metrics']['health_distribution']}")
    print(f"Route balance: {report['efficiency_metrics']['route_balance']}")
    
    print("\n=== RECOMMENDATIONS ===")
    for rec in report['recommendations']:
        print(f"• {rec}")
    
    print("\n=== SAMPLE TIMETABLE SLOTS ===")
    for i, (slot, data) in enumerate(list(timetable.items())[:5]):
        print(f"{slot}: {len(data['trains'])} trains, Health: {data['avg_health_score']:.1f}, Demand: {data['predicted_demand']}")
