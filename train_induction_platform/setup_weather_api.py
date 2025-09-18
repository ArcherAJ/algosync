#!/usr/bin/env python3
"""
Weather API Setup Helper for KMRL AI Platform
This script helps you test your weather API key and configure the system
"""

import requests
import json
from datetime import datetime

def test_weather_api(api_key, city="Kochi"):
    """Test if the weather API key is working"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Key is working!")
            print(f"📍 Location: {data['name']}, {data['sys']['country']}")
            print(f"🌡️ Temperature: {data['main']['temp']}°C")
            print(f"☁️ Weather: {data['weather'][0]['description']}")
            print(f"💨 Wind: {data['wind']['speed']} m/s")
            print(f"💧 Humidity: {data['main']['humidity']}%")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def main():
    print("🌤️ Weather API Setup Helper for KMRL AI Platform")
    print("=" * 50)
    
    print("\n📋 Steps to get your free API key:")
    print("1. Visit: https://home.openweathermap.org/users/sign_up")
    print("2. Sign up for a free account")
    print("3. Go to 'API keys' section")
    print("4. Copy your API key")
    
    print("\n🔑 Enter your API key to test:")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return
    
    if len(api_key) < 20:
        print("❌ API key seems too short. Please check your key.")
        return
    
    print(f"\n🧪 Testing API key...")
    if test_weather_api(api_key):
        print("\n🎉 Great! Your API key is working.")
        print("\n📝 Next steps:")
        print("1. Run your KMRL AI Platform: streamlit run main.py")
        print("2. Go to '🌤️ Advanced Analytics' tab")
        print("3. Click '🌤️ Weather Monitoring' sub-tab")
        print("4. Expand '⚙️ Weather API Configuration'")
        print("5. Paste your API key and click 'Save API Key'")
        print("\n✨ You'll now get real weather data in your optimization!")
    else:
        print("\n🔧 Troubleshooting:")
        print("- Make sure your API key is correct")
        print("- Check if your API key is activated (may take 10 minutes)")
        print("- Verify you're using the correct API key from OpenWeatherMap")
        print("- Try again in a few minutes if you just created the account")

if __name__ == "__main__":
    main()
