from common_imports import *
import folium
from folium import plugins
import threading
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from ibm_maximo_integration import IBMMaximoIntegration, MaximoDataAdapter

class TrainStatus(Enum):
    """Train status enumeration"""
    STATIONARY = "stationary"
    MOVING = "moving"
    ARRIVING = "arriving"
    DEPARTING = "departing"
    DELAYED = "delayed"
    MAINTENANCE = "maintenance"

@dataclass
class TrainPosition:
    """Represents a train's current position and status"""
    trainset_id: str
    current_station: str
    next_station: str
    route: str
    status: TrainStatus
    position_lat: float
    position_lon: float
    speed: float  # km/h
    direction: str  # "forward" or "reverse"
    delay_minutes: int
    passenger_count: int
    capacity: int
    last_update: datetime
    estimated_arrival: datetime
    estimated_departure: datetime

class TrainTracker:
    """Real-time train tracking system"""
    
    def __init__(self):
        self.trains: Dict[str, TrainPosition] = {}
        self.station_coordinates = self._load_station_coordinates()
        self.route_segments = self._calculate_route_segments()
        self.tracking_active = False
        self.tracking_thread = None
        self.collision_detector = CollisionDetector()
        
        # Initialize IBM Maximo integration
        self.maximo = IBMMaximoIntegration()
        self.maximo_connected = False
        self.maximo_sync_enabled = True
        
    def _load_station_coordinates(self) -> Dict[str, Tuple[float, float]]:
        """Load station coordinates for Kochi Metro"""
        return {
            # Aluva-Kakkanad Line
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
            
            # Thrippunithura-Vytilla Line
            "Thrippunithura": (9.9450, 76.3500),
        }
    
    def _calculate_route_segments(self) -> Dict[str, List[Tuple[str, str]]]:
        """Calculate route segments between stations"""
        aluva_kakkanad = [
            "Aluva", "Pulinchodu", "Companypady", "Ambattukavu", "Muttom", "Kalamassery", 
            "CUSAT", "Pathadipalam", "Edapally", "Changampuzha Park", "Palarivattom", 
            "JLN Stadium", "Kaloor", "Lissie", "MG Road", "Maharaja's College", 
            "Ernakulam South", "Kadavanthra", "Elamkulam", "Vytilla", "Thaikoodam", 
            "Petta", "Vadakkekotta", "SN Junction", "Kakkanad"
        ]
        
        thrippunithura_vytilla = [
            "Thrippunithura", "Vadakkekotta", "Petta", "SN Junction", "Kakkanad", "Kalamassery"
        ]
        
        return {
            "Aluva-Kakkanad": aluva_kakkanad,
            "Thrippunithura-Vytilla": thrippunithura_vytilla
        }
    
    def initialize_trains_from_timetable(self, timetable) -> None:
        """Initialize train positions from timetable data with Maximo integration"""
        self.trains.clear()
        
        # Connect to Maximo if not already connected
        if self.maximo_sync_enabled and not self.maximo_connected:
            self.maximo_connected = self.maximo.connect()
            if self.maximo_connected:
                print("✅ Connected to IBM Maximo for train tracking")
        
        # Handle both list and dictionary formats
        if isinstance(timetable, list):
            # Convert list format to dictionary format for processing
            timetable_dict = {}
            for slot in timetable:
                time_slot = slot.get('time_slot', '06:00-06:30')
                timetable_dict[time_slot] = slot
            timetable = timetable_dict
        
        # Handle timetable as dictionary with time_slot keys
        for time_slot, slot_data in timetable.items():
            slot_start = datetime.strptime(time_slot.split('-')[0], '%H:%M')
            
            # Get trains from the slot data
            trains_in_slot = slot_data.get('trains', [])
            
            for train_data in trains_in_slot:
                trainset_id = train_data['trainset_id']
                route = train_data['route']
                
                # Sync train data with Maximo if connected
                if self.maximo_connected and self.maximo_sync_enabled:
                    self._sync_train_with_maximo(trainset_id, train_data)
                
                # Get route stations
                stations = self.route_segments.get(route, [])
                if not stations:
                    continue
                
                # Determine starting station based on depot
                depot = train_data.get('depot', 'Aluva Depot')
                if 'Aluva' in depot:
                    start_station = stations[0]  # First station
                    direction = "forward"
                else:
                    start_station = stations[-1]  # Last station
                    direction = "reverse"
                
                # Calculate position
                station_coords = self.station_coordinates.get(start_station, (10.0, 76.0))
                
                # Add some randomness to position within station area
                lat_offset = random.uniform(-0.001, 0.001)
                lon_offset = random.uniform(-0.001, 0.001)
                
                train_position = TrainPosition(
                    trainset_id=trainset_id,
                    current_station=start_station,
                    next_station=self._get_next_station(stations, start_station, direction),
                    route=route,
                    status=TrainStatus.STATIONARY,
                    position_lat=station_coords[0] + lat_offset,
                    position_lon=station_coords[1] + lon_offset,
                    speed=0.0,
                    direction=direction,
                    delay_minutes=random.randint(0, 5),
                    passenger_count=random.randint(50, train_data.get('capacity', 300)),
                    capacity=train_data.get('capacity', 300),
                    last_update=datetime.now(),
                    estimated_arrival=slot_start + timedelta(minutes=random.randint(0, 5)),
                    estimated_departure=slot_start + timedelta(minutes=random.randint(2, 8))
                )
                
                self.trains[trainset_id] = train_position
    
    def _get_next_station(self, stations: List[str], current: str, direction: str) -> str:
        """Get next station based on direction"""
        try:
            current_index = stations.index(current)
            if direction == "forward":
                return stations[min(current_index + 1, len(stations) - 1)]
            else:
                return stations[max(current_index - 1, 0)]
        except ValueError:
            return current
    
    def start_tracking(self) -> None:
        """Start real-time train tracking"""
        if self.tracking_active:
            return
        
        self.tracking_active = True
        self.tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
        self.tracking_thread.start()
        print("🚆 Train tracking started")
    
    def stop_tracking(self) -> None:
        """Stop real-time train tracking"""
        self.tracking_active = False
        if self.tracking_thread:
            self.tracking_thread.join()
        print("🛑 Train tracking stopped")
    
    def _tracking_loop(self) -> None:
        """Main tracking loop"""
        while self.tracking_active:
            try:
                self._update_train_positions()
                self._detect_collisions()
                time.sleep(10)  # Update every 10 seconds
            except Exception as e:
                print(f"Tracking error: {e}")
                time.sleep(5)
    
    def _update_train_positions(self) -> None:
        """Update all train positions"""
        for trainset_id, train in self.trains.items():
            self._update_single_train(train)
    
    def _update_single_train(self, train: TrainPosition) -> None:
        """Update a single train's position"""
        current_time = datetime.now()
        
        # Simulate train movement
        if train.status == TrainStatus.MOVING:
            # Calculate movement between stations
            current_coords = self.station_coordinates.get(train.current_station)
            next_coords = self.station_coordinates.get(train.next_station)
            
            if current_coords and next_coords:
                # Calculate distance and direction
                lat_diff = next_coords[0] - current_coords[0]
                lon_diff = next_coords[1] - current_coords[1]
                
                # Move train towards next station
                move_factor = 0.1  # Adjust for realistic movement
                train.position_lat += lat_diff * move_factor
                train.position_lon += lon_diff * move_factor
                
                # Update speed
                train.speed = random.uniform(25, 35)  # km/h
                
                # Check if arrived at next station
                distance_to_station = math.sqrt(
                    (train.position_lat - next_coords[0])**2 + 
                    (train.position_lon - next_coords[1])**2
                )
                
                if distance_to_station < 0.001:  # Arrived at station
                    train.current_station = train.next_station
                    train.status = TrainStatus.ARRIVING
                    train.speed = 0
                    
                    # Update next station
                    stations = self.route_segments.get(train.route, [])
                    train.next_station = self._get_next_station(stations, train.current_station, train.direction)
        
        elif train.status == TrainStatus.ARRIVING:
            # Station dwell time
            dwell_time = random.randint(30, 120)  # seconds
            if (current_time - train.last_update).seconds > dwell_time:
                train.status = TrainStatus.DEPARTING
                train.last_update = current_time
        
        elif train.status == TrainStatus.DEPARTING:
            # Departure delay
            departure_delay = random.randint(10, 60)  # seconds
            if (current_time - train.last_update).seconds > departure_delay:
                train.status = TrainStatus.MOVING
                train.last_update = current_time
        
        # Update passenger count
        train.passenger_count = max(0, train.passenger_count + random.randint(-10, 15))
        train.passenger_count = min(train.passenger_count, train.capacity)
        
        # Update timestamps
        train.last_update = current_time
    
    def _detect_collisions(self) -> None:
        """Detect potential collisions between trains"""
        self.collision_detector.check_collisions(list(self.trains.values()))
    
    def get_train_positions(self) -> Dict[str, TrainPosition]:
        """Get current train positions"""
        return self.trains.copy()
    
    def get_train_by_id(self, trainset_id: str) -> Optional[TrainPosition]:
        """Get specific train position by ID"""
        return self.trains.get(trainset_id)
    
    def get_trains_at_station(self, station_name: str) -> List[TrainPosition]:
        """Get all trains currently at a specific station"""
        return [train for train in self.trains.values() 
                if train.current_station == station_name]
    
    def get_trains_on_route(self, route: str) -> List[TrainPosition]:
        """Get all trains on a specific route"""
        return [train for train in self.trains.values() 
                if train.route == route]
    
    def check_and_get_collision_alerts(self) -> List[Dict]:
        """Check for collisions and return alerts for AlertManager integration"""
        if not self.trains:
            return []
        
        # Convert trains to list for collision detection
        trains_list = list(self.trains.values())
        self.collision_detector.check_collisions(trains_list)
        return self.collision_detector.get_collision_alerts()
    
    def _sync_train_with_maximo(self, trainset_id: str, train_data: Dict) -> None:
        """Sync individual train data with Maximo"""
        try:
            # Create or update asset in Maximo
            asset_id = self.maximo.create_trainset_asset(train_data)
            
            if asset_id:
                # Update asset status based on operational status
                status = train_data.get('operational_status', 'Available')
                self.maximo.update_asset_status(asset_id, status)
                
                # Create work orders for maintenance needs
                job_cards_open = train_data.get('job_cards_open', 0)
                if job_cards_open > 0:
                    maintenance_data = {
                        'description': f'Maintenance required for {trainset_id}',
                        'type': 'CM',  # Corrective Maintenance
                        'priority': 'High' if job_cards_open > 2 else 'Medium',
                        'estimated_cost': self.maximo._calculate_maintenance_cost(train_data),
                        'location': train_data.get('depot', 'Maintenance Depot')
                    }
                    self.maximo.create_maintenance_work_order(asset_id, maintenance_data)
                    
        except Exception as e:
            print(f"❌ Error syncing train {trainset_id} with Maximo: {e}")
    
    def enable_maximo_sync(self) -> bool:
        """Enable Maximo synchronization"""
        self.maximo_sync_enabled = True
        if not self.maximo_connected:
            self.maximo_connected = self.maximo.connect()
        return self.maximo_connected
    
    def disable_maximo_sync(self) -> None:
        """Disable Maximo synchronization"""
        self.maximo_sync_enabled = False
    
    def get_maximo_status(self) -> Dict:
        """Get Maximo integration status"""
        return {
            'connected': self.maximo_connected,
            'sync_enabled': self.maximo_sync_enabled,
            'last_sync': self.maximo.last_sync.isoformat() if self.maximo.last_sync else None,
            'server_url': self.maximo.maximo_url
        }
    
    def sync_all_trains_with_maximo(self) -> Dict:
        """Sync all tracked trains with Maximo"""
        if not self.maximo_connected or not self.maximo_sync_enabled:
            return {'error': 'Maximo not connected or sync disabled'}
        
        sync_results = {
            'trains_synced': 0,
            'assets_updated': 0,
            'work_orders_created': 0,
            'errors': []
        }
        
        for trainset_id, train_position in self.trains.items():
            try:
                # Convert train position to train data format
                train_data = {
                    'id': trainset_id,
                    'depot': train_position.route,  # Use route as depot for now
                    'operational_status': train_position.status.value.title(),
                    'job_cards_open': 0,  # Default value
                    'capacity': train_position.capacity
                }
                
                self._sync_train_with_maximo(trainset_id, train_data)
                sync_results['trains_synced'] += 1
                
            except Exception as e:
                sync_results['errors'].append(f"Error syncing {trainset_id}: {str(e)}")
        
        return sync_results

