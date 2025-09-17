import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random
from typing import List, Dict, Any, Tuple

class TimetableGenerator:
    def __init__(self):
        start_time = datetime.strptime("05:00", "%H:%M")
        end_time = datetime.strptime("00:00", "%H:%M") + timedelta(days=1)  # next day midnight
        slot_length = timedelta(minutes=30)

        self.time_slots = []
        while start_time < end_time:
            slot_end = start_time + slot_length
            self.time_slots.append(f"{start_time.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}")
            start_time = slot_end
        self.line_routes = {
            "Aluva-Kakkanad": ["Aluva", "Pulinchodu", "Companypady", "Ambattukavu", "Muttom", "Kalamassery", "CUSAT", "Pathadipalam", 
                              "Edapally", "Changampuzha Park", "Palarivattom", "JLN Stadium", "Kaloor", "Lissie", "MG Road", 
                              "Maharaja's College", "Ernakulam South", "Kadavanthra", "Elamkulam", "Vytilla", "Thaikoodam", "Petta", 
                              "Vadakkekotta", "SN Junction", "Kakkanad"],
            "Thrippunithura-Vytilla": ["Thrippunithura", "Vadakkekotta", "Petta", "SN Junction", "Kakkanad", "Kalamassery"]
        }
    
    def generate_timetable(self, trainsets: List[Dict], constraints: Dict) -> List[Dict]:
        """Generate timetable based on optimized train assignments"""
        service_trains = [t for t in trainsets if t['recommendation'] == 'Service']
        
        # Sort service trains by AI score (highest first)
        service_trains.sort(key=lambda x: x['ai_score'], reverse=True)
        
        # Determine number of trains needed per time slot based on historical demand
        peak_hours = ["07:00-08:00", "08:00-09:00", "17:00-18:00", "18:00-19:00"]
        off_peak_hours = ["05:00-06:00", "06:00-07:00", "09:00-22:00"]  # Excluding peak
        
        timetable = []
        
        # Assign trains to time slots based on their readiness and demand
        train_index = 0
        for time_slot in self.time_slots:
            # Determine how many trains needed for this time slot
            if time_slot in peak_hours:
                trains_needed = min(15, len(service_trains))  # Max capacity during peak
            else:
                trains_needed = min(10, len(service_trains))  # Reduced during off-peak
            
            # Select trains for this time slot
            slot_trains = []
            for i in range(trains_needed):
                if train_index >= len(service_trains):
                    train_index = 0  # Loop back to start if we run out of trains
                
                train = service_trains[train_index]
                slot_trains.append({
                    'trainset_id': train['id'],
                    'depot': train['depot'],
                    'route': self._assign_route(train),
                    'capacity': self._calculate_capacity(train),
                    'ai_score': train['ai_score']
                })
                train_index += 1
            
            timetable.append({
                'time_slot': time_slot,
                'trains': slot_trains,
                'total_trains': len(slot_trains),
                'peak_hour': time_slot in peak_hours
            })
        
        return timetable
    
    def _assign_route(self, train: Dict) -> str:
        """Assign route based on depot and availability"""
        if train['depot'] == 'Aluva Depot':
            return "Aluva-Kakkanad"
        else:  # Petta Depot
            return random.choice(["Aluva-Kakkanad", "Thrippunithura-Vytilla"])
    
    def _calculate_capacity(self, train: Dict) -> int:
        """Calculate capacity based on train condition"""
        base_capacity = 300  # Standard capacity
        reliability_factor = train['operational']['reliability_score'] / 100
        
        # Reduce capacity if high wear or maintenance issues
        wear_avg = sum(train['mileage']['component_wear'].values()) / 3
        if wear_avg > 70:
            reliability_factor *= 0.9
        if train['job_cards']['open'] > 0:
            reliability_factor *= 0.95
            
        return int(base_capacity * reliability_factor)