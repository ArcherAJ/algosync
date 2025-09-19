#!/usr/bin/env python3
"""
Test script for IBM Maximo Integration with KMRL Train Induction Platform
"""

from maximo_data_connector import MaximoDataConnector

def test_maximo_integration():
    """Test the complete Maximo integration workflow"""
    print("🔧 Testing IBM Maximo Integration...")
    
    # Initialize connector
    connector = MaximoDataConnector()
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
    
    # Export results
    filename = connector.export_results_to_csv()
    if filename:
        print(f"📤 Results exported to: {filename}")
    
    # Generate report
    report = connector.get_summary_report()
    print("\n📋 Summary Report:")
    print("=" * 50)
    print(report)
    
    print("\n✅ IBM Maximo Integration Test Completed Successfully!")

if __name__ == "__main__":
    test_maximo_integration()
