#!/usr/bin/env python3
"""
Test script for ML models in branding.py
This script demonstrates how to use the ML models independently
"""

from common_imports import *

# Add the frontend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))

from branding import AdvertisementMLPredictor

def test_ml_models():
    """Test the ML models functionality"""
    print("🤖 Testing ML Models for Advertisement Performance Prediction")
    print("=" * 60)
    
    # Initialize the predictor
    predictor = AdvertisementMLPredictor()
    
    # Load data
    print("📊 Loading advertisement data...")
    if not predictor.load_data():
        print("❌ Failed to load data")
        return False
    
    print(f"✅ Loaded {len(predictor.data)} campaigns")
    
    # Train models
    print("🧠 Training ML models...")
    if not predictor.train_models():
        print("❌ Failed to train models")
        return False
    
    print("✅ Models trained successfully!")
    
    # Get model performance
    performance = predictor.get_model_performance()
    print("\n📈 Model Performance:")
    print(f"Revenue Prediction - R²: {performance['revenue']['r2']:.3f}, RMSE: {performance['revenue']['rmse']:.0f}")
    print(f"Engagement Prediction - R²: {performance['engagement']['r2']:.3f}, RMSE: {performance['engagement']['rmse']:.4f}")
    print(f"ROI Prediction - R²: {performance['roi']['r2']:.3f}, RMSE: {performance['roi']['rmse']:.3f}")
    
    # Test predictions
    print("\n🔮 Testing Predictions:")
    
    # Sample campaign data
    test_campaigns = [
        {
            'advertiser': 'Apple',
            'category': 'Telecom',
            'subcategory': 'Mobile',
            'duration_days': 30,
            'investment': 100000,
            'impressions': 50000,
            'engagement_rate': 0.05,
            'target_demographic': 'Professionals',
            'compartment_type': 'Standard'
        },
        {
            'advertiser': 'Google',
            'category': 'FMCG',
            'subcategory': 'Snacks',
            'duration_days': 60,
            'investment': 200000,
            'impressions': 100000,
            'engagement_rate': 0.07,
            'target_demographic': 'Students',
            'compartment_type': 'Premium'
        }
    ]
    
    for i, campaign in enumerate(test_campaigns, 1):
        print(f"\nCampaign {i}: {campaign['advertiser']} - {campaign['category']}")
        
        predicted_revenue = predictor.predict_revenue(campaign)
        predicted_engagement = predictor.predict_engagement(campaign)
        predicted_roi = predictor.predict_roi(campaign)
        
        print(f"  Predicted Revenue: ₹{predicted_revenue:,.0f}")
        print(f"  Predicted Engagement: {predicted_engagement:.3f}")
        print(f"  Predicted ROI: {predicted_roi:.3f}")
        
        # ROI recommendation
        if predicted_roi > 0.5:
            recommendation = "🎯 Excellent ROI - Highly recommended!"
        elif predicted_roi > 0.2:
            recommendation = "👍 Good ROI - Consider this campaign"
        elif predicted_roi > 0:
            recommendation = "⚠️ Low ROI - Review parameters"
        else:
            recommendation = "❌ Negative ROI - Not recommended"
        
        print(f"  Recommendation: {recommendation}")
    
    print("\n✅ ML Models test completed successfully!")
    return True

if __name__ == "__main__":
    test_ml_models()
