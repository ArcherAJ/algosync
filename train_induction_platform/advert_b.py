import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime, timedelta

class MetroAdvertisementPlanner:
    def __init__(self):
        self.ads_data = pd.DataFrame()
        self.metro_capacity = 8  # number of compartments per train
        self.women_compartments = 2  # number of women-only compartments
        self.base_metro_frequency = 10  # base number of metros per hour
        self.max_metro_frequency = 20  # maximum number of metros per hour
        self.peak_hours = [(7, 10), (17, 20)]  # morning and evening peak hours
        
    def load_ads_data(self, ads_data: pd.DataFrame):
        """Load advertisement data from DataFrame and normalize column names"""
        # Normalize column names to match expected format
        normalized_data = ads_data.copy()
        
        # Map CSV columns to expected columns
        column_mapping = {
            'campaign_id': 'company_id',
            'advertiser': 'company_name',
            'investment': 'rate_per_day',
            'compartment_type': 'placement_type'
        }
        
        # Rename columns if they exist
        for csv_col, expected_col in column_mapping.items():
            if csv_col in normalized_data.columns:
                normalized_data = normalized_data.rename(columns={csv_col: expected_col})
        
        # Calculate rate_per_day from investment and duration if not already present
        if 'rate_per_day' not in normalized_data.columns and 'investment' in ads_data.columns and 'duration_days' in ads_data.columns:
            normalized_data['rate_per_day'] = ads_data['investment'] / ads_data['duration_days']
        
        # Add women_specific column based on compartment_type
        if 'placement_type' in normalized_data.columns:
            normalized_data['women_specific'] = normalized_data['placement_type'] == 'Women'
        elif 'women_specific' not in normalized_data.columns:
            # Default to False if not specified
            normalized_data['women_specific'] = False
        
        self.ads_data = normalized_data
        return True
        
    def calculate_revenue_potential(self, company_id: str, duration_days: int, 
                                   placement: str = "standard") -> float:
        """Calculate revenue potential for a specific company"""
        company_data = self.ads_data[self.ads_data['company_id'] == company_id]
        if company_data.empty:
            return 0.0
        
        # Use actual revenue_generated from CSV if available
        if 'revenue_generated' in company_data.columns:
            base_revenue = company_data['revenue_generated'].values[0]
            # Scale based on duration ratio
            original_duration = company_data['duration_days'].values[0] if 'duration_days' in company_data.columns else 1
            duration_ratio = duration_days / original_duration if original_duration > 0 else 1
            scaled_revenue = base_revenue * duration_ratio
        else:
            # Fallback to rate-based calculation
            base_rate = company_data['rate_per_day'].values[0]
            category = company_data['category'].values[0]
            
            # Apply category multiplier
            category_multiplier = self._get_category_multiplier(category)
            
            # Apply placement multiplier
            placement_multiplier = self._get_placement_multiplier(placement)
            
            # Calculate total revenue
            scaled_revenue = base_rate * duration_days * category_multiplier * placement_multiplier
        
        # Apply placement multiplier for final calculation
        placement_multiplier = self._get_placement_multiplier(placement)
        total_revenue = scaled_revenue * placement_multiplier
        
        return total_revenue
        
    def _get_category_multiplier(self, category: str) -> float:
        """Get multiplier based on advertisement category"""
        multipliers = {
            'premium': 1.5,
            'standard': 1.0,
            'budget': 0.8
        }
        return multipliers.get(category, 1.0)
    
    def _get_placement_multiplier(self, placement: str) -> float:
        """Get multiplier based on ad placement"""
        multipliers = {
            'premium_spot': 1.8,  # Eye-level, high visibility areas
            'standard': 1.0,      # Regular placement
            'women_compartment': 1.2  # Women's compartment specific
        }
        return multipliers.get(placement, 1.0)
        
    def determine_metro_frequency(self, total_revenue: float, hour_of_day: int = None) -> int:
        """Determine metro frequency based on total revenue and time of day"""
        # Scale frequency based on revenue (simplified model)
        additional_metros = min(int(total_revenue / 10000), self.max_metro_frequency - self.base_metro_frequency)
        base_frequency = self.base_metro_frequency + additional_metros
        
        # Adjust for peak hours if specific hour is provided
        if hour_of_day is not None:
            for start, end in self.peak_hours:
                if start <= hour_of_day < end:
                    base_frequency = min(base_frequency * 1.5, self.max_metro_frequency)
                    break
        
        return int(base_frequency)
        
    def filter_feminine_ads(self, ads_data: pd.DataFrame = None) -> pd.DataFrame:
        """Filter advertisements suitable for women's compartments"""
        if ads_data is None:
            ads_data = self.ads_data
        
        # Get ads for women's compartments based on compartment_type
        women_compartment_ads = ads_data[ads_data['compartment_type'] == 'Women'] if 'compartment_type' in ads_data.columns else pd.DataFrame()
        
        # Also filter by feminine subcategories
        feminine_categories = ['fashion', 'beauty', 'health', 'childcare', 'jewelry', 
                              'cosmetics', 'wellness', 'maternity', 'Personal Care', 'Beverages']
        feminine_subcategory_ads = ads_data[ads_data['subcategory'].isin(feminine_categories)] if 'subcategory' in ads_data.columns else pd.DataFrame()
        
        # Include ads specifically marked as suitable for women
        women_specific_ads = ads_data[ads_data['women_specific'] == True] if 'women_specific' in ads_data.columns else pd.DataFrame()
        
        # Target demographic-based filtering
        women_demographic_ads = ads_data[ads_data['target_demographic'] == 'Women'] if 'target_demographic' in ads_data.columns else pd.DataFrame()
        
        # Combine all feminine ads and remove duplicates
        all_feminine_ads_list = []
        if not women_compartment_ads.empty:
            all_feminine_ads_list.append(women_compartment_ads)
        if not feminine_subcategory_ads.empty:
            all_feminine_ads_list.append(feminine_subcategory_ads)
        if not women_specific_ads.empty:
            all_feminine_ads_list.append(women_specific_ads)
        if not women_demographic_ads.empty:
            all_feminine_ads_list.append(women_demographic_ads)
        
        if all_feminine_ads_list:
            all_feminine_ads = pd.concat(all_feminine_ads_list).drop_duplicates()
        else:
            all_feminine_ads = pd.DataFrame()
        
        return all_feminine_ads
        
    def get_optimal_ads_allocation(self, duration_days: int) -> Dict:
        """Calculate optimal advertisement allocation and metro frequency"""
        if self.ads_data.empty:
            return {}
            
        # Calculate revenue for each company
        revenues = {}
        for _, row in self.ads_data.iterrows():
            revenue = self.calculate_revenue_potential(row['company_id'], duration_days)
            revenues[row['company_id']] = revenue
            
        # Sort companies by revenue
        sorted_companies = sorted(revenues.items(), key=lambda x: x[1], reverse=True)
        
        # Calculate total revenue
        total_revenue = sum(revenues.values())
        
        # Determine metro frequency for different times of day
        metro_frequencies = {}
        for hour in range(24):
            metro_frequencies[hour] = self.determine_metro_frequency(total_revenue, hour)
        
        # Get feminine ads for women's compartments
        feminine_ads = self.filter_feminine_ads()
        
        # Calculate revenue from women's compartment ads specifically
        women_comp_revenue = 0
        for _, ad in feminine_ads.iterrows():
            women_comp_revenue += self.calculate_revenue_potential(
                ad['company_id'], duration_days, "women_compartment"
            )
        
        # Generate smart recommendations
        recommendations = self._generate_recommendations(total_revenue, women_comp_revenue, feminine_ads)
        
        return {
            'total_revenue': total_revenue,
            'women_comp_revenue': women_comp_revenue,
            'metro_frequencies': metro_frequencies,
            'company_revenues': dict(sorted_companies),
            'feminine_ads': feminine_ads.to_dict('records'),
            'recommendations': recommendations
        }
    
    def _generate_recommendations(self, total_revenue: float, women_comp_revenue: float, 
                                feminine_ads: pd.DataFrame) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # General recommendations
        if total_revenue > 500000:
            recommendations.append("High revenue potential detected. Consider increasing metro frequency during peak hours.")
        elif total_revenue > 200000:
            recommendations.append("Moderate revenue potential. Focus on premium advertisers to increase revenue.")
        else:
            recommendations.append("Low revenue potential. Consider reaching out to more premium brands.")
        
        # Women's compartment recommendations
        women_comp_ratio = women_comp_revenue / total_revenue if total_revenue > 0 else 0
        if women_comp_ratio < 0.2:
            recommendations.append("Low women's compartment advertising revenue. Consider targeting more feminine-focused brands.")
        elif women_comp_ratio > 0.4:
            recommendations.append("Strong women's compartment advertising revenue. Consider expanding women's compartment allocation.")
        else:
            recommendations.append("Adequate women's compartment revenue. Maintain current strategy.")
        
        # Specific brand recommendations
        if len(feminine_ads) > 0:
            # Use revenue_generated if available, otherwise use rate_per_day
            if 'revenue_generated' in feminine_ads.columns:
                top_feminine_brand = feminine_ads.sort_values('revenue_generated', ascending=False).iloc[0]
                recommendations.append(f"Consider prioritizing {top_feminine_brand['advertiser']} for women's compartments (high revenue: ₹{top_feminine_brand['revenue_generated']:,.2f}).")
            elif 'rate_per_day' in feminine_ads.columns:
                top_feminine_brand = feminine_ads.sort_values('rate_per_day', ascending=False).iloc[0]
                recommendations.append(f"Consider prioritizing {top_feminine_brand['company_name']} for women's compartments (high rate: ₹{top_feminine_brand['rate_per_day']}/day).")
            else:
                # Fallback to first brand
                top_feminine_brand = feminine_ads.iloc[0]
                company_name = top_feminine_brand.get('company_name', top_feminine_brand.get('advertiser', 'Unknown'))
                recommendations.append(f"Consider prioritizing {company_name} for women's compartments.")
        
        # Peak hour recommendations
        recommendations.append(f"Peak hours configured: {self.peak_hours[0][0]}-{self.peak_hours[0][1]} and {self.peak_hours[1][0]}-{self.peak_hours[1][1]}. Metro frequency will be increased during these times.")
        
        return recommendations