class CollisionDetector:
    """Detects and prevents train collisions"""
    
    def __init__(self):
        self.minimum_distance = 0.002  # Minimum distance between trains (degrees)
        self.collision_alerts = []
    
    def check_collisions(self, trains: List[TrainPosition]) -> None:
        """Check for potential collisions"""
        self.collision_alerts.clear()
        
        for i, train1 in enumerate(trains):
            for j, train2 in enumerate(trains[i+1:], i+1):
                if train1.route == train2.route:  # Same route
                    distance = self._calculate_distance(train1, train2)
                    
                    if distance < self.minimum_distance:
                        alert = {
                            'trains': [train1.trainset_id, train2.trainset_id],
                            'distance': distance,
                            'severity': 'HIGH' if distance < self.minimum_distance * 0.5 else 'MEDIUM',
                            'timestamp': datetime.now(),
                            'location': train1.current_station
                        }
                        self.collision_alerts.append(alert)
    
    def _calculate_distance(self, train1: TrainPosition, train2: TrainPosition) -> float:
        """Calculate distance between two trains"""
        return math.sqrt(
            (train1.position_lat - train2.position_lat)**2 + 
            (train1.position_lon - train2.position_lon)**2
        )
    
    def get_collision_alerts(self) -> List[Dict]:
        """Get current collision alerts"""
        return self.collision_alerts.copy()

