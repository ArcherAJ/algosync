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

class PredictiveMaintenanceModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
    def prepare_training_data(self, historical_data):
        """Prepare training data from historical records"""
        features = []
        labels = []
        for record in historical_data:
            # Feature engineering
            feature_vector = [
                record['mileage']['total_km'],
                record['mileage']['since_maintenance'],
                sum(record['mileage']['component_wear'].values()) / 3,  # Average wear
                record['job_cards']['open'],
                1 if record['fitness']['rolling_stock'] else 0,
                1 if record['fitness']['signalling'] else 0,
                1 if record['fitness']['telecom'] else 0,
                (record['operational']['last_service'] - datetime.now()).days if record['operational']['last_service'] else 30,
                record['operational']['reliability_score']
            ]
            # Label: days until next maintenance (simplified)
            maintenance_urgency = (
                (100 - record['operational']['reliability_score']) / 10 +
                record['job_cards']['open'] * 2 +
                sum(record['mileage']['component_wear'].values()) / 30
            )
            label = max(1, min(30, 30 - maintenance_urgency))
            features.append(feature_vector)
            labels.append(label)
        return np.array(features), np.array(labels)
    def train_model(self, historical_data):
        """Train the predictive maintenance model"""
        try:
            features, labels = self.prepare_training_data(historical_data)
            if len(features) < 10:
                # Not enough data for proper training
                self.is_trained = False
                return False
            # Scale features
            features_scaled = self.scaler.fit_transform(features)
            # Train Random Forest model
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.model.fit(features_scaled, labels)
            self.is_trained = True
            return True
        except Exception as e:
            print(f"Error training model: {e}")
            self.is_trained = False
            return False
    def predict_maintenance(self, trainsets):
        """Predict maintenance needs for all trainsets"""
        if not self.is_trained or self.model is None:
            return self._fallback_predictions(trainsets)
        predictions = []
        for trainset in trainsets:
            try:
                # Prepare features for prediction
                features = np.array([[
                    trainset['mileage']['total_km'],
                    trainset['mileage']['since_maintenance'],
                    sum(trainset['mileage']['component_wear'].values()) / 3,
                    trainset['job_cards']['open'],
                    1 if trainset['fitness']['rolling_stock'] else 0,
                    1 if trainset['fitness']['signalling'] else 0,
                    1 if trainset['fitness']['telecom'] else 0,
                    (trainset['operational']['last_service'] - datetime.now()).days if trainset['operational']['last_service'] else 30,
                    trainset['operational']['reliability_score']
                ]])
                # Scale and predict
                features_scaled = self.scaler.transform(features)
                days_until_maintenance = self.model.predict(features_scaled)[0]
                # Calculate risk score
                risk_score = min(100, max(0, 100 - (days_until_maintenance / 30 * 100)))
                # Determine recommendation
                if risk_score > 75:
                    action = 'Schedule Immediately'
                    priority = 'High'
                elif risk_score > 50:
                    action = 'Schedule Soon'
                    priority = 'Medium'
                elif risk_score > 25:
                    action = 'Monitor Closely'
                    priority = 'Low'
                else:
                    action = 'OK'
                    priority = 'None'
                predictions.append({
                    'trainset_id': trainset['id'],
                    'risk_score': round(risk_score, 1),
                    'days_until_maintenance': round(max(0, days_until_maintenance), 1),
                    'recommended_action': action,
                    'priority': priority,
                    'confidence': 'High' if self.is_trained else 'Low'
                })
            except Exception as e:
                # Fallback if prediction fails
                predictions.append(self._fallback_prediction(trainset))
        return pd.DataFrame(predictions)
    def _fallback_predictions(self, trainsets):
        """Fallback predictions when model is not trained"""
        return pd.DataFrame([self._fallback_prediction(t) for t in trainsets])
    def _fallback_prediction(self, trainset):
        """Simple heuristic-based fallback prediction"""
        wear_avg = sum(trainset['mileage']['component_wear'].values()) / 3
        mileage_ratio = trainset['mileage']['since_maintenance'] / 10000
        risk_score = min(100, max(0, wear_avg * 0.7 + mileage_ratio * 30))
        days_until_maintenance = max(0, 30 - (risk_score / 100 * 30))
        if risk_score > 70:
            action = 'Schedule Soon'
            priority = 'High'
        elif risk_score > 40:
            action = 'Monitor'
            priority = 'Medium'
        else:
            action = 'OK'
            priority = 'Low'
        return {
            'trainset_id': trainset['id'],
            'risk_score': round(risk_score, 1),
            'days_until_maintenance': round(days_until_maintenance, 1),
            'recommended_action': action,
            'priority': priority,
            'confidence': 'Low (Heuristic)'
        }
# Real-time Data Integration