from common_imports import *
from ibm_maximo_integration import IBMMaximoIntegration, MaximoDataAdapter
from mock_maximo_server import start_mock_maximo_server, get_mock_server
from typing import Dict, List, Optional, Any
import pandas as pd
from datetime import datetime, timedelta
import json

class MaximoDataConnector:
    """
    Comprehensive IBM Maximo Data Connector for KMRL Train Induction Platform
    
    This class connects IBM Maximo with existing datasets and generates
    comprehensive results for asset management, maintenance planning,
    and operational optimization.
    """
    
    def __init__(self):
        """Initialize the Maximo data connector"""
        self.maximo = IBMMaximoIntegration()
        self.maximo_connected = False
        self.datasets = {}
        self.results = {}
        self.mock_server = None
        self.use_mock_mode = True  # Always use mock mode for now
        
    def connect_to_maximo(self) -> bool:
        """Connect to IBM Maximo server with mock fallback"""
        try:
            if self.use_mock_mode:
                # Always use mock server for demonstration
                self.mock_server = start_mock_maximo_server()
                self.maximo_connected = True
                print("✅ Connected to Mock Maximo Server successfully")
                return True
            else:
                self.maximo_connected = self.maximo.connect()
                if self.maximo_connected:
                    print("✅ Connected to IBM Maximo successfully")
                else:
                    print("⚠️ Maximo connection failed - using mock mode")
                    self.mock_server = start_mock_maximo_server()
                    self.maximo_connected = True
                return self.maximo_connected
        except Exception as e:
            print(f"❌ Maximo connection error: {e}")
            print("🔄 Switching to Mock Maximo Server...")
            self.mock_server = start_mock_maximo_server()
            self.maximo_connected = True
            return True
    
    def load_existing_datasets(self) -> Dict[str, pd.DataFrame]:
        """Load all existing datasets from CSV files"""
        datasets = {}
        
        try:
            # Load trainsets data
            datasets['trainsets'] = pd.read_csv('trainsets_ml_ready.csv')
            print(f"✅ Loaded {len(datasets['trainsets'])} trainsets")
            
            # Load stations data
            datasets['stations'] = pd.read_csv('metro_stations.csv')
            print(f"✅ Loaded {len(datasets['stations'])} stations")
            
            # Load passenger demand data
            try:
                datasets['passenger_demand'] = pd.read_csv('passenger_demand_data.csv')
                print(f"✅ Loaded passenger demand data")
            except:
                print("⚠️ Passenger demand data not found")
            
            # Load energy consumption data
            try:
                datasets['energy'] = pd.read_csv('energy_consumption.csv')
                print(f"✅ Loaded energy consumption data")
            except:
                print("⚠️ Energy consumption data not found")
            
            # Load historical maintenance data
            try:
                datasets['maintenance'] = pd.read_csv('historical_maintenance.csv')
                print(f"✅ Loaded historical maintenance data")
            except:
                print("⚠️ Historical maintenance data not found")
            
            self.datasets = datasets
            return datasets
            
        except Exception as e:
            print(f"❌ Error loading datasets: {e}")
            return {}
    
    def sync_trainsets_with_maximo(self) -> Dict:
        """Sync trainsets data with IBM Maximo"""
        if not self.datasets.get('trainsets') is not None:
            return {'error': 'No trainsets data loaded'}
        
        sync_results = {
            'assets_created': 0,
            'work_orders_created': 0,
            'assets_updated': 0,
            'errors': []
        }
        
        try:
            trainsets_df = self.datasets['trainsets']
            
            for _, trainset in trainsets_df.iterrows():
                # Convert trainset data to Maximo format
                trainset_data = self._convert_trainset_to_maximo_format(trainset)
                
                # Create asset in Maximo
                asset_id = self.maximo.create_trainset_asset(trainset_data)
                if asset_id:
                    sync_results['assets_created'] += 1
                    
                    # Create work orders for maintenance needs
                    if trainset['job_cards_open'] > 0:
                        maintenance_data = {
                            'description': f"Maintenance required for {trainset['trainset_id']}",
                            'type': 'CM',  # Corrective Maintenance
                            'priority': self._map_priority(trainset['job_cards_priority']),
                            'estimated_cost': self._calculate_maintenance_cost(trainset),
                            'location': trainset['depot'],
                            'scheduled_start': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'scheduled_finish': (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')
                        }
                        
                        wo_id = self.maximo.create_maintenance_work_order(asset_id, maintenance_data)
                        if wo_id:
                            sync_results['work_orders_created'] += 1
                    
                    # Update asset status
                    status = self._map_operational_status(trainset['operational_status'])
                    self.maximo.update_asset_status(asset_id, status)
                    sync_results['assets_updated'] += 1
            
            print(f"✅ Synced {sync_results['assets_created']} trainsets with Maximo")
            return sync_results
            
        except Exception as e:
            sync_results['errors'].append(str(e))
            print(f"❌ Error syncing trainsets: {e}")
            return sync_results
    
    def sync_stations_with_maximo(self) -> Dict:
        """Sync stations data with IBM Maximo as facility assets"""
        if not self.datasets.get('stations') is not None:
            return {'error': 'No stations data loaded'}
        
        sync_results = {
            'facilities_created': 0,
            'errors': []
        }
        
        try:
            stations_df = self.datasets['stations']
            
            for _, station in stations_df.iterrows():
                # Create station as facility asset in Maximo
                facility_data = {
                    'assetnum': station['station_id'],
                    'description': f"KMRL Station - {station['station_name']}",
                    'assettype': 'FACILITY',
                    'location': station['station_name'],
                    'status': 'ACTIVE',
                    'manufacturer': 'KMRL',
                    'model': 'Metro Station',
                    'serialnumber': station['station_id'],
                    'installdate': datetime.now().strftime('%Y-%m-%d'),
                    'warrantyexpiration': (datetime.now() + timedelta(days=365*10)).strftime('%Y-%m-%d'),
                    'lastinspection': datetime.now().strftime('%Y-%m-%d'),
                    'nextinspection': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
                    'maintenancecost': 0.0,
                    'replacementcost': 500000000.0,  # 500 million INR
                    'criticality': 'HIGH'
                }
                
                # Create facility asset
                response = self.maximo.session.post(
                    f"{self.maximo.maximo_url}/oslc/os/mxapiasset",
                    json=facility_data
                )
                
                if response.status_code in [200, 201]:
                    sync_results['facilities_created'] += 1
                else:
                    sync_results['errors'].append(f"Failed to create facility {station['station_id']}")
            
            print(f"✅ Synced {sync_results['facilities_created']} stations with Maximo")
            return sync_results
            
        except Exception as e:
            sync_results['errors'].append(str(e))
            print(f"❌ Error syncing stations: {e}")
            return sync_results
    
    def generate_comprehensive_results(self) -> Dict:
        """Generate comprehensive Maximo integration results"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'maximo_connected': self.maximo_connected,
            'datasets_loaded': list(self.datasets.keys()),
            'sync_results': {},
            'analytics': {},
            'recommendations': []
        }
        
        try:
            # Sync all data with Maximo
            if self.datasets.get('trainsets') is not None:
                results['sync_results']['trainsets'] = self.sync_trainsets_with_maximo()
            
            if self.datasets.get('stations') is not None:
                results['sync_results']['stations'] = self.sync_stations_with_maximo()
            
            # Generate analytics
            results['analytics'] = self._generate_analytics()
            
            # Generate recommendations
            results['recommendations'] = self._generate_recommendations()
            
            self.results = results
            return results
            
        except Exception as e:
            results['error'] = str(e)
            print(f"❌ Error generating results: {e}")
            return results
    
    def _convert_trainset_to_maximo_format(self, trainset: pd.Series) -> Dict:
        """Convert trainset data to Maximo asset format"""
        return {
            'id': trainset['trainset_id'],
            'depot': trainset['depot'],
            'operational_status': trainset['operational_status'],
            'job_cards_open': trainset['job_cards_open'],
            'capacity': 300,  # Default capacity
            'manufacturer': 'Alstom',
            'model': 'Metro Train',
            'year_manufactured': 2017 + (hash(trainset['trainset_id']) % 5),  # Random year 2017-2021
            'fitness_certificate_valid': all([
                trainset['fitness_rolling_stock'],
                trainset['fitness_signalling'],
                trainset['fitness_telecom']
            ]),
            'mileage_total': trainset['mileage_total_km'],
            'reliability_score': trainset['operational_reliability_score']
        }
    
    def _map_priority(self, priority: str) -> str:
        """Map KMRL priority to Maximo priority"""
        priority_mapping = {
            'Low': '3',
            'Medium': '2',
            'High': '1',
            'Critical': '1'
        }
        return priority_mapping.get(priority, '2')
    
    def _map_operational_status(self, status: str) -> str:
        """Map KMRL operational status to Maximo asset status"""
        status_mapping = {
            'Available': 'ACTIVE',
            'Standby': 'ACTIVE',
            'Maintenance': 'MAINTENANCE',
            'IBL': 'OUT_OF_SERVICE'
        }
        return status_mapping.get(status, 'ACTIVE')
    
    def _calculate_maintenance_cost(self, trainset: pd.Series) -> float:
        """Calculate estimated maintenance cost"""
        base_cost = 10000.0
        job_cards = trainset['job_cards_open']
        wear_factor = (trainset['mileage_brake_wear'] + trainset['mileage_bogie_wear'] + trainset['mileage_hvac_wear']) / 300
        
        return base_cost + (job_cards * 5000) + (wear_factor * 2000)
    
    def _generate_analytics(self) -> Dict:
        """Generate comprehensive analytics from the data"""
        analytics = {}
        
        try:
            if self.datasets.get('trainsets') is not None:
                trainsets_df = self.datasets['trainsets']
                
                # Fleet analytics
                analytics['fleet'] = {
                    'total_trainsets': len(trainsets_df),
                    'available_trainsets': len(trainsets_df[trainsets_df['operational_status'] == 'Available']),
                    'maintenance_trainsets': len(trainsets_df[trainsets_df['operational_status'] == 'Maintenance']),
                    'ibl_trainsets': len(trainsets_df[trainsets_df['operational_status'] == 'IBL']),
                    'average_reliability': trainsets_df['operational_reliability_score'].mean(),
                    'total_job_cards': trainsets_df['job_cards_open'].sum(),
                    'average_mileage': trainsets_df['mileage_total_km'].mean()
                }
                
                # Maintenance analytics
                analytics['maintenance'] = {
                    'critical_maintenance': len(trainsets_df[trainsets_df['job_cards_open'] > 3]),
                    'high_priority_jobs': len(trainsets_df[trainsets_df['job_cards_priority'] == 'High']),
                    'preventive_maintenance': len(trainsets_df[trainsets_df['job_cards_maintenance_type'] == 'Preventive']),
                    'corrective_maintenance': len(trainsets_df[trainsets_df['job_cards_maintenance_type'] == 'Corrective']),
                    'estimated_total_cost': sum(self._calculate_maintenance_cost(row) for _, row in trainsets_df.iterrows())
                }
                
                # Depot analytics
                depot_analysis = trainsets_df.groupby('depot').agg({
                    'trainset_id': 'count',
                    'operational_reliability_score': 'mean',
                    'job_cards_open': 'sum',
                    'mileage_total_km': 'mean'
                }).to_dict('index')
                
                analytics['depots'] = depot_analysis
                
                # Branding analytics
                if 'branding_advertiser' in trainsets_df.columns:
                    branding_analysis = trainsets_df.groupby('branding_advertiser').agg({
                        'trainset_id': 'count',
                        'branding_contract_value': 'sum'
                    }).to_dict('index')
                    analytics['branding'] = branding_analysis
            
            if self.datasets.get('stations') is not None:
                stations_df = self.datasets['stations']
                
                analytics['stations'] = {
                    'total_stations': len(stations_df),
                    'total_passengers': stations_df['daily_passengers'].sum(),
                    'average_accessibility': stations_df['accessibility_score'].mean(),
                    'total_parking': stations_df['parking_capacity'].sum(),
                    'total_commercial_spaces': stations_df['commercial_spaces'].sum()
                }
            
            return analytics
            
        except Exception as e:
            print(f"❌ Error generating analytics: {e}")
            return {}
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on the data"""
        recommendations = []
        
        try:
            if self.datasets.get('trainsets') is not None:
                trainsets_df = self.datasets['trainsets']
                
                # Maintenance recommendations
                critical_maintenance = trainsets_df[trainsets_df['job_cards_open'] > 3]
                if len(critical_maintenance) > 0:
                    recommendations.append(f"🚨 URGENT: {len(critical_maintenance)} trainsets require immediate maintenance")
                
                low_reliability = trainsets_df[trainsets_df['operational_reliability_score'] < 70]
                if len(low_reliability) > 0:
                    recommendations.append(f"⚠️ {len(low_reliability)} trainsets have low reliability scores - consider preventive maintenance")
                
                # Fleet optimization recommendations
                available_ratio = len(trainsets_df[trainsets_df['operational_status'] == 'Available']) / len(trainsets_df)
                if available_ratio < 0.8:
                    recommendations.append("📈 Fleet availability is below 80% - optimize maintenance scheduling")
                
                # Depot recommendations
                depot_analysis = trainsets_df.groupby('depot')['job_cards_open'].sum()
                max_depot = depot_analysis.idxmax()
                if depot_analysis[max_depot] > 10:
                    recommendations.append(f"🔧 {max_depot} depot has high maintenance workload - consider resource reallocation")
                
                # Branding recommendations
                if 'branding_advertiser' in trainsets_df.columns:
                    unbranded = trainsets_df[trainsets_df['branding_advertiser'].isna()]
                    if len(unbranded) > 0:
                        recommendations.append(f"💰 {len(unbranded)} trainsets are unbranded - potential revenue opportunity")
            
            if self.datasets.get('stations') is not None:
                stations_df = self.datasets['stations']
                
                # Station recommendations
                low_accessibility = stations_df[stations_df['accessibility_score'] < 0.7]
                if len(low_accessibility) > 0:
                    recommendations.append(f"♿ {len(low_accessibility)} stations have low accessibility scores - consider improvements")
                
                high_passengers = stations_df[stations_df['daily_passengers'] > stations_df['daily_passengers'].quantile(0.8)]
                if len(high_passengers) > 0:
                    recommendations.append(f"👥 {len(high_passengers)} stations have high passenger volume - consider capacity expansion")
            
            return recommendations
            
        except Exception as e:
            print(f"❌ Error generating recommendations: {e}")
            return []
    
    def export_results_to_csv(self, filename: str = None) -> str:
        """Export comprehensive results to CSV"""
        if not filename:
            filename = f"maximo_integration_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        try:
            # Create results DataFrame
            results_data = []
            
            if self.datasets.get('trainsets') is not None:
                trainsets_df = self.datasets['trainsets']
                for _, trainset in trainsets_df.iterrows():
                    results_data.append({
                        'Asset_ID': trainset['trainset_id'],
                        'Asset_Type': 'TRAINSET',
                        'Status': self._map_operational_status(trainset['operational_status']),
                        'Depot': trainset['depot'],
                        'Reliability_Score': trainset['operational_reliability_score'],
                        'Job_Cards_Open': trainset['job_cards_open'],
                        'Priority': trainset['job_cards_priority'],
                        'Maintenance_Type': trainset['job_cards_maintenance_type'],
                        'Estimated_Cost': self._calculate_maintenance_cost(trainset),
                        'Mileage_Total': trainset['mileage_total_km'],
                        'Fitness_Valid': all([
                            trainset['fitness_rolling_stock'],
                            trainset['fitness_signalling'],
                            trainset['fitness_telecom']
                        ]),
                        'Branding_Advertiser': trainset.get('branding_advertiser', 'None'),
                        'Contract_Value': trainset.get('branding_contract_value', 0),
                        'AI_Score': trainset.get('ai_score', 0),
                        'Recommendation': trainset.get('recommendation', 'Unknown')
                    })
            
            if self.datasets.get('stations') is not None:
                stations_df = self.datasets['stations']
                for _, station in stations_df.iterrows():
                    results_data.append({
                        'Asset_ID': station['station_id'],
                        'Asset_Type': 'FACILITY',
                        'Status': 'ACTIVE',
                        'Depot': station['station_name'],
                        'Reliability_Score': station['accessibility_score'] * 100,
                        'Job_Cards_Open': 0,
                        'Priority': 'Low',
                        'Maintenance_Type': 'Routine',
                        'Estimated_Cost': 0,
                        'Mileage_Total': 0,
                        'Fitness_Valid': True,
                        'Branding_Advertiser': 'None',
                        'Contract_Value': 0,
                        'AI_Score': station['accessibility_score'] * 100,
                        'Recommendation': 'Operational'
                    })
            
            # Create DataFrame and export
            results_df = pd.DataFrame(results_data)
            results_df.to_csv(filename, index=False)
            
            print(f"✅ Results exported to {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Error exporting results: {e}")
            return ""
    
    def get_summary_report(self) -> str:
        """Generate a comprehensive summary report"""
        if not self.results:
            return "No results available. Please run generate_comprehensive_results() first."
        
        report = f"""
# IBM Maximo Integration Report
Generated: {self.results['timestamp']}

## Connection Status
- Maximo Connected: {'✅ Yes' if self.results['maximo_connected'] else '❌ No'}
- Datasets Loaded: {', '.join(self.results['datasets_loaded'])}

## Sync Results
"""
        
        if 'sync_results' in self.results:
            for dataset, results in self.results['sync_results'].items():
                if 'error' not in results:
                    report += f"\n### {dataset.title()}\n"
                    for key, value in results.items():
                        if key != 'errors':
                            report += f"- {key.replace('_', ' ').title()}: {value}\n"
        
        if 'analytics' in self.results:
            report += "\n## Analytics Summary\n"
            analytics = self.results['analytics']
            
            if 'fleet' in analytics:
                fleet = analytics['fleet']
                report += f"\n### Fleet Analytics\n"
                report += f"- Total Trainsets: {fleet['total_trainsets']}\n"
                report += f"- Available: {fleet['available_trainsets']}\n"
                report += f"- In Maintenance: {fleet['maintenance_trainsets']}\n"
                report += f"- Average Reliability: {fleet['average_reliability']:.1f}%\n"
                report += f"- Total Job Cards: {fleet['total_job_cards']}\n"
            
            if 'maintenance' in analytics:
                maint = analytics['maintenance']
                report += f"\n### Maintenance Analytics\n"
                report += f"- Critical Maintenance: {maint['critical_maintenance']}\n"
                report += f"- High Priority Jobs: {maint['high_priority_jobs']}\n"
                report += f"- Estimated Total Cost: ₹{maint['estimated_total_cost']:,.0f}\n"
        
        if 'recommendations' in self.results:
            report += "\n## Recommendations\n"
            for i, rec in enumerate(self.results['recommendations'], 1):
                report += f"{i}. {rec}\n"
        
        return report

# Example usage and testing
if __name__ == "__main__":
    # Initialize the connector
    connector = MaximoDataConnector()
    
    # Connect to Maximo
    connector.connect_to_maximo()
    
    # Load existing datasets
    datasets = connector.load_existing_datasets()
    
    # Generate comprehensive results
    results = connector.generate_comprehensive_results()
    
    # Export results
    filename = connector.export_results_to_csv()
    
    # Generate summary report
    report = connector.get_summary_report()
    print(report)
