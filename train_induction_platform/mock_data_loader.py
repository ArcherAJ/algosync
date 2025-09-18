from common_imports import *
from train_tracker import TrainTracker, TrainPosition, TrainStatus
import pandas as pd
from datetime import datetime

class MockDataLoader:
    """Utility class to load and process mock train tracking data"""
    
    def __init__(self, csv_file_path='mock_train_tracking_data.csv'):
        self.csv_file_path = csv_file_path
        self.data = None
        
    def load_data(self):
        """Load mock data from CSV file"""
        try:
            self.data = pd.read_csv(self.csv_file_path)
            print(f"✅ Loaded {len(self.data)} records from {self.csv_file_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def get_latest_positions(self):
        """Get the latest position for each train"""
        if self.data is None:
            return None
        
        # Get the latest timestamp
        latest_time = self.data['timestamp'].max()
        
        # Filter data for latest timestamp
        latest_data = self.data[self.data['timestamp'] == latest_time]
        
        return latest_data
    
    def get_train_history(self, trainset_id):
        """Get historical data for a specific train"""
        if self.data is None:
            return None
        
        return self.data[self.data['trainset_id'] == trainset_id].sort_values('timestamp')
    
    def get_station_data(self, station_name):
        """Get all trains that passed through a specific station"""
        if self.data is None:
            return None
        
        return self.data[self.data['current_station'] == station_name]
    
    def get_route_data(self, route_name):
        """Get all trains on a specific route"""
        if self.data is None:
            return None
        
        return self.data[self.data['route'] == route_name]
    
    def get_status_summary(self):
        """Get summary statistics by status"""
        if self.data is None:
            return None
        
        return self.data.groupby('status').agg({
            'trainset_id': 'count',
            'speed_kmh': 'mean',
            'passenger_count': 'mean',
            'delay_minutes': 'mean'
        }).round(2)
    
    def get_capacity_analysis(self):
        """Analyze capacity utilization"""
        if self.data is None:
            return None
        
        self.data['capacity_utilization'] = (self.data['passenger_count'] / self.data['capacity']) * 100
        
        return {
            'average_utilization': self.data['capacity_utilization'].mean(),
            'max_utilization': self.data['capacity_utilization'].max(),
            'overcrowded_trains': len(self.data[self.data['capacity_utilization'] > 90]),
            'underutilized_trains': len(self.data[self.data['capacity_utilization'] < 50])
        }
    
    def get_delay_analysis(self):
        """Analyze delay patterns"""
        if self.data is None:
            return None
        
        delayed_trains = self.data[self.data['delay_minutes'] > 0]
        
        return {
            'total_delays': len(delayed_trains),
            'average_delay': delayed_trains['delay_minutes'].mean(),
            'max_delay': delayed_trains['delay_minutes'].max(),
            'delay_percentage': (len(delayed_trains) / len(self.data)) * 100
        }
    
    def create_train_positions(self, timestamp=None):
        """Convert CSV data to TrainPosition objects"""
        if self.data is None:
            return []
        
        # Use latest timestamp if none specified
        if timestamp is None:
            timestamp = self.data['timestamp'].max()
        
        # Filter data for specific timestamp
        filtered_data = self.data[self.data['timestamp'] == timestamp]
        
        train_positions = []
        for _, row in filtered_data.iterrows():
            # Convert status string to enum
            status_map = {
                'stationary': TrainStatus.STATIONARY,
                'moving': TrainStatus.MOVING,
                'arriving': TrainStatus.ARRIVING,
                'departing': TrainStatus.DEPARTING,
                'delayed': TrainStatus.DELAYED,
                'maintenance': TrainStatus.MAINTENANCE
            }
            
            status = status_map.get(row['status'], TrainStatus.STATIONARY)
            
            train_position = TrainPosition(
                trainset_id=row['trainset_id'],
                current_station=row['current_station'],
                next_station=row['next_station'],
                route=row['route'],
                status=status,
                position_lat=row['position_lat'],
                position_lon=row['position_lon'],
                speed=row['speed_kmh'],
                direction=row['direction'],
                delay_minutes=int(row['delay_minutes']),
                passenger_count=int(row['passenger_count']),
                capacity=int(row['capacity']),
                last_update=datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S'),
                estimated_arrival=datetime.strptime(row['estimated_arrival'], '%H:%M:%S'),
                estimated_departure=datetime.strptime(row['estimated_departure'], '%H:%M:%S')
            )
            
            train_positions.append(train_position)
        
        return train_positions
    
    def get_time_range(self):
        """Get the time range of the data"""
        if self.data is None:
            return None
        
        return {
            'start_time': self.data['timestamp'].min(),
            'end_time': self.data['timestamp'].max(),
            'duration_hours': (pd.to_datetime(self.data['timestamp'].max()) - 
                             pd.to_datetime(self.data['timestamp'].min())).total_seconds() / 3600
        }
    
    def export_filtered_data(self, output_file, filters=None):
        """Export filtered data to CSV"""
        if self.data is None:
            return False
        
        filtered_data = self.data.copy()
        
        if filters:
            for column, value in filters.items():
                if column in filtered_data.columns:
                    filtered_data = filtered_data[filtered_data[column] == value]
        
        filtered_data.to_csv(output_file, index=False)
        print(f"✅ Exported {len(filtered_data)} records to {output_file}")
        return True

def demo_mock_data_usage():
    """Demonstrate how to use the mock data"""
    print("🚆 Mock Train Tracking Data Demo")
    print("=" * 50)
    
    # Initialize data loader
    loader = MockDataLoader('mock_train_tracking_data.csv')
    
    # Load data
    if not loader.load_data():
        return
    
    # Get time range
    time_range = loader.get_time_range()
    print(f"\n📅 Data Time Range:")
    print(f"  Start: {time_range['start_time']}")
    print(f"  End: {time_range['end_time']}")
    print(f"  Duration: {time_range['duration_hours']:.1f} hours")
    
    # Get latest positions
    latest_positions = loader.get_latest_positions()
    print(f"\n📍 Latest Train Positions ({len(latest_positions)} trains):")
    for _, train in latest_positions.iterrows():
        print(f"  {train['trainset_id']}: {train['current_station']} -> {train['next_station']} "
              f"({train['status']}, {train['speed_kmh']} km/h)")
    
    # Get status summary
    status_summary = loader.get_status_summary()
    print(f"\n📊 Status Summary:")
    print(status_summary)
    
    # Get capacity analysis
    capacity_analysis = loader.get_capacity_analysis()
    print(f"\n👥 Capacity Analysis:")
    print(f"  Average Utilization: {capacity_analysis['average_utilization']:.1f}%")
    print(f"  Max Utilization: {capacity_analysis['max_utilization']:.1f}%")
    print(f"  Overcrowded Trains: {capacity_analysis['overcrowded_trains']}")
    print(f"  Underutilized Trains: {capacity_analysis['underutilized_trains']}")
    
    # Get delay analysis
    delay_analysis = loader.get_delay_analysis()
    print(f"\n⏰ Delay Analysis:")
    print(f"  Total Delays: {delay_analysis['total_delays']}")
    print(f"  Average Delay: {delay_analysis['average_delay']:.1f} minutes")
    print(f"  Max Delay: {delay_analysis['max_delay']} minutes")
    print(f"  Delay Percentage: {delay_analysis['delay_percentage']:.1f}%")
    
    # Get train history example
    train_history = loader.get_train_history('TRAIN_001')
    print(f"\n🚆 Train TRAIN_001 History ({len(train_history)} records):")
    for _, record in train_history.head(3).iterrows():
        print(f"  {record['timestamp']}: {record['current_station']} -> {record['next_station']} "
              f"({record['status']})")
    
    print(f"\n🎉 Mock data demo completed!")
    print(f"📁 Use this data to test your train tracking platform!")

if __name__ == "__main__":
    demo_mock_data_usage()
