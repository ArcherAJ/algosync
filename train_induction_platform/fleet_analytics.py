from common_imports import *

class FleetPerformanceAnalytics:
    """
    ML-powered fleet performance analytics system
    Uses clustering and anomaly detection for fleet insights
    """
    
    def __init__(self):
        self.clustering_model = None
        self.anomaly_detector = None
        self.performance_scorer = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.cluster_centers = None
        
    def prepare_fleet_data(self, trainsets):
        """Prepare fleet data for analytics"""
        fleet_data = []
        
        for trainset in trainsets:
            # Calculate performance metrics
            wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
            efficiency_score = trainset['operational']['reliability_score'] / 100
            maintenance_urgency = trainset['job_cards']['open']
            fitness_score = sum([
                1 if trainset['fitness']['rolling_stock'] else 0,
                1 if trainset['fitness']['signalling'] else 0,
                1 if trainset['fitness']['telecom'] else 0
            ]) / 3
            
            # Create feature vector
            feature_vector = [
                trainset['mileage']['total_km'],
                trainset['mileage']['since_maintenance'],
                wear_avg,
                maintenance_urgency,
                efficiency_score,
                fitness_score,
                trainset['operational']['reliability_score'],
                trainset['ai_score'] if 'ai_score' in trainset else 50
            ]
            
            fleet_data.append({
                'trainset_id': trainset['id'],
                'features': feature_vector,
                'depot': trainset.get('depot', 'Unknown'),
                'status': trainset['operational']['status']
            })
        
        return fleet_data
    
    def train_models(self, trainsets):
        """Train clustering and anomaly detection models"""
        try:
            fleet_data = self.prepare_fleet_data(trainsets)
            if len(fleet_data) < 10:
                self.is_trained = False
                return False
            
            # Extract features
            features = np.array([item['features'] for item in fleet_data])
            
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            
            # Train clustering model (K-Means)
            self.clustering_model = KMeans(n_clusters=4, random_state=42)
            cluster_labels = self.clustering_model.fit_predict(features_scaled)
            self.cluster_centers = self.clustering_model.cluster_centers_
            
            # Train anomaly detector
            self.anomaly_detector = IsolationForest(contamination=0.1, random_state=42)
            anomaly_labels = self.anomaly_detector.fit_predict(features_scaled)
            
            # Train performance scorer (ensemble)
            performance_scores = []
            for i, item in enumerate(fleet_data):
                # Calculate performance score based on multiple factors
                score = (
                    item['features'][4] * 0.3 +  # efficiency_score
                    item['features'][5] * 0.3 +  # fitness_score
                    (100 - item['features'][3]) / 100 * 0.2 +  # maintenance (inverted)
                    (100 - item['features'][2]) / 100 * 0.2    # wear (inverted)
                ) * 100
                performance_scores.append(score)
            
            # Train performance prediction model
            self.performance_scorer = RandomForestRegressor(n_estimators=100, random_state=42)
            self.performance_scorer.fit(features_scaled, performance_scores)
            
            # Store cluster assignments
            for i, item in enumerate(fleet_data):
                item['cluster'] = cluster_labels[i]
                item['is_anomaly'] = anomaly_labels[i] == -1
                item['performance_score'] = performance_scores[i]
            
            self.fleet_data = fleet_data
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error training fleet analytics models: {e}")
            self.is_trained = False
            return False
    
    def get_fleet_clusters(self):
        """Get fleet performance clusters"""
        if not self.is_trained:
            return None
        
        clusters = {}
        for item in self.fleet_data:
            cluster_id = item['cluster']
            if cluster_id not in clusters:
                clusters[cluster_id] = {
                    'trainsets': [],
                    'avg_performance': 0,
                    'cluster_characteristics': {}
                }
            clusters[cluster_id]['trainsets'].append(item)
        
        # Calculate cluster characteristics
        for cluster_id, cluster_data in clusters.items():
            trainsets = cluster_data['trainsets']
            avg_features = np.mean([t['features'] for t in trainsets], axis=0)
            avg_performance = np.mean([t['performance_score'] for t in trainsets])
            
            clusters[cluster_id]['avg_performance'] = avg_performance
            clusters[cluster_id]['cluster_characteristics'] = {
                'avg_mileage': avg_features[0],
                'avg_wear': avg_features[2],
                'avg_maintenance_urgency': avg_features[3],
                'avg_efficiency': avg_features[4],
                'avg_fitness': avg_features[5],
                'cluster_size': len(trainsets)
            }
        
        return clusters
    
    def get_anomalies(self):
        """Get anomalous trainsets"""
        if not self.is_trained:
            return None
        
        anomalies = [item for item in self.fleet_data if item['is_anomaly']]
        
        # Sort by performance score (worst first)
        anomalies.sort(key=lambda x: x['performance_score'])
        
        return anomalies
    
    def get_performance_ranking(self):
        """Get fleet performance ranking"""
        if not self.is_trained:
            return None
        
        # Sort by performance score
        ranked_fleet = sorted(self.fleet_data, key=lambda x: x['performance_score'], reverse=True)
        
        return ranked_fleet
    
    def predict_performance(self, trainset):
        """Predict performance for a specific trainset"""
        if not self.is_trained or self.performance_scorer is None:
            return None
        
        try:
            # Prepare features
            wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
            efficiency_score = trainset['operational']['reliability_score'] / 100
            fitness_score = sum([
                1 if trainset['fitness']['rolling_stock'] else 0,
                1 if trainset['fitness']['signalling'] else 0,
                1 if trainset['fitness']['telecom'] else 0
            ]) / 3
            
            features = np.array([[
                trainset['mileage']['total_km'],
                trainset['mileage']['since_maintenance'],
                wear_avg,
                trainset['job_cards']['open'],
                efficiency_score,
                fitness_score,
                trainset['operational']['reliability_score'],
                trainset.get('ai_score', 50)
            ]])
            
            features_scaled = self.scaler.transform(features)
            predicted_performance = self.performance_scorer.predict(features_scaled)[0]
            
            return max(0, min(100, predicted_performance))
            
        except Exception as e:
            print(f"Performance prediction error: {e}")
            return None
    
    def get_fleet_insights(self):
        """Get comprehensive fleet insights"""
        if not self.is_trained:
            return None
        
        clusters = self.get_fleet_clusters()
        anomalies = self.get_anomalies()
        ranking = self.get_performance_ranking()
        
        # Calculate overall metrics
        total_trainsets = len(self.fleet_data)
        avg_performance = np.mean([item['performance_score'] for item in self.fleet_data])
        high_performers = len([item for item in self.fleet_data if item['performance_score'] > 80])
        low_performers = len([item for item in self.fleet_data if item['performance_score'] < 40])
        
        # Depot analysis
        depot_analysis = {}
        for item in self.fleet_data:
            depot = item['depot']
            if depot not in depot_analysis:
                depot_analysis[depot] = {
                    'trainsets': [],
                    'avg_performance': 0,
                    'count': 0
                }
            depot_analysis[depot]['trainsets'].append(item)
            depot_analysis[depot]['count'] += 1
        
        for depot, data in depot_analysis.items():
            data['avg_performance'] = np.mean([t['performance_score'] for t in data['trainsets']])
        
        # Status analysis
        status_analysis = {}
        for item in self.fleet_data:
            status = item['status']
            if status not in status_analysis:
                status_analysis[status] = {
                    'count': 0,
                    'avg_performance': 0,
                    'trainsets': []
                }
            status_analysis[status]['trainsets'].append(item)
            status_analysis[status]['count'] += 1
        
        for status, data in status_analysis.items():
            data['avg_performance'] = np.mean([t['performance_score'] for t in data['trainsets']])
        
        return {
            'overall_metrics': {
                'total_trainsets': total_trainsets,
                'avg_performance': round(avg_performance, 2),
                'high_performers': high_performers,
                'low_performers': low_performers,
                'anomaly_count': len(anomalies)
            },
            'clusters': clusters,
            'anomalies': anomalies[:10],  # Top 10 anomalies
            'top_performers': ranking[:10],  # Top 10 performers
            'depot_analysis': depot_analysis,
            'status_analysis': status_analysis,
            'recommendations': self._generate_recommendations(clusters, anomalies, depot_analysis)
        }
    
    def _generate_recommendations(self, clusters, anomalies, depot_analysis):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Cluster-based recommendations
        for cluster_id, cluster_data in clusters.items():
            if cluster_data['avg_performance'] < 50:
                recommendations.append(f"Cluster {cluster_id}: Low performance cluster with {cluster_data['cluster_characteristics']['cluster_size']} trainsets - requires immediate attention")
        
        # Anomaly-based recommendations
        if len(anomalies) > 0:
            recommendations.append(f"Found {len(anomalies)} anomalous trainsets - investigate maintenance and operational issues")
        
        # Depot-based recommendations
        for depot, data in depot_analysis.items():
            if data['avg_performance'] < 60:
                recommendations.append(f"Depot {depot}: Below-average performance ({data['avg_performance']:.1f}) - review operational procedures")
        
        return recommendations
    
    def get_model_performance(self):
        """Get model performance metrics"""
        if not self.is_trained:
            return None
        
        return {
            'is_trained': self.is_trained,
            'clustering_model': 'K-Means (4 clusters)',
            'anomaly_detector': 'Isolation Forest',
            'performance_scorer': 'Random Forest Regressor',
            'total_trainsets_analyzed': len(self.fleet_data) if hasattr(self, 'fleet_data') else 0
        }
    
    def export_fleet_report(self):
        """Export comprehensive fleet report"""
        if not self.is_trained:
            return None
        
        insights = self.get_fleet_insights()
        
        # Create DataFrame for export
        export_data = []
        for item in self.fleet_data:
            export_data.append({
                'trainset_id': item['trainset_id'],
                'depot': item['depot'],
                'status': item['status'],
                'cluster': item['cluster'],
                'is_anomaly': item['is_anomaly'],
                'performance_score': item['performance_score'],
                'total_km': item['features'][0],
                'since_maintenance': item['features'][1],
                'avg_wear': item['features'][2],
                'maintenance_urgency': item['features'][3],
                'efficiency': item['features'][4],
                'fitness': item['features'][5]
            })
        
        df = pd.DataFrame(export_data)
        return df, insights
