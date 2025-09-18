from common_imports import *

class WeatherDataIntegrator:
    """
    Weather data integration for metro operations
    Integrates real-time weather data with passenger demand and operations
    """
    
    def __init__(self):
        self.weather_api_key = None
        self.weather_data = {}
        self.weather_cache = {}
        self.cache_duration = 1800  # 30 minutes
        self.weather_impact_model = None
        self.is_trained = False
        self.api_requests_count = 0
        self.last_request_time = None
        self.rate_limit = 60  # requests per minute for free tier
        
    def set_api_key(self, api_key):
        """Set OpenWeatherMap API key"""
        self.weather_api_key = api_key
        self.api_requests_count = 0
        self.last_request_time = None
        print(f"Weather API key set successfully. Free tier allows {self.rate_limit} requests per minute.")
        
    def _check_rate_limit(self):
        """Check if we're within rate limits"""
        current_time = datetime.now()
        
        if self.last_request_time is None:
            self.last_request_time = current_time
            return True
        
        # Reset counter if more than a minute has passed
        if (current_time - self.last_request_time).seconds >= 60:
            self.api_requests_count = 0
            self.last_request_time = current_time
        
        return self.api_requests_count < self.rate_limit
        
    def get_weather_data(self, city="Kochi"):
        """Get current weather data"""
        if not self.weather_api_key:
            return self._get_mock_weather_data()
        
        # Check rate limit
        if not self._check_rate_limit():
            print("Rate limit exceeded, using cached data")
            return self._get_cached_weather_data(city)
        
        try:
            # Check cache first
            cache_key = f"{city}_{datetime.now().strftime('%Y%m%d%H')}"
            if cache_key in self.weather_cache:
                cached_time = self.weather_cache[cache_key]['timestamp']
                if (datetime.now() - cached_time).seconds < self.cache_duration:
                    return self.weather_cache[cache_key]['data']
            
            # Fetch from API
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            # Increment request counter
            self.api_requests_count += 1
            
            if response.status_code == 200:
                data = response.json()
                weather_info = {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'wind_speed': data['wind']['speed'],
                    'weather_condition': data['weather'][0]['main'],
                    'weather_description': data['weather'][0]['description'],
                    'visibility': data.get('visibility', 10000),
                    'timestamp': datetime.now(),
                    'data_source': 'OpenWeatherMap API'
                }
                
                # Cache the data
                self.weather_cache[cache_key] = {
                    'data': weather_info,
                    'timestamp': datetime.now()
                }
                
                print(f"Weather data fetched successfully for {city}")
                return weather_info
            else:
                print(f"Weather API error: {response.status_code} - {response.text}")
                return self._get_mock_weather_data()
                
        except Exception as e:
            print(f"Weather API error: {e}")
            return self._get_mock_weather_data()
    
    def _get_cached_weather_data(self, city):
        """Get cached weather data when rate limit is exceeded"""
        cache_key = f"{city}_{datetime.now().strftime('%Y%m%d%H')}"
        if cache_key in self.weather_cache:
            cached_data = self.weather_cache[cache_key]['data'].copy()
            cached_data['data_source'] = 'Cached (Rate Limited)'
            return cached_data
        return self._get_mock_weather_data()
    
    def _get_mock_weather_data(self):
        """Generate mock weather data for testing"""
        conditions = ['Clear', 'Clouds', 'Rain', 'Thunderstorm', 'Fog', 'Mist']
        condition = random.choice(conditions)
        
        # Generate realistic weather based on condition
        if condition == 'Rain':
            temp = random.uniform(22, 28)
            humidity = random.uniform(80, 95)
        elif condition == 'Clear':
            temp = random.uniform(28, 35)
            humidity = random.uniform(60, 80)
        else:
            temp = random.uniform(24, 30)
            humidity = random.uniform(70, 85)
        
        return {
            'temperature': round(temp, 1),
            'humidity': round(humidity, 1),
            'pressure': random.uniform(1000, 1020),
            'wind_speed': random.uniform(5, 25),
            'weather_condition': condition,
            'weather_description': f"{condition.lower()} conditions",
            'visibility': random.uniform(5000, 15000),
            'timestamp': datetime.now(),
            'data_source': 'Mock Data (No API Key)'
        }
    
    def get_weather_forecast(self, city="Kochi", days=5):
        """Get weather forecast for multiple days"""
        if not self.weather_api_key:
            return self._get_mock_forecast(days)
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                forecast = []
                
                for item in data['list'][:days * 8]:  # 8 forecasts per day
                    forecast.append({
                        'datetime': datetime.fromtimestamp(item['dt']),
                        'temperature': item['main']['temp'],
                        'humidity': item['main']['humidity'],
                        'weather_condition': item['weather'][0]['main'],
                        'weather_description': item['weather'][0]['description']
                    })
                
                return forecast
            else:
                return self._get_mock_forecast(days)
                
        except Exception as e:
            print(f"Weather forecast API error: {e}")
            return self._get_mock_forecast(days)
    
    def _get_mock_forecast(self, days):
        """Generate mock weather forecast"""
        forecast = []
        current_time = datetime.now()
        
        for i in range(days * 8):
            forecast_time = current_time + timedelta(hours=i * 3)
            conditions = ['Clear', 'Clouds', 'Rain', 'Thunderstorm']
            condition = random.choice(conditions)
            
            if condition == 'Rain':
                temp = random.uniform(22, 28)
            elif condition == 'Clear':
                temp = random.uniform(28, 35)
            else:
                temp = random.uniform(24, 30)
            
            forecast.append({
                'datetime': forecast_time,
                'temperature': round(temp, 1),
                'humidity': random.uniform(60, 95),
                'weather_condition': condition,
                'weather_description': f"{condition.lower()} conditions"
            })
        
        return forecast
    
    def calculate_weather_impact(self, weather_data, passenger_demand):
        """Calculate how weather affects passenger demand"""
        if not self.is_trained:
            return self._calculate_basic_weather_impact(weather_data, passenger_demand)
        
        try:
            # Prepare features for ML model
            features = [
                weather_data['temperature'],
                weather_data['humidity'],
                weather_data['pressure'],
                weather_data['wind_speed'],
                weather_data['visibility'] / 1000,  # Convert to km
                1 if weather_data['weather_condition'] in ['Rain', 'Thunderstorm'] else 0,
                1 if weather_data['weather_condition'] == 'Clear' else 0
            ]
            
            # Use trained model to predict impact
            impact_factor = self.weather_impact_model.predict([features])[0]
            return max(0.5, min(1.5, impact_factor))  # Clamp between 0.5 and 1.5
            
        except Exception as e:
            print(f"Weather impact calculation error: {e}")
            return self._calculate_basic_weather_impact(weather_data, passenger_demand)
    
    def _calculate_basic_weather_impact(self, weather_data, passenger_demand):
        """Basic weather impact calculation"""
        impact_factor = 1.0
        
        # Temperature impact
        temp = weather_data['temperature']
        if temp < 20 or temp > 35:
            impact_factor *= 0.9  # Extreme temperatures reduce ridership
        
        # Rain impact
        if weather_data['weather_condition'] in ['Rain', 'Thunderstorm']:
            impact_factor *= 0.85  # Rain reduces ridership
        
        # Clear weather impact
        if weather_data['weather_condition'] == 'Clear':
            impact_factor *= 1.05  # Clear weather increases ridership
        
        # Humidity impact
        if weather_data['humidity'] > 90:
            impact_factor *= 0.95  # High humidity reduces comfort
        
        return max(0.5, min(1.5, impact_factor))
    
    def train_weather_impact_model(self, historical_data):
        """Train ML model to predict weather impact on ridership"""
        try:
            if len(historical_data) < 50:
                return False
            
            # Prepare training data
            features = []
            targets = []
            
            for record in historical_data:
                weather_features = [
                    record['temperature'],
                    record['humidity'],
                    record['pressure'],
                    record['wind_speed'],
                    record['visibility'] / 1000,
                    1 if record['weather_condition'] in ['Rain', 'Thunderstorm'] else 0,
                    1 if record['weather_condition'] == 'Clear' else 0
                ]
                features.append(weather_features)
                targets.append(record['demand_impact'])
            
            # Train model
            X = np.array(features)
            y = np.array(targets)
            
            self.weather_impact_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.weather_impact_model.fit(X, y)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Weather impact model training error: {e}")
            return False
    
    def get_weather_recommendations(self, weather_data):
        """Get operational recommendations based on weather"""
        recommendations = []
        
        if weather_data['weather_condition'] in ['Rain', 'Thunderstorm']:
            recommendations.append("🌧️ Rain expected - Increase platform staff for passenger assistance")
            recommendations.append("🚇 Consider reducing train frequency during heavy rain")
            recommendations.append("🧹 Ensure proper drainage and cleaning systems are active")
        
        if weather_data['temperature'] > 35:
            recommendations.append("🌡️ High temperature - Ensure HVAC systems are functioning optimally")
            recommendations.append("💧 Increase water availability at stations")
            recommendations.append("⏰ Consider adjusting peak hours due to heat")
        
        if weather_data['humidity'] > 90:
            recommendations.append("💨 High humidity - Monitor air quality and ventilation")
            recommendations.append("🧽 Increase cleaning frequency for passenger comfort")
        
        if weather_data['wind_speed'] > 20:
            recommendations.append("💨 Strong winds - Secure outdoor equipment and signage")
            recommendations.append("⚠️ Monitor for debris on tracks")
        
        if weather_data['visibility'] < 1000:
            recommendations.append("🌫️ Low visibility - Increase safety measures")
            recommendations.append("📢 Enhance passenger announcements")
        
        return recommendations
    
    def get_weather_insights(self):
        """Get comprehensive weather insights"""
        current_weather = self.get_weather_data()
        forecast = self.get_weather_forecast(days=3)
        
        insights = {
            'current_weather': current_weather,
            'forecast': forecast,
            'recommendations': self.get_weather_recommendations(current_weather),
            'impact_factor': self.calculate_weather_impact(current_weather, 1000),
            'model_trained': self.is_trained
        }
        
        return insights
