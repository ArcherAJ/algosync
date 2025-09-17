import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def create_trainsets_csv():
    """Create comprehensive trainsets data for AI/ML"""
    n_trainsets = 100  # Large dataset for ML
    
    data = {
        'trainset_id': [],
        'depot': [],
        'fitness_rolling_stock': [],
        'fitness_signalling': [],
        'fitness_telecom': [],
        'fitness_expires_at': [],
        'fitness_days_until_expiry': [],
        'job_cards_open': [],
        'job_cards_priority': [],
        'job_cards_maintenance_type': [],
        'branding_advertiser': [],
        'branding_contract_value': [],
        'branding_hours_required': [],
        'branding_exposure_deficit': [],
        'mileage_total_km': [],
        'mileage_since_maintenance': [],
        'mileage_brake_wear': [],
        'mileage_bogie_wear': [],
        'mileage_hvac_wear': [],
        'cleaning_interior_status': [],
        'cleaning_exterior_status': [],
        'cleaning_days_since_clean': [],
        'operational_status': [],
        'operational_reliability_score': [],
        'operational_days_since_service': [],
        'ai_score': [],
        'recommendation': [],
        'timestamp': []
    }
    
    depots = ['Aluva Depot', 'Petta Depot', 'Muttom Yard', 'Kakkanad Depot']
    advertisers = ['Coca-Cola', 'Pepsi', 'Amazon', 'Google', 'Microsoft', 'Apple', 
                  'Samsung', 'Toyota', 'Flipkart', 'BSNL', 'Airtel', 'Jio', None]
    priorities = ['Low', 'Medium', 'High', 'Critical']
    maintenance_types = ['Routine', 'Preventive', 'Corrective', 'Emergency']
    statuses = ['Available', 'Standby', 'Maintenance', 'IBL']
    cleaning_statuses = ['Clean', 'Requires Cleaning']
    
    current_time = datetime.now()
    
    for i in range(1, n_trainsets + 1):
        trainset_id = f"KMRL-{str(i).zfill(3)}"
        total_km = random.randint(20000, 250000)
        wear_factor = total_km / 250000
        
        # Generate correlated features
        reliability = max(70, 100 - int(wear_factor * 30))
        open_jobs = random.randint(0, min(6, int(wear_factor * 8)))
        days_since_service = random.randint(0, 90)
        
        data['trainset_id'].append(trainset_id)
        data['depot'].append(random.choice(depots))
        
        # Fitness data with correlations
        data['fitness_rolling_stock'].append(random.random() > (0.05 + wear_factor * 0.1))
        data['fitness_signalling'].append(random.random() > (0.03 + wear_factor * 0.08))
        data['fitness_telecom'].append(random.random() > (0.04 + wear_factor * 0.09))
        
        expiry_date = current_time + timedelta(days=random.randint(1, 60))
        data['fitness_expires_at'].append(expiry_date)
        data['fitness_days_until_expiry'].append((expiry_date - current_time).days)
        
        # Job cards with correlation to wear
        data['job_cards_open'].append(open_jobs)
        data['job_cards_priority'].append(random.choices(priorities, 
                                                       weights=[0.4, 0.3, 0.2, 0.1])[0])
        data['job_cards_maintenance_type'].append(random.choice(maintenance_types))
        
        # Branding data
        advertiser = random.choice(advertisers)
        data['branding_advertiser'].append(advertiser)
        data['branding_contract_value'].append(random.randint(20000, 200000) if advertiser else 0)
        data['branding_hours_required'].append(random.randint(0, 12))
        data['branding_exposure_deficit'].append(random.randint(0, 48))
        
        # Mileage data
        data['mileage_total_km'].append(total_km)
        data['mileage_since_maintenance'].append(random.randint(1000, 10000))
        data['mileage_brake_wear'].append(min(100, int(20 + wear_factor * 80)))
        data['mileage_bogie_wear'].append(min(100, int(15 + wear_factor * 85)))
        data['mileage_hvac_wear'].append(min(100, int(25 + wear_factor * 75)))
        
        # Cleaning data
        data['cleaning_interior_status'].append(random.choices(cleaning_statuses, 
                                                             weights=[0.7, 0.3])[0])
        data['cleaning_exterior_status'].append(random.choices(cleaning_statuses, 
                                                             weights=[0.6, 0.4])[0])
        data['cleaning_days_since_clean'].append(random.randint(0, 7))
        
        # Operational data
        data['operational_status'].append(random.choices(statuses, 
                                                       weights=[0.6, 0.2, 0.15, 0.05])[0])
        data['operational_reliability_score'].append(reliability)
        data['operational_days_since_service'].append(days_since_service)
        
        # AI Score calculation (simplified)
        ai_score = reliability - (open_jobs * 5) - (wear_factor * 15)
        ai_score = max(0, min(100, ai_score))
        data['ai_score'].append(ai_score)
        
        # Recommendation based on score
        if ai_score < 40 or data['operational_status'][-1] == 'IBL':
            recommendation = 'IBL'
        elif ai_score > 75:
            recommendation = 'Service'
        else:
            recommendation = 'Standby'
        data['recommendation'].append(recommendation)
        
        data['timestamp'].append(current_time)
    
    df = pd.DataFrame(data)
    df.to_csv('trainsets_ml_ready.csv', index=False)
    return df

