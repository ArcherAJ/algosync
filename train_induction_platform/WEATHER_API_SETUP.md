# Weather API Setup Guide for KMRL AI Platform

## 🌤️ Free Weather API Integration

### Step 1: Get Your Free API Key

1. **Visit OpenWeatherMap**: Go to https://home.openweathermap.org/users/sign_up
2. **Sign Up**: Create a free account (no credit card required)
3. **Get API Key**: 
   - After registration, go to "API keys" section
   - Copy your API key (it looks like: `abc123def456ghi789jkl012mno345pqr678`)

### Step 2: Free Tier Limits
- **60 calls per minute**
- **1,000,000 calls per month**
- **Current weather data**
- **5-day weather forecast**
- **Historical weather data**

### Step 3: Configure in Your Application

#### Option A: Set API Key in Streamlit App
1. Run your application: `streamlit run main.py`
2. Go to "🌤️ Advanced Analytics" tab
3. Click on "🌤️ Weather Monitoring" sub-tab
4. Expand "⚙️ Weather API Configuration"
5. Enter your API key and click "Save API Key"

#### Option B: Set API Key Programmatically
```python
# In your Python code
from system_manager import SystemIntegrationManager
system_manager = SystemIntegrationManager()
system_manager.weather_integrator.set_api_key("YOUR_API_KEY_HERE")
```

### Step 4: Test the Integration
1. After setting the API key, refresh the weather data
2. You should see real weather data instead of mock data
3. Check the "Weather Impact Analysis" section for live data

## 🔧 Alternative Free APIs

### Open-Meteo (No API Key Required)
- **URL**: https://open-meteo.com/
- **Features**: High-resolution forecasts, no registration needed
- **Limits**: 10,000 requests per day

### WeatherAPI.com
- **URL**: https://www.weatherapi.com/signup.aspx
- **Features**: Real-time weather, 3-day forecasts
- **Free Tier**: 1 million calls per month

## 📊 Weather Data Used in Optimization

Your system uses weather data for:
- **Passenger Demand Prediction** - Weather affects ridership
- **Energy Consumption Optimization** - Temperature impacts HVAC usage
- **Maintenance Scheduling** - Weather conditions affect maintenance needs
- **Operational Recommendations** - Weather-based operational adjustments

## 🚀 Benefits of Real Weather Data

1. **Accurate Demand Forecasting** - Weather significantly impacts metro ridership
2. **Energy Optimization** - Temperature data helps optimize HVAC systems
3. **Safety Recommendations** - Weather alerts for operational safety
4. **Cost Savings** - Better resource allocation based on weather conditions

## 🔍 Troubleshooting

### Common Issues:
1. **API Key Not Working**: Ensure you've activated your API key (may take 10 minutes)
2. **Rate Limiting**: Free tier has 60 calls/minute limit
3. **Location Issues**: Default location is Kochi, India - adjust if needed

### Support:
- OpenWeatherMap Support: https://openweathermap.org/help
- Documentation: https://openweathermap.org/api
