#!/usr/bin/env python3
"""
Mock Train Tracking Data Generator
Creates comprehensive CSV data for train tracking testing
"""

from common_imports import *
import csv
from datetime import datetime, timedelta
import random

def generate_mock_train_tracking_data():
    """Generate comprehensive mock train tracking data"""
    
    # Station coordinates for Kochi Metro
    stations = {
        "Aluva": (10.1076, 76.3516),
        "Pulinchodu": (10.1023, 76.3589),
        "Companypady": (10.0967, 76.3662),
        "Ambattukavu": (10.0911, 76.3735),
        "Muttom": (10.0855, 76.3808),
        "Kalamassery": (10.0799, 76.3881),
        "CUSAT": (10.0743, 76.3954),
        "Pathadipalam": (10.0687, 76.4027),
        "Edapally": (10.0631, 76.4100),
        "Changampuzha Park": (10.0575, 76.4173),
        "Palarivattom": (10.0519, 76.4246),
        "JLN Stadium": (10.0463, 76.4319),
        "Kaloor": (10.0407, 76.4392),
        "Lissie": (10.0351, 76.4465),
        "MG Road": (10.0295, 76.4538),
        "Maharaja's College": (10.0239, 76.4611),
        "Ernakulam South": (10.0183, 76.4684),
        "Kadavanthra": (10.0127, 76.4757),
        "Elamkulam": (10.0071, 76.4830),
        "Vytilla": (10.0015, 76.4903),
        "Thaikoodam": (9.9959, 76.4976),
        "Petta": (9.9903, 76.5049),
        "Vadakkekotta": (9.9847, 76.5122),
        "SN Junction": (9.9791, 76.5195),
        "Kakkanad": (9.9735, 76.5268),
        "Thrippunithura": (9.9450, 76.3500)
    }
    
    # Routes
    routes = {
        "Aluva-Kakkanad": ["Aluva", "Pulinchodu", "Companypady", "Ambattukavu", "Muttom", 
                           "Kalamassery", "CUSAT", "Pathadipalam", "Edapally", "Changampuzha Park", 
                           "Palarivattom", "JLN Stadium", "Kaloor", "Lissie", "MG Road", 
                           "Maharaja's College", "Ernakulam South", "Kadavanthra", "Elamkulam", 
                           "Vytilla", "Thaikoodam", "Petta", "Vadakkekotta", "SN Junction", "Kakkanad"],
        "Thrippunithura-Vytilla": ["Thrippunithura", "Vadakkekotta", "Petta", "SN Junction", "Kakkanad", "Kalamassery"]
    }
    
    # Train statuses
    statuses = ["stationary", "moving", "arriving", "departing", "delayed", "maintenance"]
    
    # Generate data for multiple time periods
    data = []
    base_time = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    
    # Generate data for 24 hours (every 5 minutes)
    for hour in range(24):
        for minute in range(0, 60, 5):  # Every 5 minutes
            current_time = base_time + timedelta(hours=hour, minutes=minute)
            
            # Generate 8-15 trains per time slot
            num_trains = random.randint(8, 15)
            
            for train_num in range(num_trains):
                # Select route
                route = random.choice(list(routes.keys()))
                route_stations = routes[route]
                
                # Select current and next station
                if route == "Aluva-Kakkanad":
                    current_idx = random.randint(0, len(route_stations)-2)
                else:
                    current_idx = random.randint(0, len(route_stations)-2)
                
                current_station = route_stations[current_idx]
                next_station = route_stations[min(current_idx + 1, len(route_stations)-1)]
                
                # Get coordinates
                current_coords = stations[current_station]
                next_coords = stations[next_station]
                
                # Add some randomness to position
                lat_offset = random.uniform(-0.001, 0.001)
                lon_offset = random.uniform(-0.001, 0.001)
                
                # Determine status based on time
                if minute % 30 < 5:  # Arriving
                    status = "arriving"
                    speed = random.uniform(5, 15)
                elif minute % 30 < 10:  # Stationary
                    status = "stationary"
                    speed = 0
                elif minute % 30 < 15:  # Departing
                    status = "departing"
                    speed = random.uniform(5, 15)
                else:  # Moving
                    status = "moving"
                    speed = random.uniform(25, 35)
                
                # Add some delays
                delay_minutes = random.randint(0, 10) if random.random() < 0.1 else 0
                if delay_minutes > 5:
                    status = "delayed"
                
                # Passenger count
                capacity = random.choice([250, 300, 350])
                passenger_count = random.randint(int(capacity*0.3), int(capacity*0.95))
                
                # Direction
                direction = "forward" if random.random() < 0.7 else "reverse"
                
                # Create record
                record = {
                    'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'trainset_id': f'TRAIN_{train_num+1:03d}',
                    'current_station': current_station,
                    'next_station': next_station,
                    'route': route,
                    'status': status,
                    'position_lat': round(current_coords[0] + lat_offset, 6),
                    'position_lon': round(current_coords[1] + lon_offset, 6),
                    'speed_kmh': round(speed, 1),
                    'direction': direction,
                    'delay_minutes': delay_minutes,
                    'passenger_count': passenger_count,
                    'capacity': capacity,
                    'utilization_percent': round((passenger_count / capacity) * 100, 1),
                    'estimated_arrival': (current_time + timedelta(minutes=random.randint(2, 8))).strftime('%H:%M:%S'),
                    'estimated_departure': (current_time + timedelta(minutes=random.randint(5, 12))).strftime('%H:%M:%S'),
                    'depot': random.choice(['Aluva Depot', 'Petta Depot']),
                    'ai_score': round(random.uniform(75, 95), 1),
                    'reliability_score': round(random.uniform(80, 98), 1),
                    'maintenance_due': random.choice(['No', 'Due in 7 days', 'Due in 3 days', 'Overdue']),
                    'weather_condition': random.choice(['Clear', 'Clouds', 'Rain', 'Thunderstorm']),
                    'temperature_c': round(random.uniform(22, 35), 1),
                    'humidity_percent': round(random.uniform(60, 90), 1)
                }
                
                data.append(record)
    
    return data

