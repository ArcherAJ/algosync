from common_imports import *

class AlertManager:
    def __init__(self):
        self.alerts = []
        self.alert_rules = {
            'fitness_expiry': {'threshold': 2, 'priority': 'High'},
            'high_risk_maintenance': {'threshold': 75, 'priority': 'Critical'},
            'branding_deficit': {'threshold': 15, 'priority': 'Medium'},
            'service_readiness': {'threshold': 12, 'priority': 'High'},
            'conflict_detection': {'priority': 'High'}
        }
    def check_alerts(self, trainsets, optimization_results=None):
        """Check all alert conditions"""
        self.alerts = []
        self._check_fitness_alerts(trainsets)
        self._check_maintenance_alerts(trainsets)
        self._check_branding_alerts(trainsets)
        self._check_service_alerts(trainsets, optimization_results)
        self._check_conflict_alerts(optimization_results)
        return self.alerts
    def _check_fitness_alerts(self, trainsets):
        """Check fitness certificate alerts"""
        for trainset in trainsets:
            if trainset['fitness']['days_until_expiry'] <= self.alert_rules['fitness_expiry']['threshold']:
                self.alerts.append({
                    'type': 'fitness_expiry',
                    'priority': self.alert_rules['fitness_expiry']['priority'],
                    'message': f"{trainset['id']}: Fitness expires in {trainset['fitness']['days_until_expiry']} days",
                    'trainset_id': trainset['id'],
                    'timestamp': datetime.now()
                })
    def _check_maintenance_alerts(self, trainsets):
        """Check maintenance risk alerts"""
        for trainset in trainsets:
            wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
            if wear_avg >= self.alert_rules['high_risk_maintenance']['threshold']:
                self.alerts.append({
                    'type': 'high_risk_maintenance',
                    'priority': self.alert_rules['high_risk_maintenance']['priority'],
                    'message': f"{trainset['id']}: High component wear ({wear_avg:.1f}%)",
                    'trainset_id': trainset['id'],
                    'timestamp': datetime.now()
                })    
    def _check_branding_alerts(self, trainsets):
        """Check branding commitment alerts"""
        for trainset in trainsets:
            if trainset['branding']['exposure_deficit'] >= self.alert_rules['branding_deficit']['threshold']:
                self.alerts.append({
                    'type': 'branding_deficit',
                    'priority': self.alert_rules['branding_deficit']['priority'],
                    'message': f"{trainset['id']}: High exposure deficit ({trainset['branding']['exposure_deficit']} hours)",
                    'trainset_id': trainset['id'],
                    'timestamp': datetime.now()
                })
    def _check_service_alerts(self, trainsets, optimization_results):
        """Check service readiness alerts"""
        if optimization_results and optimization_results.get('service_ready', 0) < self.alert_rules['service_readiness']['threshold']:
            self.alerts.append({
                'type': 'service_readiness',
                'priority': self.alert_rules['service_readiness']['priority'],
                'message': f"Low service readiness: Only {optimization_results['service_ready']} trains available",
                'trainset_id': None,
                'timestamp': datetime.now()
            })
    def _check_conflict_alerts(self, optimization_results):
        """Check optimization conflict alerts"""
        if optimization_results and optimization_results.get('conflicts'):
            self.alerts.append({
                'type': 'conflict_detection',
                'priority': self.alert_rules['conflict_detection']['priority'],
                'message': f"Found {len(optimization_results['conflicts'])} optimization conflicts",
                'trainset_id': None,
                'timestamp': datetime.now()
            }) 
    def get_priority_alerts(self, priority_level='Critical'):
        """Get alerts filtered by priority"""
        return [alert for alert in self.alerts if alert['priority'] == priority_level]
# Report Generation System