def create_historical_maintenance_csv():
    """Create historical maintenance data for predictive modeling"""
    n_records = 500
    
    data = {
        'maintenance_id': [],
        'trainset_id': [],
        'maintenance_date': [],
        'maintenance_type': [],
        'duration_hours': [],
        'cost': [],
        'components_replaced': [],
        'technician_id': [],
        'priority': [],
        'downtime_days': [],
        'preventive_flag': [],
        'failure_severity': []
    }
    
    maintenance_types = ['Routine', 'Preventive', 'Corrective', 'Emergency']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    components = ['Brakes', 'Engines', 'Doors', 'HVAC', 'Bogies', 'Electrical', 'Signalling']
    technicians = [f'TECH-{i:03d}' for i in range(1, 21)]
    
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(1, n_records + 1):
        data['maintenance_id'].append(f"MTN-{i:04d}")
        data['trainset_id'].append(f"KMRL-{random.randint(1, 100):03d}")
        
        # Random date in the past year
        random_days = random.randint(0, 365)
        maintenance_date = start_date + timedelta(days=random_days)
        data['maintenance_date'].append(maintenance_date)
        
        maintenance_type = random.choice(maintenance_types)
        data['maintenance_type'].append(maintenance_type)
        
        # Correlated features
        if maintenance_type == 'Emergency':
            duration = random.randint(8, 48)
            cost = random.randint(50000, 200000)
            downtime = random.randint(3, 10)
            severity = random.randint(7, 10)
            components_count = random.randint(2, 5)
        elif maintenance_type == 'Corrective':
            duration = random.randint(4, 16)
            cost = random.randint(20000, 80000)
            downtime = random.randint(1, 5)
            severity = random.randint(4, 7)
            components_count = random.randint(1, 3)
        else:
            duration = random.randint(2, 8)
            cost = random.randint(5000, 20000)
            downtime = random.randint(0, 2)
            severity = random.randint(1, 4)
            components_count = random.randint(0, 2)
        
        data['duration_hours'].append(duration)
        data['cost'].append(cost)
        data['components_replaced'].append(', '.join(random.sample(components, components_count)))
        data['technician_id'].append(random.choice(technicians))
        data['priority'].append(random.choice(priorities))
        data['downtime_days'].append(downtime)
        data['preventive_flag'].append(maintenance_type == 'Preventive')
        data['failure_severity'].append(severity)
    
    df = pd.DataFrame(data)
    df.to_csv('historical_maintenance.csv', index=False)
    return df

