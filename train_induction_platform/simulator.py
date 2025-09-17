from common_imports import *
from utils import calculate_ai_score

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
        """ Generate a synthetic trainset with realistic patterns based on historical data   """
        now = datetime.now()
        # Base patterns from historical data if available
        if historical_data and not historical_data.empty:
            pass  # Would implement ML-based pattern extraction in real system
        # Generate realistic expiry dates (clustered around maintenance cycles)
        maintenance_cycle = random.choice([30, 60, 90])
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
        """Generate a more realistic dataset with correlated patterns """
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
# Advanced AI Optimization Engine