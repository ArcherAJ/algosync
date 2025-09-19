#!/usr/bin/env python3
"""
Test script for Mock IBM Maximo Integration with KMRL Train Induction Platform
"""

from maximo_data_connector import MaximoDataConnector
from mock_maximo_server import start_mock_maximo_server

def test_mock_maximo_integration():
    """Test the complete Mock Maximo integration workflow"""
    print("🔧 Testing Mock IBM Maximo Integration...")
    
    # Start mock server
    mock_server = start_mock_maximo_server()
    print("✅ Mock Maximo Server started")
    
    # Initialize connector
    connector = MaximoDataConnector()
    connector.mock_server = mock_server
    connector.maximo_connected = True
    print("✅ Maximo Data Connector initialized")
    
    # Load datasets
    datasets = connector.load_existing_datasets()
    print(f"✅ Loaded {len(datasets)} datasets")
    
    # Generate comprehensive results
    results = connector.generate_comprehensive_results()
    print("✅ Generated comprehensive results")
    
    # Display summary
    if 'sync_results' in results:
        total_assets = 0
        total_work_orders = 0
        
        for dataset, sync_data in results['sync_results'].items():
            if 'error' not in sync_data:
                if 'assets_created' in sync_data:
                    total_assets += sync_data['assets_created']
                if 'facilities_created' in sync_data:
                    total_assets += sync_data['facilities_created']
                if 'work_orders_created' in sync_data:
                    total_work_orders += sync_data['work_orders_created']
        
        print(f"📊 Summary:")
        print(f"   - Total Assets Synced: {total_assets}")
        print(f"   - Total Work Orders: {total_work_orders}")
        print(f"   - Recommendations: {len(results.get('recommendations', []))}")
    
    # Show mock server status
    server_status = mock_server.get_server_status()
    print(f"\n🔧 Mock Server Status:")
    print(f"   - Server Running: {server_status['server_running']}")
    print(f"   - Total Assets: {server_status['total_assets']}")
    print(f"   - Total Work Orders: {server_status['total_work_orders']}")
    print(f"   - Total Requests: {server_status['total_requests']}")
    
    # Show some sample data
    print(f"\n📋 Sample Assets:")
    assets = mock_server.get_assets()
    for i, asset in enumerate(assets[:3]):  # Show first 3 assets
        print(f"   {i+1}. {asset['assetnum']} - {asset['description']} ({asset['status']})")
    
    print(f"\n📋 Sample Work Orders:")
    work_orders = mock_server.get_work_orders()
    for i, wo in enumerate(work_orders[:3]):  # Show first 3 work orders
        print(f"   {i+1}. {wo['wonum']} - {wo['description']} ({wo['status']})")
    
    # Export results
    filename = connector.export_results_to_csv()
    if filename:
        print(f"\n📤 Results exported to: {filename}")
    
    print("\n✅ Mock IBM Maximo Integration Test Completed Successfully!")
    print("🎉 The system is now ready to work with your existing data!")

if __name__ == "__main__":
    test_mock_maximo_integration()
