from common_imports import *

class ReportGenerator:
    def __init__(self):
        self.report_templates = {
            'daily_operations': self._generate_daily_operations_report,
            'maintenance_plan': self._generate_maintenance_report,
            'branding_compliance': self._generate_branding_report,
            'optimization_summary': self._generate_optimization_report
        }
    def generate_report(self, report_type, trainsets, optimization_results=None, alerts=None):
        """Generate a specific type of report"""
        if report_type in self.report_templates:
            return self.report_templates[report_type](trainsets, optimization_results, alerts)
        return None
    def _generate_daily_operations_report(self, trainsets, optimization_results, alerts):
        """Generate daily operations report"""
        service_ready = sum(1 for t in trainsets if t.get('manual_override') or t['recommendation'] == 'Service')
        standby = sum(1 for t in trainsets if t.get('manual_override') or t['recommendation'] == 'Standby')
        ibl = sum(1 for t in trainsets if t.get('manual_override') or t['recommendation'] == 'IBL')
        report = {
            'title': 'Daily Operations Report',
            'timestamp': datetime.now(),
            'summary': {
                'total_trainsets': len(trainsets),
                'service_ready': service_ready,
                'standby': standby,
                'ibl_maintenance': ibl,
                'availability_rate': round(service_ready / len(trainsets) * 100, 1) if trainsets else 0
            },
            'fitness_status': {
                'all_valid': sum(1 for t in trainsets if t['fitness']['overall_valid']),
                'expiring_soon': sum(1 for t in trainsets if t['fitness']['days_until_expiry'] <= 2)
            },
            'maintenance_status': {
                'open_job_cards': sum(t['job_cards']['open'] for t in trainsets),
                'critical_priority': sum(1 for t in trainsets if t['job_cards']['priority'] == 'Critical')
            }
        }
        return report
    def _generate_maintenance_report(self, trainsets, optimization_results, alerts):
        """Generate maintenance planning report"""
        high_risk_trains = []
        for t in trainsets:
            wear_avg = sum(t['mileage']['component_wear'].values()) / 3
            if wear_avg > 70 or t['job_cards']['open'] > 2:
                high_risk_trains.append({
                    'id': t['id'],
                    'wear_score': wear_avg,
                    'open_jobs': t['job_cards']['open'],
                    'priority': t['job_cards']['priority']
                })
        report = {
            'title': 'Maintenance Planning Report',
            'timestamp': datetime.now(),
            'high_risk_trains': sorted(high_risk_trains, key=lambda x: x['wear_score'], reverse=True),
            'total_open_jobs': sum(t['job_cards']['open'] for t in trainsets),
            'preventive_maintenance_needed': sum(1 for t in trainsets if t['mileage']['since_maintenance'] > 8000),
            'critical_issues': sum(1 for t in trainsets if t['job_cards']['priority'] == 'Critical')
        }        
        return report
    def _generate_branding_report(self, trainsets, optimization_results, alerts):
        """Generate branding compliance report"""
        branding_stats = {}
        for t in trainsets:
            advertiser = t['branding']['advertiser'] or 'Unbranded'
            if advertiser not in branding_stats:
                branding_stats[advertiser] = {
                    'total_hours_required': 0,
                    'total_deficit': 0,
                    'train_count': 0,
                    'total_value': 0
                }
            branding_stats[advertiser]['total_hours_required'] += t['branding']['hours_required_today']
            branding_stats[advertiser]['total_deficit'] += t['branding']['exposure_deficit']
            branding_stats[advertiser]['train_count'] += 1
            branding_stats[advertiser]['total_value'] += t['branding']['contract_value']
        report = {
            'title': 'Branding Compliance Report',
            'timestamp': datetime.now(),
            'advertiser_stats': branding_stats,
            'total_exposure_deficit': sum(t['branding']['exposure_deficit'] for t in trainsets),
            'total_contract_value': sum(t['branding']['contract_value'] for t in trainsets),
            'trains_requiring_exposure': sum(1 for t in trainsets if t['branding']['hours_required_today'] > 0)
        }
        return report
    def _generate_optimization_report(self, trainsets, optimization_results, alerts):
        """Generate optimization performance report"""
        if not optimization_results:
            return None
        report = {
            'title': 'Optimization Performance Report',
            'timestamp': datetime.now(),
            'optimization_results': optimization_results,
            'constraint_compliance': {
                'service_target_met': optimization_results.get('service_ready', 0) >= optimization_results.get('target_service', 0),
                'ibl_within_limit': optimization_results.get('ibl_maintenance', 0) <= optimization_results.get('max_ibl', 5)
            },
            'conflict_resolution': len(optimization_results.get('conflicts', [])),
            'predicted_impact': {
                'punctuality_improvement': max(0, (optimization_results.get('punctuality_score', 0) - 98.5)),
                'cost_savings': optimization_results.get('cost_optimization', 0),
                'energy_savings': optimization_results.get('energy_savings', 0)
            }
        }
        return report
    def export_report_to_csv(self, report, filename_prefix):
        """Export report data to CSV format"""
        if not report:
            return None
        df_data = []
        if 'advertiser_stats' in report:
            for advertiser, stats in report['advertiser_stats'].items():
                df_data.append({
                    'advertiser': advertiser,
                    'trains_count': stats['train_count'],
                    'hours_required': stats['total_hours_required'],
                    'exposure_deficit': stats['total_deficit'],
                    'contract_value': stats['total_value']
                })
        elif 'high_risk_trains' in report:
            for train in report['high_risk_trains']:
                df_data.append(train)
        if df_data:
            df = pd.DataFrame(df_data)
            return df.to_csv(index=False)
        return None
# System Integration Manager