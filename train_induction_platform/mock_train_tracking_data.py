from common_imports import *
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

class MockTrainTrackingDataGenerator:
    """Generates comprehensive mock data for train tracking system"""
    
    def __init__(self):
        self.stations = self._get_station_data()
        self.routes = self._get_route_data()
        self.trainsets = self._get_trainset_data()
        
    def _get_station_data(self) -> List[Dict]:
        """Get station information with coordinates and passenger data"""
        return [
            {"station_id": "STN-001", "station_name": "Aluva", "lat": 10.1076, "lon": 76.3516, 
             "daily_passengers": 16727, "platforms": 2, "elevation": 10.5},
            {"station_id": "STN-002", "station_name": "Pulinchodu", "lat": 10.1023, "lon": 76.3589, 
             "daily_passengers": 22102, "platforms": 2, "elevation": 12.3},
            {"station_id": "STN-003", "station_name": "Companypady", "lat": 10.0967, "lon": 76.3662, 
             "daily_passengers": 12757, "platforms": 2, "elevation": 15.7},
            {"station_id": "STN-004", "station_name": "Ambattukavu", "lat": 10.0911, "lon": 76.3735, 
             "daily_passengers": 24739, "platforms": 2, "elevation": 18.2},
            {"station_id": "STN-005", "station_name": "Muttom", "lat": 10.0855, "lon": 76.3808, 
             "daily_passengers": 21038, "platforms": 2, "elevation": 20.1},
            {"station_id": "STN-006", "station_name": "Kalamassery", "lat": 10.0799, "lon": 76.3881, 
             "daily_passengers": 18543, "platforms": 2, "elevation": 22.5},
            {"station_id": "STN-007", "station_name": "CUSAT", "lat": 10.0743, "lon": 76.3954, 
             "daily_passengers": 15234, "platforms": 2, "elevation": 25.3},
            {"station_id": "STN-008", "station_name": "Pathadipalam", "lat": 10.0687, "lon": 76.4027, 
             "daily_passengers": 19876, "platforms": 2, "elevation": 28.7},
            {"station_id": "STN-009", "station_name": "Edapally", "lat": 10.0631, "lon": 76.4100, 
             "daily_passengers": 22345, "platforms": 2, "elevation": 31.2},
            {"station_id": "STN-010", "station_name": "Changampuzha Park", "lat": 10.0575, "lon": 76.4173, 
             "daily_passengers": 18765, "platforms": 2, "elevation": 33.8},
            {"station_id": "STN-011", "station_name": "Palarivattom", "lat": 10.0519, "lon": 76.4246, 
             "daily_passengers": 25678, "platforms": 2, "elevation": 36.4},
            {"station_id": "STN-012", "station_name": "JLN Stadium", "lat": 10.0463, "lon": 76.4319, 
             "daily_passengers": 21345, "platforms": 2, "elevation": 39.1},
            {"station_id": "STN-013", "station_name": "Kaloor", "lat": 10.0407, "lon": 76.4392, 
             "daily_passengers": 28765, "platforms": 2, "elevation": 41.7},
            {"station_id": "STN-014", "station_name": "Lissie", "lat": 10.0351, "lon": 76.4465, 
             "daily_passengers": 19876, "platforms": 2, "elevation": 44.3},
            {"station_id": "STN-015", "station_name": "MG Road", "lat": 10.0295, "lon": 76.4538, 
             "daily_passengers": 34567, "platforms": 2, "elevation": 46.9},
            {"station_id": "STN-016", "station_name": "Maharaja's College", "lat": 10.0239, "lon": 76.4611, 
             "daily_passengers": 18765, "platforms": 2, "elevation": 49.5},
            {"station_id": "STN-017", "station_name": "Ernakulam South", "lat": 10.0183, "lon": 76.4684, 
             "daily_passengers": 29876, "platforms": 2, "elevation": 52.1},
            {"station_id": "STN-018", "station_name": "Kadavanthra", "lat": 10.0127, "lon": 76.4757, 
             "daily_passengers": 22345, "platforms": 2, "elevation": 54.7},
            {"station_id": "STN-019", "station_name": "Elamkulam", "lat": 10.0071, "lon": 76.4830, 
             "daily_passengers": 19876, "platforms": 2, "elevation": 57.3},
            {"station_id": "STN-020", "station_name": "Vytilla", "lat": 10.0015, "lon": 76.4903, 
             "daily_passengers": 31234, "platforms": 2, "elevation": 59.9},
            {"station_id": "STN-021", "station_name": "Thaikoodam", "lat": 9.9959, "lon": 76.4976, 
             "daily_passengers": 18765, "platforms": 2, "elevation": 62.5},
            {"station_id": "STN-022", "station_name": "Petta", "lat": 9.9903, "lon": 76.5049, 
             "daily_passengers": 25678, "platforms": 2, "elevation": 65.1},
            {"station_id": "STN-023", "station_name": "Vadakkekotta", "lat": 9.9847, "lon": 76.5122, 
             "daily_passengers": 19876, "platforms": 2, "elevation": 67.7},
            {"station_id": "STN-024", "station_name": "SN Junction", "lat": 9.9791, "lon": 76.5195, 
             "daily_passengers": 22345, "platforms": 2, "elevation": 70.3},
            {"station_id": "STN-025", "station_name": "Kakkanad", "lat": 9.9735, "lon": 76.5268, 
             "daily_passengers": 28765, "platforms": 2, "elevation": 72.9},
            {"station_id": "STN-026", "station_name": "Thrippunithura", "lat": 9.9450, "lon": 76.3500, 
             "daily_passengers": 19876, "platforms": 2, "elevation": 15.2}
        ]
    
    def _get_route_data(self) -> List[Dict]:
        """Get route information"""
        return [
            {
                "route_id": "RT-001",
                "route_name": "Aluva-Kakkanad",
                "stations": ["Aluva", "Pulinchodu", "Companypady", "Ambattukavu", "Muttom", 
                           "Kalamassery", "CUSAT", "Pathadipalam", "Edapally", "Changampuzha Park",
                           "Palarivattom", "JLN Stadium", "Kaloor", "Lissie", "MG Road",
                           "Maharaja's College", "Ernakulam South", "Kadavanthra", "Elamkulam",
                           "Vytilla", "Thaikoodam", "Petta", "Vadakkekotta", "SN Junction", "Kakkanad"],
                "total_distance_km": 25.2,
                "average_travel_time_minutes": 45,
                "peak_frequency_minutes": 4,
                "off_peak_frequency_minutes": 8
            },
            {
                "route_id": "RT-002", 
                "route_name": "Thrippunithura-Vytilla",
                "stations": ["Thrippunithura", "Vadakkekotta", "Petta", "SN Junction", "Kakkanad", "Kalamassery"],
                "total_distance_km": 12.8,
                "average_travel_time_minutes": 25,
                "peak_frequency_minutes": 6,
                "off_peak_frequency_minutes": 12
            }
        ]
    
    def _get_trainset_data(self) -> List[Dict]:
        """Get trainset information"""
        return [
            {
                "trainset_id": "KMRL-001",
                "depot": "Aluva Depot",
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom",
                "year_manufactured": 2017,
                "last_maintenance": "2024-01-15",
                "next_maintenance": "2024-04-15",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            },
            {
                "trainset_id": "KMRL-002", 
                "depot": "Aluva Depot",
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom",
                "year_manufactured": 2017,
                "last_maintenance": "2024-01-20",
                "next_maintenance": "2024-04-20",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            },
            {
                "trainset_id": "KMRL-003",
                "depot": "Muttom Depot", 
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom",
                "year_manufactured": 2018,
                "last_maintenance": "2024-02-01",
                "next_maintenance": "2024-05-01",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            },
            {
                "trainset_id": "KMRL-004",
                "depot": "Muttom Depot",
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom", 
                "year_manufactured": 2018,
                "last_maintenance": "2024-02-10",
                "next_maintenance": "2024-05-10",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            },
            {
                "trainset_id": "KMRL-005",
                "depot": "Petta Depot",
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom",
                "year_manufactured": 2019,
                "last_maintenance": "2024-02-15",
                "next_maintenance": "2024-05-15",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            },
            {
                "trainset_id": "KMRL-006",
                "depot": "Petta Depot",
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom",
                "year_manufactured": 2019,
                "last_maintenance": "2024-02-20",
                "next_maintenance": "2024-05-20",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            },
            {
                "trainset_id": "KMRL-007",
                "depot": "Aluva Depot",
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom",
                "year_manufactured": 2020,
                "last_maintenance": "2024-03-01",
                "next_maintenance": "2024-06-01",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            },
            {
                "trainset_id": "KMRL-008",
                "depot": "Muttom Depot",
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom",
                "year_manufactured": 2020,
                "last_maintenance": "2024-03-05",
                "next_maintenance": "2024-06-05",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            },
            {
                "trainset_id": "KMRL-009",
                "depot": "Petta Depot",
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom",
                "year_manufactured": 2021,
                "last_maintenance": "2024-03-10",
                "next_maintenance": "2024-06-10",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            },
            {
                "trainset_id": "KMRL-010",
                "depot": "Aluva Depot",
                "capacity": 300,
                "max_speed_kmh": 80,
                "manufacturer": "Alstom",
                "year_manufactured": 2021,
                "last_maintenance": "2024-03-15",
                "next_maintenance": "2024-06-15",
                "fitness_certificate_valid": True,
                "operational_status": "Available"
            }
        ]
    
    def generate_timetable_data(self) -> List[Dict]:
        """Generate comprehensive timetable data"""
        timetable = []
        start_time = datetime.now().replace(hour=5, minute=0, second=0, microsecond=0)
        
        # Generate 30-minute slots from 5:00 AM to 11:30 PM
        for slot_num in range(37):  # 5:00 AM to 11:30 PM = 18.5 hours = 37 slots
            slot_start = start_time + timedelta(minutes=30 * slot_num)
            slot_end = slot_start + timedelta(minutes=30)
            time_slot = f"{slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"
            
            # Determine if peak hour
            hour = slot_start.hour
            is_peak = (7 <= hour <= 9) or (17 <= hour <= 19)
            
            # Generate trains for this slot
            trains = self._generate_trains_for_slot(slot_start, is_peak)
            
            # Calculate demand based on time and weather
            demand_level = self._calculate_demand_level(hour, is_peak)
            
            timetable.append({
                "time_slot": time_slot,
                "slot_start": slot_start.isoformat(),
                "slot_end": slot_end.isoformat(),
                "total_trains": len(trains),
                "trains": trains,
                "peak_hour": is_peak,
                "demand_level": demand_level,
                "weather_condition": random.choice(["Clear", "Cloudy", "Light Rain", "Sunny"]),
                "temperature": random.randint(22, 35),
                "humidity": random.randint(60, 90),
                "total_capacity": sum(train.get('capacity', 300) for train in trains),
                "predicted_demand": random.randint(800, 2500) if is_peak else random.randint(400, 1200)
            })
        
        return timetable
    
    def _generate_trains_for_slot(self, slot_time: datetime, is_peak: bool) -> List[Dict]:
        """Generate trains for a specific time slot"""
        trains = []
        
        # Determine number of trains based on peak/off-peak
        if is_peak:
            num_trains = random.randint(8, 12)
        else:
            num_trains = random.randint(4, 8)
        
        # Select trains from available trainsets
        available_trainsets = random.sample(self.trainsets, min(num_trains, len(self.trainsets)))
        
        for trainset in available_trainsets:
            # Determine route based on depot
            depot = trainset['depot']
            if 'Aluva' in depot:
                route = 'Aluva-Kakkanad'
            elif 'Petta' in depot:
                route = 'Thrippunithura-Vytilla'
            else:
                route = 'Aluva-Kakkanad'
            
            # Generate train data
            train_data = {
                "trainset_id": trainset['trainset_id'],
                "route": route,
                "depot": trainset['depot'],
                "capacity": trainset['capacity'],
                "max_speed": trainset['max_speed_kmh'],
                "manufacturer": trainset['manufacturer'],
                "year_manufactured": trainset['year_manufactured'],
                "operational_status": trainset['operational_status'],
                "fitness_valid": trainset['fitness_certificate_valid'],
                "ai_score": random.randint(75, 95),
                "delay_minutes": random.randint(0, 5),
                "passenger_count": random.randint(50, trainset['capacity']),
                "energy_efficiency": random.uniform(0.8, 1.0),
                "maintenance_score": random.randint(80, 100),
                "reliability_score": random.randint(85, 98)
            }
            
            trains.append(train_data)
        
        return trains
    
    def _calculate_demand_level(self, hour: int, is_peak: bool) -> str:
        """Calculate demand level based on time"""
        if is_peak:
            return random.choice(["High", "Very High"])
        elif 10 <= hour <= 16:
            return "Medium"
        else:
            return "Low"
    
    def generate_real_time_tracking_data(self, timetable: List[Dict]) -> List[Dict]:
        """Generate real-time tracking data based on timetable"""
        tracking_data = []
        current_time = datetime.now()
        
        for slot in timetable:
            slot_start = datetime.fromisoformat(slot['slot_start'])
            
            # Only generate tracking for current and future slots
            if slot_start <= current_time <= datetime.fromisoformat(slot['slot_end']):
                for train in slot['trains']:
                    # Generate current position data
                    position_data = self._generate_train_position(train, slot_start)
                    tracking_data.append(position_data)
        
        return tracking_data
    
    def _generate_train_position(self, train: Dict, slot_time: datetime) -> Dict:
        """Generate position data for a specific train"""
        route_stations = self._get_route_stations(train['route'])
        
        # Determine current station (simulate movement)
        current_station_idx = random.randint(0, len(route_stations) - 1)
        current_station = route_stations[current_station_idx]
        
        # Get station coordinates
        station_data = next((s for s in self.stations if s['station_name'] == current_station), None)
        
        if station_data:
            # Add small random offset to simulate position within station
            lat = station_data['lat'] + random.uniform(-0.001, 0.001)
            lon = station_data['lon'] + random.uniform(-0.001, 0.001)
        else:
            lat, lon = 10.0, 76.0  # Default coordinates
        
        # Determine next station
        next_station_idx = (current_station_idx + 1) % len(route_stations)
        next_station = route_stations[next_station_idx]
        
        # Generate status
        status_options = ["stationary", "moving", "arriving", "departing"]
        status = random.choice(status_options)
        
        # Calculate speed based on status
        speed = random.uniform(25, 35) if status == "moving" else 0.0
        
        return {
            "trainset_id": train['trainset_id'],
            "current_station": current_station,
            "next_station": next_station,
            "route": train['route'],
            "status": status,
            "position_lat": lat,
            "position_lon": lon,
            "speed": speed,
            "direction": "forward",
            "delay_minutes": random.randint(0, 5),
            "passenger_count": random.randint(50, train['capacity']),
            "capacity": train['capacity'],
            "last_update": datetime.now().isoformat(),
            "estimated_arrival": (datetime.now() + timedelta(minutes=random.randint(2, 8))).isoformat(),
            "estimated_departure": (datetime.now() + timedelta(minutes=random.randint(5, 12))).isoformat()
        }
    
    def _get_route_stations(self, route_name: str) -> List[str]:
        """Get stations for a specific route"""
        route_data = next((r for r in self.routes if r['route_name'] == route_name), None)
        return route_data['stations'] if route_data else []
    
    def save_to_csv(self, data: List[Dict], filename: str) -> None:
        """Save data to CSV file"""
        if not data:
            return
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"✅ Data saved to {filename}")

def generate_timetable_data() -> List[Dict]:
    """Generate timetable data for the application"""
    generator = MockTrainTrackingDataGenerator()
    return generator.generate_timetable_data()

def generate_tracking_data() -> List[Dict]:
    """Generate real-time tracking data"""
    generator = MockTrainTrackingDataGenerator()
    timetable = generator.generate_timetable_data()
    return generator.generate_real_time_tracking_data(timetable)

if __name__ == "__main__":
    # Generate and save all mock data
    generator = MockTrainTrackingDataGenerator()
    
    # Generate timetable data
    timetable_data = generator.generate_timetable_data()
    generator.save_to_csv(timetable_data, "mock_timetable_data.csv")
    
    # Generate tracking data
    tracking_data = generator.generate_real_time_tracking_data(timetable_data)
    generator.save_to_csv(tracking_data, "mock_tracking_data.csv")
    
    # Generate station data
    generator.save_to_csv(generator.stations, "mock_station_data.csv")
    
    # Generate route data
    generator.save_to_csv(generator.routes, "mock_route_data.csv")
    
    # Generate trainset data
    generator.save_to_csv(generator.trainsets, "mock_trainset_data.csv")
    
    print("🎉 All mock data files generated successfully!")