# Mock data generation function
def initialize_sample_data():
    """Initialize sample advertisement data with both regular and feminine-focused brands"""
    data = {
        'company_id': ['comp_001', 'comp_002', 'comp_003', 'comp_004', 'comp_005', 
                      'comp_006', 'comp_007', 'comp_008', 'comp_009', 'comp_010',
                      'comp_011', 'comp_012', 'comp_013', 'comp_014', 'comp_015'],
        'company_name': ['Coca Cola', 'Pepsi', 'Samsung', 'Apple', 'Toyota', 
                        'Flipkart', 'BSNL', 'Airtel', 'L\'Oreal', 'Vanity Fair',
                        'Titan Raga', 'Forest Essentials', 'FirstCry', 'Lakme', 'Mamaearth'],
        'category': ['premium', 'standard', 'premium', 'premium', 'standard', 
                    'standard', 'budget', 'standard', 'premium', 'premium',
                    'premium', 'premium', 'standard', 'standard', 'standard'],
        'subcategory': ['beverages', 'beverages', 'electronics', 'electronics', 'automotive', 
                       'ecommerce', 'telecom', 'telecom', 'cosmetics', 'fashion',
                       'jewelry', 'wellness', 'childcare', 'beauty', 'maternity'],
        'rate_per_day': [5000, 4000, 4500, 5500, 3500, 3000, 2500, 3200, 4200, 4800,
                        5200, 3800, 3300, 3700, 3500],
        'women_specific': [False, False, False, False, False, False, False, False, True, True,
                          True, True, True, True, True],
        'target_demographic': ['all', 'all', 'all', 'all', 'all', 'all', 'all', 'all', 'women', 'women',
                              'women', 'women', 'parents', 'women', 'women']
    }
    
    return pd.DataFrame(data)