def create_passenger_demand_csv():
    """Create passenger demand data for timetable optimization"""
    n_days = 365
    time_slots = [f"{h:02d}:00-{h+1:02d}:00" for h in range(5, 24)]
    
    data = {
        'date': [],
        'time_slot': [],
        'passenger_count': [],
        'line': [],
        'weather_condition': [],
        'day_of_week': [],
        'is_holiday': [],
        'special_event': []
    }
    
    lines = ['Aluva-Kakkanad', 'Thrippunithura-Vytilla']
    weather_conditions = ['Sunny', 'Cloudy', 'Rainy', 'Stormy']
    special_events = [None, 'Festival', 'Sports Event', 'Concert', 'Protest']
    
    start_date = datetime.now() - timedelta(days=n_days)
    
    for day in range(n_days):
        current_date = start_date + timedelta(days=day)
        day_of_week = current_date.weekday()
        is_weekend = day_of_week >= 5
        is_holiday = random.random() < 0.1  # 10% chance of holiday
        
        for time_slot in time_slots:
            hour = int(time_slot.split(':')[0])
            
            # Base demand pattern
            if 7 <= hour <= 9 or 17 <= hour <= 19:  # Peak hours
                base_demand = random.randint(800, 1200)
            else:
                base_demand = random.randint(300, 700)
            
            # Adjust for day of week
            if is_weekend:
                base_demand = int(base_demand * 1.2)
            
            # Adjust for holidays
            if is_holiday:
                base_demand = int(base_demand * 0.7)
            
            # Weather impact
            weather = random.choice(weather_conditions)
            if weather == 'Rainy':
                base_demand = int(base_demand * 1.1)
            elif weather == 'Stormy':
                base_demand = int(base_demand * 0.6)
            
            # Special events
            event = random.choices(special_events, weights=[0.85, 0.05, 0.05, 0.03, 0.02])[0]
            if event:
                base_demand = int(base_demand * 1.5)
            
            for line in lines:
                data['date'].append(current_date)
                data['time_slot'].append(time_slot)
                data['passenger_count'].append(base_demand + random.randint(-100, 100))
                data['line'].append(line)
                data['weather_condition'].append(weather)
                data['day_of_week'].append(day_of_week)
                data['is_holiday'].append(is_holiday)
                data['special_event'].append(event)
    
    df = pd.DataFrame(data)
    df.to_csv('passenger_demand_data.csv', index=False)
    return df

