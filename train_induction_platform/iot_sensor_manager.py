from common_imports import *

class IoTSensorManager:
    """
    IoT Sensor data collection and management
    Handles various sensors for train and station monitoring
    """
    
    def __init__(self):
        self.sensors = {
            'vibration': {},
            'temperature': {},
            'noise': {},
            'air_quality': {},
            'weight': {},
            'humidity': {}
        }
        self.sensor_data = {}
        self.anomaly_detector = None
        self.is_trained = False
        
    def initialize_sensors(self, trainsets):
        """Initialize sensors for all trainsets"""
        for trainset in trainsets:
            trainset_id = trainset['id']
            
            # Initialize sensor data structure
            self.sensor_data[trainset_id] = {
                'vibration': {
                    'current': random.uniform(0.1, 2.0),  # mm/s
                    'threshold': 2.5,
                    'status': 'Normal',
                    'last_update': datetime.now()
                },
                'temperature': {
                    'current': random.uniform(20, 35),  # Celsius
                    'threshold': 40,
                    'status': 'Normal',
                    'last_update': datetime.now()
                },
                'noise': {
                    'current': random.uniform(60, 85),  # dB
                    'threshold': 90,
                    'status': 'Normal',
                    'last_update': datetime.now()
                },
                'air_quality': {
                    'current': random.uniform(50, 150),  # AQI
                    'threshold': 200,
                    'status': 'Good',
                    'last_update': datetime.now()
                },
                'weight': {
                    'current': random.uniform(200, 400),  # tons
                    'capacity': 450,
                    'status': 'Normal',
                    'last_update': datetime.now()
                },
                'humidity': {
                    'current': random.uniform(40, 80),  # %
                    'threshold': 85,
                    'status': 'Normal',
                    'last_update': datetime.now()
                }
            }
    
    def update_sensor_data(self, trainset_id, sensor_type, value):
        """Update sensor data for a specific trainset"""
        if trainset_id not in self.sensor_data:
            return False
        
        if sensor_type not in self.sensor_data[trainset_id]:
            return False
        
        # Update sensor data
        self.sensor_data[trainset_id][sensor_type]['current'] = value
        self.sensor_data[trainset_id][sensor_type]['last_update'] = datetime.now()
        
        # Check thresholds and update status
        self._check_sensor_threshold(trainset_id, sensor_type, value)
        
        return True
    
    def _check_sensor_threshold(self, trainset_id, sensor_type, value):
        """Check if sensor value exceeds threshold"""
        sensor_data = self.sensor_data[trainset_id][sensor_type]
        
        if sensor_type == 'vibration':
            if value > sensor_data['threshold']:
                sensor_data['status'] = 'Warning'
            elif value > sensor_data['threshold'] * 0.8:
                sensor_data['status'] = 'Caution'
            else:
                sensor_data['status'] = 'Normal'
        
        elif sensor_type == 'temperature':
            if value > sensor_data['threshold']:
                sensor_data['status'] = 'Critical'
            elif value > sensor_data['threshold'] * 0.9:
                sensor_data['status'] = 'Warning'
            else:
                sensor_data['status'] = 'Normal'
        
        elif sensor_type == 'noise':
            if value > sensor_data['threshold']:
                sensor_data['status'] = 'Critical'
            elif value > sensor_data['threshold'] * 0.9:
                sensor_data['status'] = 'Warning'
            else:
                sensor_data['status'] = 'Normal'
        
        elif sensor_type == 'air_quality':
            if value > sensor_data['threshold']:
                sensor_data['status'] = 'Unhealthy'
            elif value > 100:
                sensor_data['status'] = 'Moderate'
            else:
                sensor_data['status'] = 'Good'
        
        elif sensor_type == 'weight':
            if value > sensor_data['capacity']:
                sensor_data['status'] = 'Overloaded'
            elif value > sensor_data['capacity'] * 0.9:
                sensor_data['status'] = 'Near Capacity'
            else:
                sensor_data['status'] = 'Normal'
        
        elif sensor_type == 'humidity':
            if value > sensor_data['threshold']:
                sensor_data['status'] = 'High'
            elif value < 30:
                sensor_data['status'] = 'Low'
            else:
                sensor_data['status'] = 'Normal'
    
    def simulate_sensor_updates(self, trainsets):
        """Simulate real-time sensor updates"""
        for trainset in trainsets:
            trainset_id = trainset['id']
            
            if trainset_id not in self.sensor_data:
                continue
            
            # Simulate realistic sensor variations
            for sensor_type in self.sensor_data[trainset_id]:
                current_value = self.sensor_data[trainset_id][sensor_type]['current']
                
                # Add realistic variation based on sensor type
                if sensor_type == 'vibration':
                    variation = random.uniform(-0.1, 0.1)
                    new_value = max(0, current_value + variation)
                elif sensor_type == 'temperature':
                    variation = random.uniform(-1, 1)
                    new_value = max(15, min(45, current_value + variation))
                elif sensor_type == 'noise':
                    variation = random.uniform(-2, 2)
                    new_value = max(50, min(100, current_value + variation))
                elif sensor_type == 'air_quality':
                    variation = random.uniform(-5, 5)
                    new_value = max(20, min(300, current_value + variation))
                elif sensor_type == 'weight':
                    variation = random.uniform(-10, 10)
                    new_value = max(100, min(500, current_value + variation))
                elif sensor_type == 'humidity':
                    variation = random.uniform(-2, 2)
                    new_value = max(20, min(95, current_value + variation))
                
                self.update_sensor_data(trainset_id, sensor_type, new_value)
    
    def get_sensor_alerts(self, trainset_id):
        """Get alerts for a specific trainset based on sensor data"""
        if trainset_id not in self.sensor_data:
            return []
        
        alerts = []
        sensor_data = self.sensor_data[trainset_id]
        
        for sensor_type, data in sensor_data.items():
            if data['status'] in ['Warning', 'Critical', 'Unhealthy', 'Overloaded']:
                alerts.append({
                    'sensor_type': sensor_type,
                    'value': data['current'],
                    'status': data['status'],
                    'threshold': data.get('threshold', data.get('capacity', 'N/A')),
                    'timestamp': data['last_update']
                })
        
        return alerts
    
    def get_fleet_sensor_summary(self):
        """Get sensor summary for entire fleet"""
        summary = {
            'total_trainsets': len(self.sensor_data),
            'alerts': [],
            'sensor_stats': {},
            'health_score': 0
        }
        
        total_health_score = 0
        trainset_count = 0
        
        for trainset_id, sensors in self.sensor_data.items():
            trainset_count += 1
            trainset_health = 100
            
            # Check each sensor
            for sensor_type, data in sensors.items():
                if sensor_type not in summary['sensor_stats']:
                    summary['sensor_stats'][sensor_type] = {
                        'normal': 0, 'warning': 0, 'critical': 0
                    }
                
                if data['status'] == 'Normal':
                    summary['sensor_stats'][sensor_type]['normal'] += 1
                elif data['status'] in ['Warning', 'Caution']:
                    summary['sensor_stats'][sensor_type]['warning'] += 1
                    trainset_health -= 20
                else:
                    summary['sensor_stats'][sensor_type]['critical'] += 1
                    trainset_health -= 40
                
                # Add alerts
                if data['status'] in ['Warning', 'Critical', 'Unhealthy', 'Overloaded']:
                    summary['alerts'].append({
                        'trainset_id': trainset_id,
                        'sensor_type': sensor_type,
                        'value': data['current'],
                        'status': data['status']
                    })
            
            total_health_score += max(0, trainset_health)
        
        summary['health_score'] = total_health_score / max(1, trainset_count)
        return summary
    
    def train_anomaly_detector(self, historical_data):
        """Train anomaly detection model for sensor data"""
        try:
            if len(historical_data) < 100:
                return False
            
            # Prepare features
            features = []
            for record in historical_data:
                feature_vector = [
                    record['vibration'],
                    record['temperature'],
                    record['noise'],
                    record['air_quality'],
                    record['weight'],
                    record['humidity']
                ]
                features.append(feature_vector)
            
            X = np.array(features)
            
            # Train Isolation Forest for anomaly detection
            self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
            self.anomaly_detector.fit(X)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Anomaly detector training error: {e}")
            return False
    
    def detect_anomalies(self, trainset_id):
        """Detect anomalies in sensor data for a specific trainset"""
        if not self.is_trained or trainset_id not in self.sensor_data:
            return None
        
        try:
            # Prepare current sensor data
            sensors = self.sensor_data[trainset_id]
            feature_vector = [
                sensors['vibration']['current'],
                sensors['temperature']['current'],
                sensors['noise']['current'],
                sensors['air_quality']['current'],
                sensors['weight']['current'],
                sensors['humidity']['current']
            ]
            
            # Predict anomaly
            anomaly_score = self.anomaly_detector.decision_function([feature_vector])[0]
            is_anomaly = self.anomaly_detector.predict([feature_vector])[0] == -1
            
            return {
                'is_anomaly': is_anomaly,
                'anomaly_score': anomaly_score,
                'confidence': abs(anomaly_score)
            }
            
        except Exception as e:
            print(f"Anomaly detection error: {e}")
            return None
    
    def get_sensor_insights(self, trainset_id):
        """Get comprehensive sensor insights for a trainset"""
        if trainset_id not in self.sensor_data:
            return None
        
        sensors = self.sensor_data[trainset_id]
        alerts = self.get_sensor_alerts(trainset_id)
        anomaly = self.detect_anomalies(trainset_id)
        
        # Calculate overall health score
        health_score = 100
        for sensor_type, data in sensors.items():
            if data['status'] in ['Warning', 'Caution']:
                health_score -= 15
            elif data['status'] in ['Critical', 'Unhealthy', 'Overloaded']:
                health_score -= 30
        
        health_score = max(0, health_score)
        
        return {
            'trainset_id': trainset_id,
            'sensors': sensors,
            'alerts': alerts,
            'anomaly': anomaly,
            'health_score': health_score,
            'overall_status': 'Good' if health_score > 80 else 'Warning' if health_score > 60 else 'Critical'
        }
