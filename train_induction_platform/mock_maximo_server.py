from common_imports import *
from typing import Dict, List, Optional, Any
import json
import threading
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class MockMaximoAsset:
    """Mock Maximo Asset data structure"""
    assetnum: str
    description: str
    assettype: str
    location: str
    status: str
    manufacturer: str
    model: str
    serialnumber: str
    installdate: str
    warrantyexpiration: str
    lastinspection: str
    nextinspection: str
    maintenancecost: float
    replacementcost: float
    criticality: str
    parentasset: Optional[str] = None
    childrenassets: List[str] = None
    
    def __post_init__(self):
        if self.childrenassets is None:
            self.childrenassets = []

@dataclass
class MockMaximoWorkOrder:
    """Mock Maximo Work Order data structure"""
    wonum: str
    description: str
    assetnum: str
    worktype: str
    priority: str
    status: str
    schedstart: str
    schedfinish: str
    actualstart: Optional[str] = None
    actualfinish: Optional[str] = None
    estcost: float = 0.0
    actualcost: float = 0.0
    laborhours: float = 0.0
    materialcost: float = 0.0
    assignedto: Optional[str] = None
    worklocation: Optional[str] = None
    parentwo: Optional[str] = None
    childwos: List[str] = None
    
    def __post_init__(self):
        if self.childwos is None:
            self.childwos = []

