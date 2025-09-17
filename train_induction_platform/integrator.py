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
from utils import calculate_ai_score

class RealTimeDataIntegrator:
    def __init__(self):
        self.data_sources = {
            'maximo': {'connected': False, 'last_update': None},
            'iot_sensors': {'connected': False, 'last_update': None},
            'fitness_certs': {'connected': False, 'last_update': None}
        }
    def connect_to_maximo(self, trainsets):
        """Simulate connecting to IBM Maximo and updating job card status"""
        updated_count = 0
        for trainset in trainsets:
            if random.random() < 0.3:  # 30% chance of update from Maximo
                # Simulate job card updates
                change = random.randint(-1, 2)
                new_count = max(0, trainset['job_cards']['open'] + change)
                if new_count != trainset['job_cards']['open']:
                    trainset['job_cards']['open'] = new_count
                    updated_count += 1
                # Simulate priority changes
                if random.random() < 0.2:
                    trainset['job_cards']['priority'] = random.choice(['Low', 'Medium', 'High', 'Critical'])
                    updated_count += 1
        self.data_sources['maximo']['last_update'] = datetime.now()
        self.data_sources['maximo']['connected'] = True
        return trainsets, updated_count
    def connect_to_iot_sensors(self, trainsets):
        """Simulate IoT sensor data updates"""
        updated_count = 0
        for trainset in trainsets:
            if random.random() < 0.4:  # 40% chance of sensor update
                # Update component wear based on recent operation
                wear_increase = random.uniform(0.1, 2.0)
                for component in trainset['mileage']['component_wear']:
                    trainset['mileage']['component_wear'][component] = min(
                        100, trainset['mileage']['component_wear'][component] + wear_increase
                    )
                # Update mileage
                daily_km = random.randint(50, 300)
                trainset['mileage']['total_km'] += daily_km
                trainset['mileage']['since_maintenance'] += daily_km
                updated_count += 1
        self.data_sources['iot_sensors']['last_update'] = datetime.now()
        self.data_sources['iot_sensors']['connected'] = True
        return trainsets, updated_count
    def connect_to_fitness_db(self, trainsets):
        """Simulate fitness certificate database updates"""
        updated_count = 0
        for trainset in trainsets:
            if random.random() < 0.25:  # 25% chance of fitness update
                # Simulate certificate expiry/extension
                if random.random() < 0.1:  # 10% chance of expiry
                    department = random.choice(['rolling_stock', 'signalling', 'telecom'])
                    trainset['fitness'][department] = False
                    updated_count += 1
                # Simplicate certificate renewal
                if random.random() < 0.15 and not all([trainset['fitness']['rolling_stock'], 
                                                     trainset['fitness']['signalling'], 
                                                     trainset['fitness']['telecom']]):
                    # Renew expired certificates
                    for dept in ['rolling_stock', 'signalling', 'telecom']:
                        if not trainset['fitness'][dept]:
                            trainset['fitness'][dept] = True
                            updated_count += 1
                # Update expiry dates
                if random.random() < 0.2:
                    days_change = random.randint(-2, 7)
                    new_expiry = trainset['fitness']['expires_at'] + timedelta(days=days_change)
                    trainset['fitness']['expires_at'] = new_expiry
                    trainset['fitness']['days_until_expiry'] = max(0, (new_expiry - datetime.now()).days)
                    updated_count += 1
        self.data_sources['fitness_certs']['last_update'] = datetime.now()
        self.data_sources['fitness_certs']['connected'] = True
        return trainsets, updated_count
    def refresh_all_data(self, trainsets):
        """Refresh data from all sources"""
        total_updates = 0
        trainsets, updates = self.connect_to_maximo(trainsets)
        total_updates += updates
        trainsets, updates = self.connect_to_iot_sensors(trainsets)
        total_updates += updates
        trainsets, updates = self.connect_to_fitness_db(trainsets)
        total_updates += updates
        # Recalculate scores after updates
        for trainset in trainsets:
            score, reasons = calculate_ai_score(trainset)
            trainset['ai_score'] = score
            trainset['score_reasons'] = reasons
        return trainsets, total_updates
# Alert & Notification System