def create_energy_consumption_csv():
    """Create energy consumption data for sustainability analysis"""
    n_months = 24
    
    data = {
        'month': [],
        'year': [],
        'energy_consumption_kwh': [],
        'distance_traveled_km': [],
        'passengers_carried': [],
        'energy_per_km': [],
        'energy_per_passenger': [],
        'renewable_percentage': [],
        'cost_per_kwh': [],
        'maintenance_impact': []
    }
    
    current_date = datetime.now()
    
    for i in range(n_months):
        month = (current_date.month - i - 1) % 12 + 1
        year = current_date.year - ((current_date.month - i - 1) // 12)
        
        # Seasonal variations
        if month in [6, 7, 8, 9]:  # Monsoon months
            energy_base = random.randint(120000, 150000)
            maintenance_impact = random.uniform(1.1, 1.3)
        elif month in [3, 4, 5]:  # Summer months
            energy_base = random.randint(140000, 170000)
            maintenance_impact = random.uniform(1.0, 1.2)
        else:
            energy_base = random.randint(100000, 130000)
            maintenance_impact = random.uniform(0.9, 1.1)
        
        distance = random.randint(80000, 120000)
        passengers = random.randint(2000000, 3000000)
        
        data['month'].append(month)
        data['year'].append(year)
        data['energy_consumption_kwh'].append(energy_base)
        data['distance_traveled_km'].append(distance)
        data['passengers_carried'].append(passengers)
        data['energy_per_km'].append(energy_base / distance)
        data['energy_per_passenger'].append(energy_base / passengers)
        data['renewable_percentage'].append(random.uniform(0.2, 0.4))
        data['cost_per_kwh'].append(random.uniform(6.5, 8.5))
        data['maintenance_impact'].append(maintenance_impact)
    
    df = pd.DataFrame(data)
    df.to_csv('energy_consumption.csv', index=False)
    return df

def create_advertisement_performance_csv():
    """Create advertisement performance data for revenue optimization"""
    n_campaigns = 200
    
    data = {
        'campaign_id': [],
        'advertiser': [],
        'category': [],
        'subcategory': [],
        'duration_days': [],
        'investment': [],
        'impressions': [],
        'engagement_rate': [],
        'revenue_generated': [],
        'roi': [],
        'target_demographic': [],
        'peak_hour_performance': [],
        'compartment_type': []
    }
    
    advertisers = ['Coca-Cola', 'Pepsi', 'Amazon', 'Google', 'Microsoft', 'Apple', 
                  'Samsung', 'Toyota', 'Flipkart', 'BSNL', 'Airtel', 'Jio']
    categories = ['FMCG', 'Technology', 'Automotive', 'Telecom', 'E-commerce', 'Finance']
    subcategories = {
        'FMCG': ['Beverages', 'Snacks', 'Personal Care'],
        'Technology': ['Electronics', 'Software', 'Gadgets'],
        'Automotive': ['Cars', 'Bikes', 'Accessories'],
        'Telecom': ['Mobile', 'Broadband', 'DTH'],
        'E-commerce': ['Shopping', 'Food Delivery', 'Travel'],
        'Finance': ['Banking', 'Insurance', 'Investments']
    }
    demographics = ['Youth', 'Family', 'Professionals', 'Students', 'Senior Citizens']
    compartments = ['Standard', 'Women', 'Premium', 'Accessible']
    
    for i in range(1, n_campaigns + 1):
        category = random.choice(categories)
        subcategory = random.choice(subcategories[category])
        advertiser = random.choice(advertisers)
        
        duration = random.randint(7, 90)
        investment = random.randint(50000, 500000)
        
        # Performance metrics with some correlation to investment
        impressions = investment * random.uniform(0.8, 1.2)
        engagement = random.uniform(0.02, 0.08)
        revenue = investment * random.uniform(0.8, 1.5)
        roi = (revenue - investment) / investment
        
        data['campaign_id'].append(f"AD-{i:04d}")
        data['advertiser'].append(advertiser)
        data['category'].append(category)
        data['subcategory'].append(subcategory)
        data['duration_days'].append(duration)
        data['investment'].append(investment)
        data['impressions'].append(impressions)
        data['engagement_rate'].append(engagement)
        data['revenue_generated'].append(revenue)
        data['roi'].append(roi)
        data['target_demographic'].append(random.choice(demographics))
        data['peak_hour_performance'].append(random.uniform(1.2, 1.8))
        data['compartment_type'].append(random.choice(compartments))
    
    df = pd.DataFrame(data)
    df.to_csv('advertisement_performance.csv', index=False)
    return df

def create_metro_stations_csv():
    """Create metro stations data with coordinates and amenities"""
    stations = {
        'station_id': [],
        'station_name': [],
        'latitude': [],
        'longitude': [],
        'line': [],
        'platforms': [],
        'elevators': [],
        'escalators': [],
        'parking_capacity': [],
        'daily_passengers': [],
        'commercial_spaces': [],
        'accessibility_score': []
    }
    
    station_data = [
        # Aluva-Kakkanad Line
        {"name": "Aluva", "lat": 10.1096, "lon": 76.3516, "line": "Aluva-Kakkanad"},
        {"name": "Pulinchodu", "lat": 10.09503, "lon": 76.34658, "line": "Aluva-Kakkanad"},
        {"name": "Companypady", "lat": 10.087293, "lon": 76.34284, "line": "Aluva-Kakkanad"},
        {"name": "Ambattukavu", "lat": 10.079372, "lon": 76.339004, "line": "Aluva-Kakkanad"},
        {"name": "Muttom", "lat": 10.072701, "lon": 76.33375, "line": "Aluva-Kakkanad"},
        {"name": "Kalamassery", "lat": 10.0481, "lon": 76.3097, "line": "Aluva-Kakkanad"},
        {"name": "CUSAT", "lat": 10.046879, "lon": 76.318377, "line": "Aluva-Kakkanad"},
        {"name": "Pathadipalam", "lat": 10.035948, "lon": 76.314371, "line": "Aluva-Kakkanad"},
        {"name": "Edapally", "lat": 10.0274, "lon": 76.3080, "line": "Aluva-Kakkanad"},
        {"name": "Changampuzha Park", "lat": 10.01488, "lon": 76.30232, "line": "Aluva-Kakkanad"},
        {"name": "Palarivattom", "lat": 9.998480, "lon": 76.311935, "line": "Aluva-Kakkanad"},
        {"name": "JLN Stadium", "lat": 9.9973, "lon": 76.3010, "line": "Aluva-Kakkanad"},
        {"name": "Kaloor", "lat": 9.99709, "lon": 76.302815, "line": "Aluva-Kakkanad"},
        {"name": "Lissie", "lat": 9.991247, "lon": 76.288035, "line": "Aluva-Kakkanad"},
        {"name": "MG Road", "lat": 9.971295, "lon": 76.299317, "line": "Aluva-Kakkanad"},
        {"name": "Maharaja's College", "lat": 9.973487, "lon": 76.285015, "line": "Aluva-Kakkanad"},
        {"name": "Ernakulam South", "lat": 9.9630, "lon": 76.3126, "line": "Aluva-Kakkanad"},
        {"name": "Kadavanthra", "lat": 9.9580, "lon": 76.3080, "line": "Aluva-Kakkanad"},
        {"name": "Elamkulam", "lat": 9.9520, "lon": 76.3050, "line": "Aluva-Kakkanad"},
        {"name": "Vytilla", "lat": 9.9630, "lon": 76.3126, "line": "Aluva-Kakkanad"},
        {"name": "Thaikoodam", "lat": 9.9550, "lon": 76.3200, "line": "Aluva-Kakkanad"},
        {"name": "Petta", "lat": 9.9500, "lon": 76.3250, "line": "Aluva-Kakkanad"},
        {"name": "Vadakkekotta", "lat": 9.9450, "lon": 76.3300, "line": "Aluva-Kakkanad"},
        {"name": "SN Junction", "lat": 9.9400, "lon": 76.3350, "line": "Aluva-Kakkanad"},
        {"name": "Kakkanad", "lat": 9.9350, "lon": 76.3400, "line": "Aluva-Kakkanad"},
        
        # Thrippunithura-Vytilla Line
        {"name": "Thrippunithura", "lat": 9.9450, "lon": 76.3500, "line": "Thrippunithura-Vytilla"},
        {"name": "Vadakkekotta", "lat": 9.9450, "lon": 76.3300, "line": "Thrippunithura-Vytilla"},
        {"name": "Petta", "lat": 9.9500, "lon": 76.3250, "line": "Thrippunithura-Vytilla"},
        {"name": "SN Junction", "lat": 9.9400, "lon": 76.3350, "line": "Thrippunithura-Vytilla"},
        {"name": "Kakkanad", "lat": 9.9350, "lon": 76.3400, "line": "Thrippunithura-Vytilla"},
        {"name": "Kalamassery", "lat": 10.0481, "lon": 76.3097, "line": "Thrippunithura-Vytilla"},
    ]
    
    for i, station in enumerate(station_data, 1):
        stations['station_id'].append(f"STN-{i:03d}")
        stations['station_name'].append(station['name'])
        stations['latitude'].append(station['lat'])
        stations['longitude'].append(station['lon'])
        stations['line'].append(station['line'])
        stations['platforms'].append(random.randint(2, 4))
        stations['elevators'].append(random.randint(1, 3))
        stations['escalators'].append(random.randint(2, 6))
        stations['parking_capacity'].append(random.randint(50, 300))
        stations['daily_passengers'].append(random.randint(5000, 25000))
        stations['commercial_spaces'].append(random.randint(5, 20))
        stations['accessibility_score'].append(random.uniform(0.7, 0.95))
    
    df = pd.DataFrame(stations)
    df.to_csv('metro_stations.csv', index=False)
    return df

def create_all_csv_files():
    """Create all CSV files and return download links"""
    print("Creating comprehensive CSV files for KMRL AI system...")
    
    files_created = {}
    
    # Create all datasets
    files_created['trainsets'] = create_trainsets_csv()
    files_created['maintenance'] = create_historical_maintenance_csv()
    files_created['passenger_demand'] = create_passenger_demand_csv()
    files_created['energy'] = create_energy_consumption_csv()
    files_created['advertisement'] = create_advertisement_performance_csv()
    files_created['stations'] = create_metro_stations_csv()
    
    print("All CSV files created successfully!")
    print("\nFiles created:")
    for file_name in files_created.keys():
        print(f"✓ {file_name}_ml_ready.csv")
    
    return files_created

# Create the CSV files
if __name__ == "__main__":
    create_all_csv_files()