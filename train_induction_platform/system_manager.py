import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import io
import time
import math
import threading
import queue
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import warnings

from simulator import KMRLDataSimulator
from optimizer import MultiObjectiveOptimizer
from predictive_model import PredictiveMaintenanceModel
from integrator import RealTimeDataIntegrator
from alerts import AlertManager
from reports import ReportGenerator

from timetable_b import TimetableGenerator

class SystemIntegrationManager:
    def __init__(self):
        self.data_simulator = KMRLDataSimulator()
        self.optimizer = MultiObjectiveOptimizer()
        self.ml_model = PredictiveMaintenanceModel()
        self.data_integrator = RealTimeDataIntegrator()
        self.alert_manager = AlertManager()
        self.report_generator = ReportGenerator()
        self.last_optimization_time = None
        self.optimization_history = []
    def initialize_system(self, n_trainsets=25):
        """Initialize the complete system with data"""
        trainsets = self.data_simulator.generate_realistic_dataset(n_trainsets)
        # Train ML model with initial data
        self.ml_model.train_model(trainsets)
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
    def reset_system(self):
        """Reset the system to initial state"""
        self.ml_model = PredictiveMaintenanceModel()
        self.optimization_history = []
        self.last_optimization_time = None
        self.data_integrator = RealTimeDataIntegrator()