class MockMaximoServer:
    """
    Mock IBM Maximo Server for testing and demonstration
    
    This class simulates a real Maximo server with REST API endpoints
    for asset management, work orders, and inventory management.
    """
    
    def __init__(self, port: int = 9080):
        """Initialize the mock Maximo server"""
        self.port = port
        self.assets: Dict[str, MockMaximoAsset] = {}
        self.work_orders: Dict[str, MockMaximoWorkOrder] = {}
        self.inventory_items: Dict[str, Dict] = {}
        self.server_running = False
        self.request_log: List[Dict] = []
        
        # Initialize with some sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample KMRL data"""
        # Sample trainset assets
        sample_trainsets = [
            MockMaximoAsset(
                assetnum="KMRL-001",
                description="KMRL Trainset KMRL-001",
                assettype="TRAINSET",
                location="Aluva Depot",
                status="ACTIVE",
                manufacturer="Alstom",
                model="Metro Train",
                serialnumber="KMRL-001",
                installdate="2017-06-01",
                warrantyexpiration="2027-06-01",
                lastinspection="2024-09-01",
                nextinspection="2024-12-01",
                maintenancecost=15000.0,
                replacementcost=50000000.0,
                criticality="HIGH"
            ),
            MockMaximoAsset(
                assetnum="KMRL-002",
                description="KMRL Trainset KMRL-002",
                assettype="TRAINSET",
                location="Kakkanad Depot",
                status="MAINTENANCE",
                manufacturer="Alstom",
                model="Metro Train",
                serialnumber="KMRL-002",
                installdate="2017-08-15",
                warrantyexpiration="2027-08-15",
                lastinspection="2024-08-15",
                nextinspection="2024-11-15",
                maintenancecost=25000.0,
                replacementcost=50000000.0,
                criticality="MEDIUM"
            )
        ]
        
        for asset in sample_trainsets:
            self.assets[asset.assetnum] = asset
        
        # Sample work orders
        sample_work_orders = [
            MockMaximoWorkOrder(
                wonum="WO-KMRL-001-001",
                description="Routine maintenance for KMRL-001",
                assetnum="KMRL-001",
                worktype="PM",
                priority="2",
                status="WSCHD",
                schedstart="2024-09-20 08:00",
                schedfinish="2024-09-20 16:00",
                estcost=15000.0,
                worklocation="Aluva Depot",
                assignedto="MAINTENANCE_TEAM_A"
            ),
            MockMaximoWorkOrder(
                wonum="WO-KMRL-002-001",
                description="Corrective maintenance for KMRL-002",
                assetnum="KMRL-002",
                worktype="CM",
                priority="1",
                status="INPRG",
                schedstart="2024-09-19 09:00",
                schedfinish="2024-09-19 17:00",
                actualstart="2024-09-19 09:15",
                estcost=25000.0,
                worklocation="Kakkanad Depot",
                assignedto="MAINTENANCE_TEAM_B"
            )
        ]
        
        for wo in sample_work_orders:
            self.work_orders[wo.wonum] = wo
    
    def start_server(self):
        """Start the mock server (simulated)"""
        self.server_running = True
        print(f"🚀 Mock Maximo Server started on port {self.port}")
        print("✅ Server is ready to accept requests")
    
    def stop_server(self):
        """Stop the mock server"""
        self.server_running = False
        print("🛑 Mock Maximo Server stopped")
    
    def log_request(self, method: str, endpoint: str, data: Dict = None):
        """Log API requests"""
        self.request_log.append({
            'timestamp': datetime.now().isoformat(),
            'method': method,
            'endpoint': endpoint,
            'data': data
        })
    
    def create_asset(self, asset_data: Dict) -> Dict:
        """Create a new asset"""
        self.log_request("POST", "/oslc/os/mxapiasset", asset_data)
        
        try:
            asset = MockMaximoAsset(
                assetnum=asset_data.get('assetnum', ''),
                description=asset_data.get('description', ''),
                assettype=asset_data.get('assettype', 'TRAINSET'),
                location=asset_data.get('location', ''),
                status=asset_data.get('status', 'ACTIVE'),
                manufacturer=asset_data.get('manufacturer', 'Unknown'),
                model=asset_data.get('model', 'Unknown'),
                serialnumber=asset_data.get('serialnumber', ''),
                installdate=asset_data.get('installdate', datetime.now().strftime('%Y-%m-%d')),
                warrantyexpiration=asset_data.get('warrantyexpiration', ''),
                lastinspection=asset_data.get('lastinspection', datetime.now().strftime('%Y-%m-%d')),
                nextinspection=asset_data.get('nextinspection', ''),
                maintenancecost=asset_data.get('maintenancecost', 0.0),
                replacementcost=asset_data.get('replacementcost', 0.0),
                criticality=asset_data.get('criticality', 'MEDIUM')
            )
            
            self.assets[asset.assetnum] = asset
            
            return {
                'status': 'success',
                'assetnum': asset.assetnum,
                'message': f'Asset {asset.assetnum} created successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def update_asset(self, assetnum: str, update_data: Dict) -> Dict:
        """Update an existing asset"""
        self.log_request("PUT", f"/oslc/os/mxapiasset/{assetnum}", update_data)
        
        if assetnum not in self.assets:
            return {
                'status': 'error',
                'message': f'Asset {assetnum} not found'
            }
        
        try:
            asset = self.assets[assetnum]
            for key, value in update_data.items():
                if hasattr(asset, key):
                    setattr(asset, key, value)
            
            return {
                'status': 'success',
                'assetnum': assetnum,
                'message': f'Asset {assetnum} updated successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_work_order(self, wo_data: Dict) -> Dict:
        """Create a new work order"""
        self.log_request("POST", "/oslc/os/mxapiworkorder", wo_data)
        
        try:
            wo = MockMaximoWorkOrder(
                wonum=wo_data.get('wonum', ''),
                description=wo_data.get('description', ''),
                assetnum=wo_data.get('assetnum', ''),
                worktype=wo_data.get('worktype', 'PM'),
                priority=wo_data.get('priority', '2'),
                status=wo_data.get('status', 'WPLAN'),
                schedstart=wo_data.get('schedstart', ''),
                schedfinish=wo_data.get('schedfinish', ''),
                estcost=wo_data.get('estcost', 0.0),
                worklocation=wo_data.get('worklocation', ''),
                assignedto=wo_data.get('assignedto', '')
            )
            
            self.work_orders[wo.wonum] = wo
            
            return {
                'status': 'success',
                'wonum': wo.wonum,
                'message': f'Work order {wo.wonum} created successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_assets(self, filters: Dict = None) -> List[Dict]:
        """Get assets with optional filters"""
        self.log_request("GET", "/oslc/os/mxapiasset", filters)
        
        assets_list = []
        for asset in self.assets.values():
            asset_dict = asdict(asset)
            
            # Apply filters if provided
            if filters:
                match = True
                for key, value in filters.items():
                    if key in asset_dict and asset_dict[key] != value:
                        match = False
                        break
                if match:
                    assets_list.append(asset_dict)
            else:
                assets_list.append(asset_dict)
        
        return assets_list
    
    def get_work_orders(self, filters: Dict = None) -> List[Dict]:
        """Get work orders with optional filters"""
        self.log_request("GET", "/oslc/os/mxapiworkorder", filters)
        
        work_orders_list = []
        for wo in self.work_orders.values():
            wo_dict = asdict(wo)
            
            # Apply filters if provided
            if filters:
                match = True
                for key, value in filters.items():
                    if key in wo_dict and wo_dict[key] != value:
                        match = False
                        break
                if match:
                    work_orders_list.append(wo_dict)
            else:
                work_orders_list.append(wo_dict)
        
        return work_orders_list
    
    def get_asset_maintenance_history(self, assetnum: str) -> List[Dict]:
        """Get maintenance history for an asset"""
        self.log_request("GET", f"/oslc/os/mxapiworkorder?assetnum={assetnum}")
        
        history = []
        for wo in self.work_orders.values():
            if wo.assetnum == assetnum and wo.status == "COMP":
                history.append(asdict(wo))
        
        return history
    
    def get_preventive_maintenance_schedule(self, days_ahead: int = 30) -> List[Dict]:
        """Get preventive maintenance schedule"""
        self.log_request("GET", f"/oslc/os/mxapiworkorder?worktype=PM&status=WSCHD")
        
        schedule = []
        end_date = datetime.now() + timedelta(days=days_ahead)
        
        for wo in self.work_orders.values():
            if wo.worktype == "PM" and wo.status == "WSCHD":
                try:
                    sched_date = datetime.strptime(wo.schedstart, '%Y-%m-%d %H:%M')
                    if sched_date <= end_date:
                        schedule.append(asdict(wo))
                except:
                    schedule.append(asdict(wo))
        
        return schedule
    
    def get_maintenance_cost_analytics(self, assetnum: str = None) -> Dict:
        """Get maintenance cost analytics"""
        self.log_request("GET", f"/oslc/os/mxapiworkorder?status=COMP")
        
        completed_wos = [wo for wo in self.work_orders.values() if wo.status == "COMP"]
        
        if assetnum:
            completed_wos = [wo for wo in completed_wos if wo.assetnum == assetnum]
        
        total_cost = sum(wo.actualcost for wo in completed_wos)
        avg_cost = total_cost / len(completed_wos) if completed_wos else 0
        
        return {
            'total_cost': total_cost,
            'average_cost': avg_cost,
            'work_order_count': len(completed_wos),
            'cost_trend': [wo.actualcost for wo in completed_wos[-12:]],  # Last 12 months
            'top_cost_drivers': self._get_top_cost_drivers(completed_wos)
        }
    
    def _get_top_cost_drivers(self, work_orders: List[MockMaximoWorkOrder]) -> List[Dict]:
        """Get top cost drivers"""
        cost_by_type = {}
        for wo in work_orders:
            wo_type = wo.worktype
            cost_by_type[wo_type] = cost_by_type.get(wo_type, 0) + wo.actualcost
        
        return sorted(cost_by_type.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def get_server_status(self) -> Dict:
        """Get server status"""
        return {
            'server_running': self.server_running,
            'port': self.port,
            'total_assets': len(self.assets),
            'total_work_orders': len(self.work_orders),
            'total_requests': len(self.request_log),
            'uptime': 'Mock server - always running'
        }
    
    def get_request_log(self) -> List[Dict]:
        """Get request log"""
        return self.request_log

# Global mock server instance
mock_server = MockMaximoServer()

def start_mock_maximo_server():
    """Start the mock Maximo server"""
    mock_server.start_server()
    return mock_server

def get_mock_server():
    """Get the mock server instance"""
    return mock_server

# Example usage
if __name__ == "__main__":
    # Start the mock server
    server = start_mock_maximo_server()
    
    # Test creating an asset
    asset_data = {
        'assetnum': 'KMRL-TEST-001',
        'description': 'Test Trainset',
        'assettype': 'TRAINSET',
        'location': 'Test Depot',
        'status': 'ACTIVE',
        'manufacturer': 'Alstom',
        'model': 'Metro Train',
        'serialnumber': 'TEST-001',
        'installdate': '2024-01-01',
        'warrantyexpiration': '2029-01-01',
        'lastinspection': '2024-09-01',
        'nextinspection': '2024-12-01',
        'maintenancecost': 10000.0,
        'replacementcost': 50000000.0,
        'criticality': 'MEDIUM'
    }
    
    result = server.create_asset(asset_data)
    print(f"Asset creation result: {result}")
    
    # Test getting assets
    assets = server.get_assets()
    print(f"Total assets: {len(assets)}")
    
    # Test getting work orders
    work_orders = server.get_work_orders()
    print(f"Total work orders: {len(work_orders)}")
    
    # Test analytics
    analytics = server.get_maintenance_cost_analytics()
    print(f"Cost analytics: {analytics}")
    
    print("✅ Mock Maximo Server test completed successfully!")
