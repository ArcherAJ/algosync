from common_imports import *
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json
import requests
from dataclasses import dataclass, asdict
from enum import Enum
from mock_maximo_server import get_mock_server, start_mock_maximo_server

class MaximoWorkOrderStatus(Enum):
    """Maximo Work Order Status enumeration"""
    WAPPR = "WAPPR"  # Work Approved
    WMATL = "WMATL"  # Work Material
    WPLAN = "WPLAN"  # Work Planned
    WSCHD = "WSCHD"  # Work Scheduled
    INPRG = "INPRG"  # In Progress
    COMP = "COMP"    # Complete
    CANCEL = "CANCEL" # Cancelled

class MaximoAssetStatus(Enum):
    """Maximo Asset Status enumeration"""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    RETIRED = "RETIRED"
    MAINTENANCE = "MAINTENANCE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"

@dataclass
class MaximoAsset:
    """Maximo Asset data structure"""
    asset_id: str
    asset_num: str
    description: str
    asset_type: str
    location: str
    status: str
    manufacturer: str
    model: str
    serial_number: str
    installation_date: str
    warranty_expiry: str
    last_inspection: str
    next_inspection: str
    maintenance_cost: float
    replacement_cost: float
    criticality: str
    parent_asset: Optional[str] = None
    children_assets: List[str] = None
    
    def __post_init__(self):
        if self.children_assets is None:
            self.children_assets = []

@dataclass
class MaximoWorkOrder:
    """Maximo Work Order data structure"""
    work_order_id: str
    work_order_num: str
    description: str
    asset_id: str
    work_type: str
    priority: str
    status: str
    scheduled_start: str
    scheduled_finish: str
    actual_start: Optional[str] = None
    actual_finish: Optional[str] = None
    estimated_cost: float = 0.0
    actual_cost: float = 0.0
    labor_hours: float = 0.0
    material_cost: float = 0.0
    assigned_to: Optional[str] = None
    work_location: Optional[str] = None
    parent_wo: Optional[str] = None
    child_wos: List[str] = None
    
    def __post_init__(self):
        if self.child_wos is None:
            self.child_wos = []

@dataclass
class MaximoInventoryItem:
    """Maximo Inventory Item data structure"""
    item_id: str
    item_num: str
    description: str
    item_type: str
    unit_cost: float
    quantity_on_hand: int
    reorder_point: int
    max_quantity: int
    location: str
    supplier: str
    lead_time_days: int
    last_received: str
    next_reorder: str

