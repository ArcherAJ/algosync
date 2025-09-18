from common_imports import *

from simulator import KMRLDataSimulator
from optimizer import MultiObjectiveOptimizer
from predictive_model import PredictiveMaintenanceModel
from integrator import RealTimeDataIntegrator
from alerts import AlertManager
from reports import ReportGenerator
from passenger_demand_predictor import PassengerDemandPredictor
from energy_optimizer import EnergyConsumptionOptimizer
from fleet_analytics import FleetPerformanceAnalytics

from timetable_b import TimetableGenerator

class SystemIntegrationManager:
    def __init__(self):
        self.data_simulator = KMRLDataSimulator()
        self.optimizer = MultiObjectiveOptimizer()
        self.ml_model = PredictiveMaintenanceModel()
        self.data_integrator = RealTimeDataIntegrator()
        self.alert_manager = AlertManager()
        self.report_generator = ReportGenerator()
        
        # Initialize new ML modules
        self.demand_predictor = PassengerDemandPredictor()
        self.energy_optimizer = EnergyConsumptionOptimizer()
        self.fleet_analytics = FleetPerformanceAnalytics()
        
        self.last_optimization_time = None
        self.optimization_history = []
        
        # Initialize ML integration
        self.optimizer.set_ml_model(self.ml_model)
    def initialize_system(self, n_trainsets=25):
        """Initialize the complete system with data"""
        trainsets = self.data_simulator.generate_realistic_dataset(n_trainsets)
        
        # Train all ML models with initial data
        self.ml_model.train_model(trainsets)
        self.demand_predictor.load_data()
        self.demand_predictor.train_models()
        self.energy_optimizer.load_data()
        self.energy_optimizer.train_models()
        self.fleet_analytics.train_models(trainsets)
        
        return trainsets
    def run_complete_optimization(self, trainsets, constraints):
        """Run complete optimization pipeline"""
        start_time = time.time()
        # Refresh real-time data
        trainsets, update_count = self.data_integrator.refresh_all_data(trainsets)
        # Run optimization
        optimized_trainsets, conflicts, service_ready, standby, ibl = self.optimizer.optimize_fleet_assignment(
            trainsets, constraints
        )
        # Generate maintenance predictions
        maintenance_predictions = self.ml_model.predict_maintenance(optimized_trainsets)
        # Calculate performance metrics
        performance_metrics = self._calculate_performance_metrics(optimized_trainsets, constraints)
        performance_metrics.update({
            'service_ready': service_ready,
            'standby': standby,
            'ibl_maintenance': ibl,
            'conflicts': conflicts,
            'data_updates': update_count,
            'processing_time': round(time.time() - start_time, 2)
        })
        # Check for alerts
        alerts = self.alert_manager.check_alerts(optimized_trainsets, performance_metrics)
        # Store in history
        optimization_record = {
            'timestamp': datetime.now(),
            'metrics': performance_metrics,
            'constraints': constraints,
            'alert_count': len(alerts)
        }
        self.optimization_history.append(optimization_record)
        self.last_optimization_time = datetime.now()
        return optimized_trainsets, performance_metrics, alerts, maintenance_predictions
    def _calculate_performance_metrics(self, trainsets, constraints):
        """Calculate comprehensive performance metrics"""
        metrics = {}
        # Fitness metrics
        metrics['fitness_compliance'] = round(sum(1 for t in trainsets if t['fitness']['overall_valid']) / len(trainsets) * 100, 1)
        # Maintenance metrics
        metrics['maintenance_backlog'] = sum(t['job_cards']['open'] for t in trainsets)
        # Branding metrics
        metrics['branding_compliance'] = round(sum(1 for t in trainsets if t['branding']['exposure_deficit'] == 0) / len(trainsets) * 100, 1)
        # Operational metrics
        metrics['avg_reliability'] = round(sum(t['operational']['reliability_score'] for t in trainsets) / len(trainsets), 1)
        # Economic metrics (simulated)
        metrics['estimated_savings'] = random.randint(5000, 20000)
        metrics['energy_efficiency'] = random.randint(85, 98)
        return metrics
    def generate_comprehensive_report(self, trainsets, metrics, alerts, report_type='daily_operations'):
        """Generate comprehensive report for management"""
        report = self.report_generator.generate_report(
            report_type, trainsets, metrics, alerts
        )
        # Add system performance data
        if report:
            report['system_performance'] = {
                'last_optimization': self.last_optimization_time,
                'total_optimizations': len(self.optimization_history),
                'ml_model_status': 'Trained' if self.ml_model.is_trained else 'Not Trained',
                'data_sources_connected': {
                    source: status['connected'] 
                    for source, status in self.data_integrator.data_sources.items()
                }
            }
        return report
    def get_optimization_trends(self):
        """Get historical optimization trends for analytics"""
        if not self.optimization_history:
            return None
        trends = {
            'timestamps': [record['timestamp'] for record in self.optimization_history],
            'service_readiness': [record['metrics'].get('service_ready', 0) for record in self.optimization_history],
            'fitness_compliance': [record['metrics'].get('fitness_compliance', 0) for record in self.optimization_history],
            'alert_counts': [record['alert_count'] for record in self.optimization_history],
            'processing_times': [record['metrics'].get('processing_time', 0) for record in self.optimization_history]
        }
        return trends
    def simulate_operational_day(self, trainsets, constraints):
        """Simulate a full operational day with multiple optimizations"""
        results = []
        # Morning optimization (05:00)
        morning_result = self.run_complete_optimization(trainsets, constraints)
        results.append(('morning', morning_result))
        # Mid-day check (12:00) - simulate some changes
        updated_trainsets, _ = self.data_integrator.connect_to_iot_sensors(trainsets)
        mid_day_result = self.run_complete_optimization(updated_trainsets, constraints)
        results.append(('mid_day', mid_day_result))
        # Evening optimization (18:00) - more changes
        updated_trainsets, _ = self.data_integrator.connect_to_maximo(trainsets)
        evening_result = self.run_complete_optimization(updated_trainsets, constraints)
        results.append(('evening', evening_result))
        return results
    def generate_timetable(self, trainsets, constraints):
        timetable_gen = TimetableGenerator()
        return timetable_gen.generate_timetable(trainsets, constraints)
    def get_ml_insights(self):
        """Get comprehensive ML insights from all modules"""
        insights = {
            'maintenance_model': self.ml_model.get_model_performance(),
            'demand_predictor': self.demand_predictor.get_model_performance(),
            'energy_optimizer': self.energy_optimizer.get_model_performance(),
            'fleet_analytics': self.fleet_analytics.get_model_performance()
        }
        return insights
    
    def get_demand_forecast(self, station_name, hours_ahead=24):
        """Get passenger demand forecast"""
        return self.demand_predictor.get_demand_forecast(station_name, hours_ahead)
    
    def get_energy_optimization(self, distance_km, passengers, month):
        """Get energy optimization recommendations"""
        return self.energy_optimizer.get_energy_optimization_recommendations(distance_km, passengers, month)
    
    def get_fleet_insights(self):
        """Get fleet performance insights"""
        return self.fleet_analytics.get_fleet_insights()
    
    def predict_maintenance_cost(self, trainset):
        """Predict maintenance cost for a trainset"""
        return self.ml_model.predict_maintenance_cost(trainset)
    
    def predict_failure_severity(self, trainset):
        """Predict failure severity for a trainset"""
        return self.ml_model.predict_failure_severity(trainset)

    def reset_system(self):
        """Reset the system to initial state"""
        self.ml_model = PredictiveMaintenanceModel()
        self.optimization_history = []
        self.last_optimization_time = None
        self.data_integrator = RealTimeDataIntegrator()