class TimetableAnalyzer:
    """Analyzes timetable for optimization opportunities"""
    
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_timetable(self, timetable) -> Dict:
        """Analyze timetable for overlaps and optimization opportunities"""
        # Handle both list and dictionary formats
        if isinstance(timetable, list):
            # Convert list format to dictionary format for processing
            timetable_dict = {}
            for slot in timetable:
                time_slot = slot.get('time_slot', '06:00-06:30')
                timetable_dict[time_slot] = slot
            timetable = timetable_dict
        
        analysis = {
            'total_slots': len(timetable),
            'peak_slots': 0,
            'off_peak_slots': 0,
            'total_train_assignments': 0,
            'route_distribution': {},
            'capacity_utilization': [],
            'potential_overlaps': [],
            'optimization_suggestions': []
        }
        
        # Handle timetable as dictionary with time_slot keys
        for time_slot, slot_data in timetable.items():
            if slot_data.get('is_peak_hour', False):
                analysis['peak_slots'] += 1
            else:
                analysis['off_peak_slots'] += 1
            
            trains_in_slot = slot_data.get('trains', [])
            analysis['total_train_assignments'] += len(trains_in_slot)
            
            # Analyze route distribution
            for train in trains_in_slot:
                route = train.get('route', 'Unknown')
                analysis['route_distribution'][route] = analysis['route_distribution'].get(route, 0) + 1
            
            # Analyze capacity
            total_capacity = sum(train.get('capacity', 300) for train in trains_in_slot)
            analysis['capacity_utilization'].append({
                'time_slot': time_slot,
                'total_capacity': total_capacity,
                'train_count': len(trains_in_slot)
            })
        
        # Detect potential overlaps
        analysis['potential_overlaps'] = self._detect_overlaps(timetable)
        
        # Generate optimization suggestions
        analysis['optimization_suggestions'] = self._generate_suggestions(analysis)
        
        return analysis
    
    def _detect_overlaps(self, timetable) -> List[Dict]:
        """Detect potential timetable overlaps"""
        overlaps = []
        time_slots = list(timetable.keys())
        
        for i, time_slot1 in enumerate(time_slots):
            for j, time_slot2 in enumerate(time_slots[i+1:], i+1):
                # Check if time slots overlap
                slot1_start = datetime.strptime(time_slot1.split('-')[0], '%H:%M')
                slot1_end = datetime.strptime(time_slot1.split('-')[1], '%H:%M')
                slot2_start = datetime.strptime(time_slot2.split('-')[0], '%H:%M')
                slot2_end = datetime.strptime(time_slot2.split('-')[1], '%H:%M')
                
                # Check for time overlap
                if not (slot1_end <= slot2_start or slot2_end <= slot1_start):
                    # Check for train overlap
                    slot1_data = timetable[time_slot1]
                    slot2_data = timetable[time_slot2]
                    trains1 = {train['trainset_id'] for train in slot1_data.get('trains', [])}
                    trains2 = {train['trainset_id'] for train in slot2_data.get('trains', [])}
                    
                    overlapping_trains = trains1.intersection(trains2)
                    if overlapping_trains:
                        overlaps.append({
                            'slot1': time_slot1,
                            'slot2': time_slot2,
                            'overlapping_trains': list(overlapping_trains),
                            'severity': 'HIGH' if len(overlapping_trains) > 3 else 'MEDIUM'
                        })
        
        return overlaps
    
    def _generate_suggestions(self, analysis: Dict) -> List[str]:
        """Generate optimization suggestions"""
        suggestions = []
        
        # Check route distribution
        total_trains = analysis['total_train_assignments']
        for route, count in analysis['route_distribution'].items():
            percentage = (count / total_trains) * 100
            if percentage > 70:
                suggestions.append(f"Route {route} is overloaded ({percentage:.1f}% of trains). Consider redistributing.")
        
        # Check capacity utilization
        avg_capacity = sum(slot['total_capacity'] for slot in analysis['capacity_utilization']) / len(analysis['capacity_utilization'])
        if avg_capacity < 2000:
            suggestions.append("Average capacity utilization is low. Consider reducing train frequency during off-peak hours.")
        
        # Check peak hour distribution
        peak_ratio = analysis['peak_slots'] / analysis['total_slots']
        if peak_ratio < 0.2:
            suggestions.append("Peak hour slots are underutilized. Consider adding more peak hour services.")
        
        return suggestions