class IBMMaximoIntegration:
    """
    IBM Maximo Integration Module for KMRL Train Induction Platform
    
    This module provides comprehensive integration with IBM Maximo for:
    - Asset Management (Trainsets, Stations, Equipment)
    - Work Order Management (Maintenance, Inspections, Repairs)
    - Inventory Management (Spare Parts, Materials)
    - Preventive Maintenance Scheduling
    - Cost Tracking and Analytics
    """
    
    def __init__(self, maximo_url: str = "http://localhost:9080/maximo", 
                 username: str = "maxadmin", password: str = "maxadmin"):
        """
        Initialize Maximo integration with mock server fallback
        
        Args:
            maximo_url: Maximo server URL
            username: Maximo username
            password: Maximo password
        """
        self.maximo_url = maximo_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
        # Cache for frequently accessed data
        self.asset_cache = {}
        self.work_order_cache = {}
        self.inventory_cache = {}
        
        # Integration status
        self.is_connected = False
        self.last_sync = None
        self.use_mock_server = False
        self.mock_server = None
        
    def connect(self) -> bool:
        """Test connection to Maximo server with mock fallback"""
        try:
            response = self.session.get(f"{self.maximo_url}/oslc/os/mxapiasset")
            self.is_connected = response.status_code == 200
            if self.is_connected:
                self.last_sync = datetime.now()
                print("✅ Connected to IBM Maximo successfully")
                self.use_mock_server = False
            return self.is_connected
        except Exception as e:
            print(f"❌ Failed to connect to Maximo: {e}")
            print("🔄 Switching to Mock Maximo Server...")
            
            # Initialize mock server
            self.mock_server = start_mock_maximo_server()
            self.use_mock_server = True
            self.is_connected = True
            self.last_sync = datetime.now()
            print("✅ Connected to Mock Maximo Server successfully")
            return True
    
    def create_trainset_asset(self, trainset_data: Dict) -> Optional[str]:
        """
        Create or update trainset asset in Maximo (with mock fallback)
        
        Args:
            trainset_data: Trainset information from KMRL system
            
        Returns:
            Asset ID if successful, None otherwise
        """
        try:
            asset_data = {
                "assetnum": trainset_data.get('id', ''),
                "description": f"KMRL Trainset {trainset_data.get('id', '')}",
                "assettype": "TRAINSET",
                "location": trainset_data.get('depot', 'Unknown Depot'),
                "status": self._map_operational_status(trainset_data.get('operational', {}).get('status', 'Available')),
                "manufacturer": "Alstom",
                "model": "Metro Train",
                "serialnumber": trainset_data.get('id', ''),
                "installdate": datetime.now().strftime('%Y-%m-%d'),
                "warrantyexpiration": (datetime.now() + timedelta(days=365*5)).strftime('%Y-%m-%d'),
                "lastinspection": datetime.now().strftime('%Y-%m-%d'),
                "nextinspection": (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
                "maintenancecost": self._calculate_maintenance_cost(trainset_data),
                "replacementcost": 50000000.0,  # 50 million INR
                "criticality": self._determine_criticality(trainset_data)
            }
            
            if self.use_mock_server and self.mock_server:
                # Use mock server
                result = self.mock_server.create_asset(asset_data)
                if result['status'] == 'success':
                    asset_id = result['assetnum']
                    self.asset_cache[asset_id] = asset_data
                    print(f"✅ Created trainset asset {asset_id} in Mock Maximo")
                    return asset_id
                else:
                    print(f"❌ Failed to create asset in mock server: {result['message']}")
                    return None
            else:
                # Use real Maximo server
                response = self.session.post(
                    f"{self.maximo_url}/oslc/os/mxapiasset",
                    json=asset_data
                )
                
                if response.status_code in [200, 201]:
                    asset_id = response.json().get('assetnum', trainset_data.get('id'))
                    self.asset_cache[asset_id] = asset_data
                    print(f"✅ Created trainset asset {asset_id} in Maximo")
                    return asset_id
                else:
                    print(f"❌ Failed to create asset: {response.text}")
                    return None
                
        except Exception as e:
            print(f"❌ Error creating trainset asset: {e}")
            return None
    
    def create_maintenance_work_order(self, trainset_id: str, maintenance_data: Dict) -> Optional[str]:
        """
        Create maintenance work order in Maximo
        
        Args:
            trainset_id: Trainset ID
            maintenance_data: Maintenance information
            
        Returns:
            Work Order ID if successful, None otherwise
        """
        try:
            work_order_data = {
                "wonum": f"WO-{trainset_id}-{datetime.now().strftime('%Y%m%d%H%M')}",
                "description": maintenance_data.get('description', f"Maintenance for {trainset_id}"),
                "assetnum": trainset_id,
                "worktype": maintenance_data.get('type', 'PM'),  # PM = Preventive Maintenance
                "priority": self._map_priority(maintenance_data.get('priority', 'Medium')),
                "status": MaximoWorkOrderStatus.WPLAN.value,
                "schedstart": maintenance_data.get('scheduled_start', datetime.now().strftime('%Y-%m-%d %H:%M')),
                "schedfinish": maintenance_data.get('scheduled_finish', (datetime.now() + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M')),
                "estcost": maintenance_data.get('estimated_cost', 10000.0),
                "worklocation": maintenance_data.get('location', 'Maintenance Depot'),
                "assignedto": maintenance_data.get('assigned_to', 'MAINTENANCE_TEAM')
            }
            
            response = self.session.post(
                f"{self.maximo_url}/oslc/os/mxapiworkorder",
                json=work_order_data
            )
            
            if response.status_code in [200, 201]:
                wo_id = response.json().get('wonum', work_order_data['wonum'])
                self.work_order_cache[wo_id] = work_order_data
                print(f"✅ Created work order {wo_id} in Maximo")
                return wo_id
            else:
                print(f"❌ Failed to create work order: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating work order: {e}")
            return None
    
    def update_asset_status(self, asset_id: str, status: str, additional_data: Dict = None) -> bool:
        """
        Update asset status in Maximo
        
        Args:
            asset_id: Asset ID
            status: New status
            additional_data: Additional data to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            update_data = {
                "status": status,
                "lastinspection": datetime.now().strftime('%Y-%m-%d')
            }
            
            if additional_data:
                update_data.update(additional_data)
            
            response = self.session.put(
                f"{self.maximo_url}/oslc/os/mxapiasset/{asset_id}",
                json=update_data
            )
            
            if response.status_code == 200:
                if asset_id in self.asset_cache:
                    self.asset_cache[asset_id].update(update_data)
                print(f"✅ Updated asset {asset_id} status to {status}")
                return True
            else:
                print(f"❌ Failed to update asset status: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error updating asset status: {e}")
            return False
    
    def get_asset_maintenance_history(self, asset_id: str) -> List[Dict]:
        """
        Get maintenance history for an asset
        
        Args:
            asset_id: Asset ID
            
        Returns:
            List of maintenance records
        """
        try:
            response = self.session.get(
                f"{self.maximo_url}/oslc/os/mxapiworkorder",
                params={"assetnum": asset_id, "status": "COMP"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('member', [])
            else:
                print(f"❌ Failed to get maintenance history: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting maintenance history: {e}")
            return []
    
    def get_preventive_maintenance_schedule(self, days_ahead: int = 30) -> List[Dict]:
        """
        Get preventive maintenance schedule
        
        Args:
            days_ahead: Number of days to look ahead
            
        Returns:
            List of scheduled maintenance activities
        """
        try:
            end_date = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')
            
            response = self.session.get(
                f"{self.maximo_url}/oslc/os/mxapiworkorder",
                params={
                    "worktype": "PM",
                    "status": "WSCHD",
                    "schedstart": f"<{end_date}"
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('member', [])
            else:
                print(f"❌ Failed to get PM schedule: {response.text}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting PM schedule: {e}")
            return []
    
    def create_inventory_item(self, item_data: Dict) -> Optional[str]:
        """
        Create inventory item in Maximo
        
        Args:
            item_data: Item information
            
        Returns:
            Item ID if successful, None otherwise
        """
        try:
            response = self.session.post(
                f"{self.maximo_url}/oslc/os/mxapiitem",
                json=item_data
            )
            
            if response.status_code in [200, 201]:
                item_id = response.json().get('itemnum', item_data.get('itemnum'))
                self.inventory_cache[item_id] = item_data
                print(f"✅ Created inventory item {item_id} in Maximo")
                return item_id
            else:
                print(f"❌ Failed to create inventory item: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating inventory item: {e}")
            return None
    
    def get_maintenance_cost_analytics(self, asset_id: str = None, months: int = 12) -> Dict:
        """
        Get maintenance cost analytics
        
        Args:
            asset_id: Specific asset ID (None for all assets)
            months: Number of months to analyze
            
        Returns:
            Cost analytics data
        """
        try:
            start_date = (datetime.now() - timedelta(days=months*30)).strftime('%Y-%m-%d')
            
            params = {
                "status": "COMP",
                "actualfinish": f">{start_date}"
            }
            
            if asset_id:
                params["assetnum"] = asset_id
            
            response = self.session.get(
                f"{self.maximo_url}/oslc/os/mxapiworkorder",
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                work_orders = data.get('member', [])
                
                # Calculate analytics
                total_cost = sum(wo.get('actualcost', 0) for wo in work_orders)
                avg_cost = total_cost / len(work_orders) if work_orders else 0
                
                return {
                    'total_cost': total_cost,
                    'average_cost': avg_cost,
                    'work_order_count': len(work_orders),
                    'cost_trend': self._calculate_cost_trend(work_orders),
                    'top_cost_drivers': self._identify_cost_drivers(work_orders)
                }
            else:
                print(f"❌ Failed to get cost analytics: {response.text}")
                return {}
                
        except Exception as e:
            print(f"❌ Error getting cost analytics: {e}")
            return {}
    
    def sync_with_kmrl_system(self, trainsets: List[Dict]) -> Dict:
        """
        Synchronize Maximo with KMRL system data
        
        Args:
            trainsets: List of trainset data from KMRL
            
        Returns:
            Sync results summary
        """
        sync_results = {
            'assets_created': 0,
            'assets_updated': 0,
            'work_orders_created': 0,
            'errors': []
        }
        
        try:
            for trainset in trainsets:
                trainset_id = trainset.get('id', '')
                
                # Create or update asset
                if trainset_id not in self.asset_cache:
                    asset_id = self.create_trainset_asset(trainset)
                    if asset_id:
                        sync_results['assets_created'] += 1
                    else:
                        sync_results['errors'].append(f"Failed to create asset for {trainset_id}")
                else:
                    # Update existing asset
                    status = self._map_operational_status(trainset.get('operational', {}).get('status', 'Available'))
                    if self.update_asset_status(trainset_id, status):
                        sync_results['assets_updated'] += 1
                
                # Create work orders for maintenance needs
                if trainset.get('job_cards', {}).get('open', 0) > 0:
                    maintenance_data = {
                        'description': f"Maintenance required for {trainset_id}",
                        'type': 'CM',  # Corrective Maintenance
                        'priority': 'High' if trainset.get('job_cards', {}).get('open', 0) > 2 else 'Medium',
                        'estimated_cost': self._calculate_maintenance_cost(trainset),
                        'location': trainset.get('depot', 'Maintenance Depot')
                    }
                    
                    wo_id = self.create_maintenance_work_order(trainset_id, maintenance_data)
                    if wo_id:
                        sync_results['work_orders_created'] += 1
            
            self.last_sync = datetime.now()
            print(f"✅ Sync completed: {sync_results}")
            return sync_results
            
        except Exception as e:
            print(f"❌ Error during sync: {e}")
            sync_results['errors'].append(str(e))
            return sync_results
    
    def _map_operational_status(self, status: str) -> str:
        """Map KMRL operational status to Maximo asset status"""
        status_mapping = {
            'Available': MaximoAssetStatus.ACTIVE.value,
            'Standby': MaximoAssetStatus.ACTIVE.value,
            'Maintenance': MaximoAssetStatus.MAINTENANCE.value,
            'IBL': MaximoAssetStatus.OUT_OF_SERVICE.value
        }
        return status_mapping.get(status, MaximoAssetStatus.ACTIVE.value)
    
    def _map_priority(self, priority: str) -> str:
        """Map priority levels"""
        priority_mapping = {
            'Low': '3',
            'Medium': '2',
            'High': '1',
            'Critical': '1'
        }
        return priority_mapping.get(priority, '2')
    
    def _calculate_maintenance_cost(self, trainset_data: Dict) -> float:
        """Calculate estimated maintenance cost based on trainset condition"""
        base_cost = 5000.0
        job_cards = trainset_data.get('job_cards', {}).get('open', 0)
        wear_factor = sum(trainset_data.get('mileage', {}).get('component_wear', {}).values()) / 300
        
        return base_cost + (job_cards * 2000) + (wear_factor * 3000)
    
    def _determine_criticality(self, trainset_data: Dict) -> str:
        """Determine asset criticality"""
        reliability = trainset_data.get('operational', {}).get('reliability_score', 80)
        job_cards = trainset_data.get('job_cards', {}).get('open', 0)
        
        if reliability < 60 or job_cards > 3:
            return 'HIGH'
        elif reliability < 80 or job_cards > 1:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _calculate_cost_trend(self, work_orders: List[Dict]) -> List[float]:
        """Calculate cost trend over time"""
        # Group by month and calculate monthly costs
        monthly_costs = {}
        for wo in work_orders:
            finish_date = wo.get('actualfinish', '')
            if finish_date:
                month_key = finish_date[:7]  # YYYY-MM
                monthly_costs[month_key] = monthly_costs.get(month_key, 0) + wo.get('actualcost', 0)
        
        return list(monthly_costs.values())
    
    def _identify_cost_drivers(self, work_orders: List[Dict]) -> List[Dict]:
        """Identify top cost drivers"""
        cost_by_type = {}
        for wo in work_orders:
            wo_type = wo.get('worktype', 'Unknown')
            cost = wo.get('actualcost', 0)
            cost_by_type[wo_type] = cost_by_type.get(wo_type, 0) + cost
        
        return sorted(cost_by_type.items(), key=lambda x: x[1], reverse=True)[:5]

class MaximoDataAdapter:
    """
    Adapter class to convert between KMRL system data and Maximo data formats
    """
    
    @staticmethod
    def trainset_to_maximo_asset(trainset_data: Dict) -> MaximoAsset:
        """Convert KMRL trainset data to Maximo asset format"""
        return MaximoAsset(
            asset_id=trainset_data.get('id', ''),
            asset_num=trainset_data.get('id', ''),
            description=f"KMRL Trainset {trainset_data.get('id', '')}",
            asset_type="TRAINSET",
            location=trainset_data.get('depot', 'Unknown Depot'),
            status=trainset_data.get('operational', {}).get('status', 'Available'),
            manufacturer="Alstom",
            model="Metro Train",
            serial_number=trainset_data.get('id', ''),
            installation_date=datetime.now().strftime('%Y-%m-%d'),
            warranty_expiry=(datetime.now() + timedelta(days=365*5)).strftime('%Y-%m-%d'),
            last_inspection=datetime.now().strftime('%Y-%m-%d'),
            next_inspection=(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
            maintenance_cost=0.0,  # Will be calculated
            replacement_cost=50000000.0,
            criticality="MEDIUM"
        )
    
    @staticmethod
    def maximo_asset_to_trainset(asset_data: Dict) -> Dict:
        """Convert Maximo asset data to KMRL trainset format"""
        return {
            'id': asset_data.get('assetnum', ''),
            'depot': asset_data.get('location', ''),
            'operational': {
                'status': asset_data.get('status', 'Available'),
                'reliability_score': 80  # Default value
            },
            'fitness': {
                'rolling_stock': True,
                'signalling': True,
                'telecom': True,
                'overall_valid': True
            },
            'job_cards': {
                'open': 0
            },
            'mileage': {
                'total_km': 0,
                'component_wear': {
                    'brake_pads': 50,
                    'bogies': 50,
                    'hvac': 50
                }
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Initialize Maximo integration
    maximo = IBMMaximoIntegration()
    
    # Test connection
    if maximo.connect():
        print("✅ Maximo integration initialized successfully")
        
        # Example trainset data
        sample_trainset = {
            'id': 'KMRL-001',
            'depot': 'Aluva Depot',
            'operational': {
                'status': 'Available',
                'reliability_score': 85
            },
            'job_cards': {
                'open': 1
            },
            'mileage': {
                'component_wear': {
                    'brake_pads': 60,
                    'bogies': 55,
                    'hvac': 70
                }
            }
        }
        
        # Create asset
        asset_id = maximo.create_trainset_asset(sample_trainset)
        print(f"Created asset: {asset_id}")
        
        # Create work order
        maintenance_data = {
            'description': 'Routine maintenance',
            'type': 'PM',
            'priority': 'Medium',
            'estimated_cost': 15000.0
        }
        
        wo_id = maximo.create_maintenance_work_order(asset_id, maintenance_data)
        print(f"Created work order: {wo_id}")
        
    else:
        print("❌ Failed to connect to Maximo")
