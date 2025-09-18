"""
Centralized Data Configuration for KMRL AI Induction Planning Platform
This file contains all shared data configurations to ensure consistency across the system.
"""

from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
random.seed(42)

class KMRLDataConfig:
    """Centralized configuration for all KMRL data"""
    
    # System Configuration
    DEFAULT_TRAINSET_COUNT = 40
    MAX_TRAINSET_COUNT = 100
    
    # Depot Configuration (2027 KMRL Model)
    DEPOTS = [
        'Aluva Depot',
        'Petta Depot', 
        'Kakkanad Depot',
        'Muttom Yard'
    ]
    
    # Advertiser/Brand Configuration
    ADVERTISERS = [
        'Coca-Cola',
        'Pepsi', 
        'Amazon',
        'Google',
        'Microsoft',
        'Apple',
        'Samsung',
        'Toyota',
        'Flipkart',
        'BSNL',
        'Airtel',
        'Jio',
        'Reliance',
        'Tata',
        'Mahindra',
        None  # For trainsets without advertising
    ]
    
    # Maintenance Configuration
    MAINTENANCE_TYPES = [
        'Routine',
        'Preventive', 
        'Corrective',
        'Emergency'
    ]
    
    PRIORITIES = [
        'Low',
        'Medium',
        'High',
        'Critical'
    ]
    
    OPERATIONAL_STATUSES = [
        'Available',
        'Standby',
        'Maintenance',
        'IBL'
    ]
    
    # Cleaning Configuration
    CLEANING_STATUSES = [
        'Clean',
        'Requires Cleaning'
    ]
    
    # Fitness Certificate Configuration
    FITNESS_DEPARTMENTS = [
        'rolling_stock',
        'signalling',
        'telecom'
    ]
    
    # Component Wear Configuration
    COMPONENT_TYPES = [
        'brake_pads',
        'bogies', 
        'hvac',
        'doors',
        'engines'
    ]
    
    # Station Configuration
    STATION_LINES = [
        'Line 1',
        'Line 2',
        'Line 3'
    ]
    
    # Time Configuration
    TIME_SLOTS = [
        '05:00-05:30', '05:30-06:00', '06:00-06:30', '06:30-07:00',
        '07:00-07:30', '07:30-08:00', '08:00-08:30', '08:30-09:00',
        '09:00-09:30', '09:30-10:00', '10:00-10:30', '10:30-11:00',
        '11:00-11:30', '11:30-12:00', '12:00-12:30', '12:30-13:00',
        '13:00-13:30', '13:30-14:00', '14:00-14:30', '14:30-15:00',
        '15:00-15:30', '15:30-16:00', '16:00-16:30', '16:30-17:00',
        '17:00-17:30', '17:30-18:00', '18:00-18:30', '18:30-19:00',
        '19:00-19:30', '19:30-20:00', '20:00-20:30', '20:30-21:00',
        '21:00-21:30', '21:30-22:00', '22:00-22:30', '22:30-23:00',
        '23:00-23:30'
    ]
    
    # Data Ranges Configuration
    RELIABILITY_SCORE_RANGE = (85, 98)
    ENERGY_EFFICIENCY_RANGE = (75, 95)
    MILEAGE_RANGE = (20000, 100000)
    CONTRACT_VALUE_RANGE = (20000, 120000)
    EXPOSURE_DEFICIT_RANGE = (1, 20)
    CROWD_DENSITY_RANGE = (0.3, 0.8)
    PUNCTUALITY_RANGE = (99.5, 99.9)  # High punctuality range
    
    # Maintenance Cycles
    MAINTENANCE_CYCLES = [30, 60, 90]  # days
    
    # Bay Configuration
    MAX_BAYS_PER_DEPOT = 15
    CLEANING_BAYS = 5
    
    @classmethod
    def get_random_depot(cls):
        """Get a random depot"""
        return random.choice(cls.DEPOTS)
    
    @classmethod
    def get_random_advertiser(cls):
        """Get a random advertiser"""
        return random.choice(cls.ADVERTISERS)
    
    @classmethod
    def get_random_maintenance_type(cls):
        """Get a random maintenance type"""
        return random.choice(cls.MAINTENANCE_TYPES)
    
    @classmethod
    def get_random_priority(cls):
        """Get a random priority"""
        return random.choice(cls.PRIORITIES)
    
    @classmethod
    def get_random_status(cls):
        """Get a random operational status"""
        return random.choice(cls.OPERATIONAL_STATUSES)
    
    @classmethod
    def get_random_cleaning_status(cls):
        """Get a random cleaning status"""
        return random.choice(cls.CLEANING_STATUSES)
    
    @classmethod
    def generate_trainset_id(cls, index):
        """Generate consistent trainset ID"""
        return f"TS{str(index).zfill(3)}"
    
    @classmethod
    def generate_fitness_certificate_id(cls, depot, trainset_id):
        """Generate fitness certificate ID"""
        depot_code = depot.replace(' ', '').replace('Depot', '').replace('Yard', '')
        return f"FIT-{depot_code}-{trainset_id}"
    
    @classmethod
    def generate_bay_name(cls, bay_number):
        """Generate bay name"""
        return f"Bay-{bay_number}"
    
    @classmethod
    def get_reliability_score(cls):
        """Get random reliability score within range"""
        return random.randint(*cls.RELIABILITY_SCORE_RANGE)
    
    @classmethod
    def get_energy_efficiency(cls):
        """Get random energy efficiency within range"""
        return random.randint(*cls.ENERGY_EFFICIENCY_RANGE)
    
    @classmethod
    def get_mileage(cls):
        """Get random mileage within range"""
        return random.randint(*cls.MILEAGE_RANGE)
    
    @classmethod
    def get_contract_value(cls):
        """Get random contract value within range"""
        return random.randint(*cls.CONTRACT_VALUE_RANGE)
    
    @classmethod
    def get_exposure_deficit(cls):
        """Get random exposure deficit within range"""
        return random.randint(*cls.EXPOSURE_DEFICIT_RANGE)
    
    @classmethod
    def get_crowd_density(cls):
        """Get random crowd density within range"""
        return random.uniform(*cls.CROWD_DENSITY_RANGE)
    
    @classmethod
    def get_punctuality_score(cls):
        """Get random punctuality score within range (99.5% - 99.9%)"""
        return round(random.uniform(*cls.PUNCTUALITY_RANGE), 2)
    
    @classmethod
    def get_maintenance_cycle(cls):
        """Get random maintenance cycle"""
        return random.choice(cls.MAINTENANCE_CYCLES)
    
    @classmethod
    def get_bay_number(cls):
        """Get random bay number"""
        return random.randint(1, cls.MAX_BAYS_PER_DEPOT)
    
    @classmethod
    def get_cleaning_bay(cls):
        """Get random cleaning bay"""
        return random.randint(1, cls.CLEANING_BAYS)
    
    @classmethod
    def get_component_wear(cls, component_type):
        """Get component wear percentage"""
        base_wear = {
            'brake_pads': (10, 90),
            'bogies': (5, 80),
            'hvac': (20, 80),
            'doors': (15, 85),
            'engines': (5, 75)
        }
        return random.randint(*base_wear.get(component_type, (10, 90)))
    
    @classmethod
    def get_facility_utilization(cls, facility_type):
        """Get facility utilization percentage"""
        utilization_ranges = {
            'elevators': (0.4, 0.9),
            'escalators': (0.6, 0.95),
            'parking': (0.3, 0.8),
            'commercial': (0.2, 0.7)
        }
        return random.uniform(*utilization_ranges.get(facility_type, (0.3, 0.8)))

# Create a global instance for easy access
config = KMRLDataConfig()