def save_to_csv(data, filename='mock_train_tracking_data.csv'):
    """Save data to CSV file"""
    
    if not data:
        print("No data to save")
        return
    
    # Get fieldnames from first record
    fieldnames = list(data[0].keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    print(f"✅ Mock train tracking data saved to {filename}")
    print(f"📊 Total records: {len(data)}")
    print(f"📅 Time range: {data[0]['timestamp']} to {data[-1]['timestamp']}")
    print(f"🚆 Unique trains: {len(set(record['trainset_id'] for record in data))}")

def create_sample_data():
    """Create a smaller sample dataset for quick testing"""
    
    stations = {
        "Aluva": (10.1076, 76.3516),
        "Kalamassery": (10.0799, 76.3881),
        "Edapally": (10.0631, 76.4100),
        "MG Road": (10.0295, 76.4538),
        "Vytilla": (10.0015, 76.4903),
        "Kakkanad": (9.9735, 76.5268)
    }
    
    routes = {
        "Aluva-Kakkanad": ["Aluva", "Kalamassery", "Edapally", "MG Road", "Vytilla", "Kakkanad"]
    }
    
    data = []
    base_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    # Generate 2 hours of data (every 10 minutes)
    for hour in range(2):
        for minute in range(0, 60, 10):
            current_time = base_time + timedelta(hours=hour, minutes=minute)
            
            # Generate 5 trains per time slot
            for train_num in range(5):
                route = "Aluva-Kakkanad"
                route_stations = routes[route]
                
                current_idx = random.randint(0, len(route_stations)-2)
                current_station = route_stations[current_idx]
                next_station = route_stations[min(current_idx + 1, len(route_stations)-1)]
                
                current_coords = stations[current_station]
                
                lat_offset = random.uniform(-0.001, 0.001)
                lon_offset = random.uniform(-0.001, 0.001)
                
                status = random.choice(["stationary", "moving", "arriving", "departing"])
                speed = random.uniform(0, 35) if status == "moving" else random.uniform(0, 15)
                
                capacity = 300
                passenger_count = random.randint(50, capacity)
                
                record = {
                    'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'trainset_id': f'TRAIN_{train_num+1:03d}',
                    'current_station': current_station,
                    'next_station': next_station,
                    'route': route,
                    'status': status,
                    'position_lat': round(current_coords[0] + lat_offset, 6),
                    'position_lon': round(current_coords[1] + lon_offset, 6),
                    'speed_kmh': round(speed, 1),
                    'direction': random.choice(['forward', 'reverse']),
                    'delay_minutes': random.randint(0, 5),
                    'passenger_count': passenger_count,
                    'capacity': capacity,
                    'utilization_percent': round((passenger_count / capacity) * 100, 1),
                    'estimated_arrival': (current_time + timedelta(minutes=random.randint(2, 8))).strftime('%H:%M:%S'),
                    'estimated_departure': (current_time + timedelta(minutes=random.randint(5, 12))).strftime('%H:%M:%S'),
                    'depot': random.choice(['Aluva Depot', 'Petta Depot']),
                    'ai_score': round(random.uniform(75, 95), 1),
                    'reliability_score': round(random.uniform(80, 98), 1),
                    'maintenance_due': random.choice(['No', 'Due in 7 days', 'Due in 3 days']),
                    'weather_condition': random.choice(['Clear', 'Clouds', 'Rain']),
                    'temperature_c': round(random.uniform(25, 32), 1),
                    'humidity_percent': round(random.uniform(70, 85), 1)
                }
                
                data.append(record)
    
    return data

if __name__ == "__main__":
    print("🚆 Mock Train Tracking Data Generator")
    print("=" * 50)
    
    # Ask user for data size preference
    print("Choose data size:")
    print("1. Full dataset (24 hours, ~17,000 records)")
    print("2. Sample dataset (2 hours, ~60 records)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        print("📊 Generating full dataset...")
        data = generate_mock_train_tracking_data()
        filename = 'mock_train_tracking_data_full.csv'
    else:
        print("📊 Generating sample dataset...")
        data = create_sample_data()
        filename = 'mock_train_tracking_data_sample.csv'
    
    # Save to CSV
    save_to_csv(data, filename)
    
    # Show sample records
    print(f"\n📋 Sample records from {filename}:")
    for i, record in enumerate(data[:3]):
        print(f"\nRecord {i+1}:")
        for key, value in record.items():
            print(f"  {key}: {value}")
    
    print(f"\n🎉 Mock data generation complete!")
    print(f"📁 File saved as: {filename}")
    print(f"📊 Use this data to test your train tracking platform!")
