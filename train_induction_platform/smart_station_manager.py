from common_imports import *

class SmartStationManager:
    """
    Smart Station Management System
    Handles crowd density, facility optimization, and station analytics
    """
    
    def __init__(self):
        self.stations = {}
        self.crowd_density_model = None
        self.facility_optimizer = None
        self.is_trained = False
        
    def initialize_stations(self):
        """Initialize station data from CSV"""
        try:
            stations_df = pd.read_csv('metro_stations.csv')
            
            for _, row in stations_df.iterrows():
                station_id = row['station_id']
                self.stations[station_id] = {
                    'station_name': row['station_name'],
                    'latitude': row['latitude'],
                    'longitude': row['longitude'],
                    'line': row['line'],
                    'platforms': row['platforms'],
                    'elevators': row['elevators'],
                    'escalators': row['escalators'],
                    'parking_capacity': row['parking_capacity'],
                    'daily_passengers': row['daily_passengers'],
                    'commercial_spaces': row['commercial_spaces'],
                    'accessibility_score': row['accessibility_score'],
                    'current_crowd_density': random.uniform(0.3, 0.8),
                    'facility_utilization': {
                        'elevators': random.uniform(0.4, 0.9),
                        'escalators': random.uniform(0.6, 0.95),
                        'parking': random.uniform(0.3, 0.8),
                        'commercial': random.uniform(0.2, 0.7)
                    },
                    'last_update': datetime.now()
                }
        except Exception as e:
            print(f"Error loading stations: {e}")
            self._create_mock_stations()
    
    def _create_mock_stations(self):
        """Create mock station data if CSV is not available"""
        mock_stations = [
            {'station_name': 'Aluva', 'platforms': 2, 'elevators': 1, 'escalators': 6},
            {'station_name': 'Pulinchodu', 'platforms': 2, 'elevators': 3, 'escalators': 5},
            {'station_name': 'Companypady', 'platforms': 4, 'elevators': 3, 'escalators': 5},
            {'station_name': 'Ambattukavu', 'platforms': 2, 'elevators': 1, 'escalators': 2},
            {'station_name': 'Muttom', 'platforms': 3, 'elevators': 2, 'escalators': 4}
        ]
        
        for i, station in enumerate(mock_stations):
            station_id = f"STN-{i+1:03d}"
            self.stations[station_id] = {
                'station_name': station['station_name'],
                'platforms': station['platforms'],
                'elevators': station['elevators'],
                'escalators': station['escalators'],
                'current_crowd_density': random.uniform(0.3, 0.8),
                'facility_utilization': {
                    'elevators': random.uniform(0.4, 0.9),
                    'escalators': random.uniform(0.6, 0.95),
                    'parking': random.uniform(0.3, 0.8),
                    'commercial': random.uniform(0.2, 0.7)
                },
                'last_update': datetime.now()
            }
    
    def update_crowd_density(self, station_id, density):
        """Update crowd density for a station"""
        if station_id in self.stations:
            self.stations[station_id]['current_crowd_density'] = max(0, min(1, density))
            self.stations[station_id]['last_update'] = datetime.now()
            return True
        return False
    
    def predict_crowd_density(self, station_id, hour, day_type='Weekday'):
        """Predict crowd density for a station at specific time"""
        if not self.is_trained or station_id not in self.stations:
            return self._predict_basic_crowd_density(hour, day_type)
        
        try:
            # Prepare features for ML model
            station_data = self.stations[station_id]
            features = [
                hour,
                1 if day_type == 'Weekday' else 0,
                station_data['platforms'],
                station_data['elevators'],
                station_data['escalators'],
                station_data['daily_passengers'] / 1000,  # Normalize
                station_data['accessibility_score']
            ]
            
            # Use trained model to predict density
            predicted_density = self.crowd_density_model.predict([features])[0]
            return max(0, min(1, predicted_density))
            
        except Exception as e:
            print(f"Crowd density prediction error: {e}")
            return self._predict_basic_crowd_density(hour, day_type)
    
    def _predict_basic_crowd_density(self, hour, day_type):
        """Basic crowd density prediction"""
        # Peak hours have higher density
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            base_density = 0.8
        elif 10 <= hour <= 16:
            base_density = 0.6
        else:
            base_density = 0.4
        
        # Weekends have different patterns
        if day_type == 'Weekend':
            base_density *= 0.8
        
        return base_density + random.uniform(-0.1, 0.1)
    
    def optimize_facility_utilization(self, station_id):
        """Optimize facility utilization for a station"""
        if station_id not in self.stations:
            return None
        
        station = self.stations[station_id]
        current_density = station['current_crowd_density']
        utilization = station['facility_utilization']
        
        recommendations = []
        
        # Elevator optimization
        if utilization['elevators'] > 0.8 and current_density > 0.7:
            recommendations.append({
                'facility': 'Elevators',
                'action': 'Increase frequency',
                'priority': 'High',
                'reason': 'High utilization during peak crowd'
            })
        
        # Escalator optimization
        if utilization['escalators'] > 0.9:
            recommendations.append({
                'facility': 'Escalators',
                'action': 'Maintenance check required',
                'priority': 'Medium',
                'reason': 'Very high utilization'
            })
        
        # Parking optimization
        if utilization['parking'] > 0.9:
            recommendations.append({
                'facility': 'Parking',
                'action': 'Consider overflow parking',
                'priority': 'High',
                'reason': 'Parking at capacity'
            })
        
        # Commercial space optimization
        if utilization['commercial'] < 0.3 and current_density > 0.6:
            recommendations.append({
                'facility': 'Commercial Spaces',
                'action': 'Increase promotional activities',
                'priority': 'Low',
                'reason': 'Low utilization despite high footfall'
            })
        
        return recommendations
    
    def get_station_health_score(self, station_id):
        """Calculate health score for a station"""
        if station_id not in self.stations:
            return 0
        
        station = self.stations[station_id]
        utilization = station['facility_utilization']
        crowd_density = station['current_crowd_density']
        
        # Calculate health score based on various factors
        health_score = 100
        
        # Crowd density impact
        if crowd_density > 0.8:
            health_score -= 20
        elif crowd_density > 0.6:
            health_score -= 10
        
        # Facility utilization impact
        for facility, util in utilization.items():
            if util > 0.9:
                health_score -= 15
            elif util > 0.8:
                health_score -= 10
            elif util < 0.2:
                health_score -= 5
        
        return max(0, health_score)
    
    def train_crowd_density_model(self, historical_data):
        """Train ML model for crowd density prediction"""
        try:
            if len(historical_data) < 100:
                return False
            
            # Prepare training data
            features = []
            targets = []
            
            for record in historical_data:
                feature_vector = [
                    record['hour'],
                    1 if record['day_type'] == 'Weekday' else 0,
                    record['platforms'],
                    record['elevators'],
                    record['escalators'],
                    record['daily_passengers'] / 1000,
                    record['accessibility_score']
                ]
                features.append(feature_vector)
                targets.append(record['crowd_density'])
            
            # Train model
            X = np.array(features)
            y = np.array(targets)
            
            self.crowd_density_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.crowd_density_model.fit(X, y)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Crowd density model training error: {e}")
            return False
    
    def get_station_analytics(self, station_id):
        """Get comprehensive analytics for a station"""
        if station_id not in self.stations:
            return None
        
        station = self.stations[station_id]
        
        analytics = {
            'station_id': station_id,
            'station_name': station['station_name'],
            'current_crowd_density': station['current_crowd_density'],
            'facility_utilization': station['facility_utilization'],
            'health_score': self.get_station_health_score(station_id),
            'recommendations': self.optimize_facility_utilization(station_id),
            'last_update': station['last_update']
        }
        
        return analytics
    
    def get_fleet_station_summary(self):
        """Get summary of all stations"""
        summary = {
            'total_stations': len(self.stations),
            'stations': [],
            'overall_health': 0,
            'crowd_alerts': []
        }
        
        total_health = 0
        
        for station_id, station in self.stations.items():
            health_score = self.get_station_health_score(station_id)
            total_health += health_score
            
            station_summary = {
                'station_id': station_id,
                'station_name': station['station_name'],
                'crowd_density': station['current_crowd_density'],
                'health_score': health_score,
                'status': 'Good' if health_score > 80 else 'Warning' if health_score > 60 else 'Critical'
            }
            
            summary['stations'].append(station_summary)
            
            # Add crowd alerts
            if station['current_crowd_density'] > 0.8:
                summary['crowd_alerts'].append({
                    'station_id': station_id,
                    'station_name': station['station_name'],
                    'crowd_density': station['current_crowd_density'],
                    'severity': 'High' if station['current_crowd_density'] > 0.9 else 'Medium'
                })
        
        summary['overall_health'] = total_health / len(self.stations) if self.stations else 0
        return summary
    
    def simulate_station_updates(self):
        """Simulate real-time station updates"""
        for station_id, station in self.stations.items():
            # Simulate crowd density changes
            current_density = station['current_crowd_density']
            variation = random.uniform(-0.1, 0.1)
            new_density = max(0, min(1, current_density + variation))
            station['current_crowd_density'] = new_density
            
            # Simulate facility utilization changes
            for facility in station['facility_utilization']:
                current_util = station['facility_utilization'][facility]
                variation = random.uniform(-0.05, 0.05)
                new_util = max(0, min(1, current_util + variation))
                station['facility_utilization'][facility] = new_util
            
            station['last_update'] = datetime.now()
