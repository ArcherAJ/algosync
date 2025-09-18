from common_imports import *

class MultiObjectiveOptimizer:
    def __init__(self):
        self.weights = {
            'punctuality': 0.25,
            'cost_efficiency': 0.20,
            'branding_compliance': 0.15,
            'maintenance_risk': 0.20,
            'energy_efficiency': 0.10,
            'operational_flexibility': 0.10
        }
        self.ml_model = None  # Will be set by system manager
        
    def set_ml_model(self, ml_model):
        """Set the ML model for enhanced optimization"""
        self.ml_model = ml_model
        
    def calculate_objective_scores(self, trainset):
        """Calculate individual objective scores for a trainset"""
        scores = {}
        # Punctuality score (based on fitness and reliability)
        scores['punctuality'] = (
            (1.0 if trainset['fitness']['overall_valid'] else 0.3) *
            (trainset['operational']['reliability_score'] / 100)
        )
        # Cost efficiency (lower maintenance needs = better)
        maintenance_penalty = min(1.0, trainset['job_cards']['open'] * 0.2 + 
                                 (0.5 if trainset['cleaning']['deep_clean_due'] else 0))
        scores['cost_efficiency'] = 1.0 - maintenance_penalty
        # Branding compliance
        branding_score = 0.5  # Base score
        if trainset['branding']['hours_required_today'] > 0:
            branding_score += 0.3
        if trainset['branding']['exposure_deficit'] > 10:
            branding_score += 0.2
        scores['branding_compliance'] = min(1.0, branding_score)
        # Maintenance risk (based on component wear and mileage)
        wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3 / 100
        mileage_risk = min(1.0, trainset['mileage']['since_maintenance'] / 10000)
        scores['maintenance_risk'] = 1.0 - max(wear_avg, mileage_risk)
        # Energy efficiency (less shunting = better)
        energy_score = 1.0 - (trainset['stabling']['shunting_moves_required'] * 0.2)
        scores['energy_efficiency'] = energy_score
        # Operational flexibility (status and availability)
        if trainset['operational']['status'] == 'Available':
            flexibility = 0.8
        elif trainset['operational']['status'] == 'Standby':
            flexibility = 0.5
        else:
            flexibility = 0.2
        scores['operational_flexibility'] = flexibility
        
        return scores
        
    def calculate_overall_score(self, trainset):
        """Calculate weighted overall score for optimization"""
        objective_scores = self.calculate_objective_scores(trainset)
        
        # Enhanced scoring with ML predictions if available
        if self.ml_model and self.ml_model.is_trained:
            try:
                # Get ML-based maintenance prediction
                ml_prediction = self.ml_model.predict_maintenance([trainset])
                if not ml_prediction.empty:
                    risk_score = ml_prediction.iloc[0]['risk_score']
                    # Adjust maintenance risk score based on ML prediction
                    objective_scores['maintenance_risk'] = 1.0 - (risk_score / 100)
            except Exception as e:
                print(f"ML prediction failed: {e}")
        
        weighted_score = sum(
            objective_scores[obj] * self.weights[obj] 
            for obj in self.weights
        )
        return weighted_score, objective_scores
        
    def optimize_fleet_assignment(self, trainsets, constraints):
        """ Optimize fleet assignment using a weighted multi-objective approach """
        optimized_trainsets = trainsets.copy()
        # Calculate scores for all trainsets
        for trainset in optimized_trainsets:
            overall_score, objective_scores = self.calculate_overall_score(trainset)
            trainset['optimization_score'] = overall_score
            trainset['objective_scores'] = objective_scores
        # Sort by optimization score
        optimized_trainsets.sort(key=lambda x: x['optimization_score'], reverse=True)
        # Apply constraints
        service_count = sum(1 for t in optimized_trainsets if t['recommendation'] == 'Service')
        target_service = constraints.get('service_target', min(15, len(optimized_trainsets)))
        max_ibl = constraints.get('max_ibl', 5)
        # Reset all recommendations first
        for trainset in optimized_trainsets:
            trainset['recommendation'] = 'Standby'
        # Assign Service status to top trainsets
        service_candidates = [t for t in optimized_trainsets 
                             if t['fitness']['overall_valid'] and 
                             t['operational']['status'] != 'IBL']
        for i in range(min(target_service, len(service_candidates))):
            service_candidates[i]['recommendation'] = 'Service'
            service_candidates[i]['optimization_note'] = 'Optimized for service'
        # Assign IBL status based on constraints and needs
        ibl_candidates = [t for t in optimized_trainsets 
                         if not t['fitness']['overall_valid'] or 
                         t['operational']['status'] == 'IBL' or
                         t['job_cards']['open'] > 2]
        ibl_candidates.sort(key=lambda x: x['optimization_score']) 
        for i in range(min(max_ibl, len(ibl_candidates))):
            ibl_candidates[i]['recommendation'] = 'IBL'
            ibl_candidates[i]['optimization_note'] = 'Required maintenance'
        # Check for conflicts
        conflicts = []
        for t in optimized_trainsets:
            if t['recommendation'] == 'Service' and not t['fitness']['overall_valid']:
                conflicts.append(f"{t['id']} recommended for service but has invalid fitness")
            if t['recommendation'] == 'Service' and t['operational']['status'] == 'IBL':
                conflicts.append(f"{t['id']} recommended for service but is in IBL")
        # Calculate overall metrics
        service_ready = sum(1 for t in optimized_trainsets if t['recommendation'] == 'Service')
        standby = sum(1 for t in optimized_trainsets if t['recommendation'] == 'Standby')
        ibl = sum(1 for t in optimized_trainsets if t['recommendation'] == 'IBL')
        return optimized_trainsets, conflicts, service_ready, standby, ibl