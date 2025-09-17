import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from advert_b import MetroAdvertisementPlanner, initialize_sample_data


# Page configuration
st.set_page_config(
    page_title="Kochin Metro Advertisement Planner",
    page_icon="🚇",
    layout="wide"
)

def create_adverb():
    # Custom CSS
    st.markdown("""
    <style>
        .main-header {font-size: 2.5rem; color: #1f77b4; text-align: center;}
        .section-header {font-size: 1.8rem; color: #1f77b4; border-bottom: 2px solid #1f77b4; padding-bottom: 0.3rem;}
        .highlight-box {background-color: #f0f2f6; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem;}
        .metric-value {font-size: 1.5rem; font-weight: bold; color: #1f77b4;}
        .recommendation-box {background-color: #e6f7ff; padding: 1rem; border-left: 4px solid #1890ff; border-radius: 0.3rem; margin: 1rem 0;}
        .stButton button {width: 100%;}
    </style>
    """, unsafe_allow_html=True)

    def format_currency(amount):
        """Format number as currency"""
        return f"₹{amount:,.2f}"

    # Initialize analyzer
    analyzer = MetroAdvertisementPlanner()
    
    # Title
    st.markdown('<h1 class="main-header">Kochin Metro Rail Limited</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">Advertisement Revenue Optimization System</h2>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'analyze_clicked' not in st.session_state:
        st.session_state.analyze_clicked = False
    if 'results' not in st.session_state:
        st.session_state.results = None
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Configuration")
        
        # Load advertisement data
        st.subheader("Advertisement Data")
        
        # Load the CSV file by default
        try:
            import os
            csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "advertisement_performance.csv")
            ads_data = pd.read_csv(csv_path)
            analyzer.load_ads_data(ads_data)
            st.success("Advertisement performance data loaded!")
        except Exception as e:
            st.error(f"Error loading CSV data: {e}")
            # Fallback to sample data
            if st.button("Use Sample Data"):
                ads_data = initialize_sample_data()
                analyzer.load_ads_data(ads_data)
                st.success("Sample data loaded!")
        
        # Optional: Upload alternative CSV file
        uploaded_file = st.file_uploader("Or upload alternative CSV file", type=["csv"])
        
        if uploaded_file is not None:
            try:
                ads_data = pd.read_csv(uploaded_file)
                analyzer.load_ads_data(ads_data)
                st.success("Alternative data uploaded successfully!")
            except Exception as e:
                st.error(f"Error loading uploaded data: {e}")
        
        # Campaign duration
        st.subheader("Campaign Settings")
        duration_days = st.slider("Campaign Duration (days)", min_value=1, max_value=365, value=30)
        
        # Peak hours adjustment
        st.subheader("Peak Hours Settings")
        morning_start, morning_end = st.slider("Morning Peak Hours", 0, 23, (7, 10))
        evening_start, evening_end = st.slider("Evening Peak Hours", 0, 23, (17, 20))
        analyzer.peak_hours = [(morning_start, morning_end), (evening_start, evening_end)]
        
        # Analyze button
        if st.button("Analyze Revenue Potential", type="primary", use_container_width=True):
            st.session_state.analyze_clicked = True
            with st.spinner("Analyzing revenue potential..."):
                st.session_state.results = analyzer.get_optimal_ads_allocation(duration_days)
    
    # Main content
    if not analyzer.ads_data.empty:
        # Display advertisement data
        st.markdown('<div class="section-header">Advertisement Data Overview</div>', unsafe_allow_html=True)
        st.dataframe(analyzer.ads_data, use_container_width=True)
        
        if st.session_state.analyze_clicked and st.session_state.results:
            results = st.session_state.results
            
            # Display results
            st.markdown('<div class="section-header">Optimization Results</div>', unsafe_allow_html=True)
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                st.metric("Total Revenue", format_currency(results['total_revenue']))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                st.metric("Women's Compartment Revenue", format_currency(results['women_comp_revenue']))
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                avg_frequency = sum(results['metro_frequencies'].values()) / 24
                st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                st.metric("Average Metro Frequency", f"{avg_frequency:.1f} trains/hour")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="highlight-box">', unsafe_allow_html=True)
                st.metric("Campaign Duration", f"{duration_days} days")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Metro frequency throughout the day
            st.subheader("Metro Frequency Throughout the Day")
            freq_df = pd.DataFrame.from_dict(
                results['metro_frequencies'], 
                orient='index', 
                columns=['frequency']
            ).reset_index()
            freq_df.columns = ['hour', 'frequency']
            
            fig = px.line(freq_df, x='hour', y='frequency', 
                        title='Metro Frequency by Hour of Day')
            fig.update_xaxes(title_text="Hour of Day", dtick=1)
            fig.update_yaxes(title_text="Trains per Hour")
            st.plotly_chart(fig, use_container_width=True)
            
            # Revenue by company
            st.subheader("Revenue by Company")
            company_revenues = pd.DataFrame.from_dict(
                results['company_revenues'], 
                orient='index', 
                columns=['revenue']
            ).reset_index()
            company_revenues.columns = ['company_id', 'revenue']
            
            # Merge with company names - handle both CSV and sample data structures
            if 'company_name' in analyzer.ads_data.columns:
                merge_columns = ['company_id', 'company_name', 'category']
            else:
                # Use advertiser column from CSV
                merge_columns = ['company_id', 'advertiser', 'category']
                analyzer.ads_data = analyzer.ads_data.rename(columns={'advertiser': 'company_name'})
            
            company_revenues = company_revenues.merge(
                analyzer.ads_data[merge_columns], 
                on='company_id'
            )
            
            # Create visualization
            fig = px.bar(company_revenues, x='company_name', y='revenue', color='category',
                        title='Revenue by Company', labels={'company_name': 'Company', 'revenue': 'Revenue'})
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
            
            # Feminine ads for women's compartments
            st.subheader("Recommended Ads for Women's Compartments")
            feminine_ads = pd.DataFrame(results['feminine_ads'])
            if not feminine_ads.empty:
                st.dataframe(feminine_ads, use_container_width=True)
                
                # Display feminine ads percentage
                feminine_percentage = (len(feminine_ads) / len(analyzer.ads_data)) * 100
                women_revenue_percentage = (results['women_comp_revenue'] / results['total_revenue']) * 100
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Feminine Ads Percentage", f"{feminine_percentage:.1f}%")
                with col2:
                    st.metric("Women's Compartment Revenue Share", f"{women_revenue_percentage:.1f}%")
                
                # Feminine ads revenue breakdown
                st.subheader("Feminine Ads Revenue Breakdown")
                feminine_revenues = []
                for ad in results['feminine_ads']:
                    revenue = analyzer.calculate_revenue_potential(
                        ad['company_id'], duration_days, "women_compartment"
                    )
                    # Handle both CSV and sample data structures
                    company_name = ad.get('company_name', ad.get('advertiser', 'Unknown'))
                    feminine_revenues.append({
                        'company_name': company_name,
                        'revenue': revenue,
                        'category': ad['category']
                    })
                
                feminine_rev_df = pd.DataFrame(feminine_revenues)
                fig = px.pie(feminine_rev_df, values='revenue', names='company_name',
                            title='Revenue Distribution of Feminine Ads')
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                st.info("No feminine-specific ads found in the current dataset.")
            
            # Recommendations
            st.subheader("Recommendations")
            for recommendation in results['recommendations']:
                st.markdown(f'<div class="recommendation-box">{recommendation}</div>', unsafe_allow_html=True)
            
            # Additional analysis: Revenue by category
            st.subheader("Revenue by Category")
            category_revenue = analyzer.ads_data.copy()
            category_revenue['revenue'] = category_revenue['company_id'].apply(
                lambda x: results['company_revenues'].get(x, 0)
            )
            category_summary = category_revenue.groupby('category')['revenue'].sum().reset_index()
            
            fig = px.pie(category_summary, values='revenue', names='category',
                        title='Revenue Distribution by Category')
            st.plotly_chart(fig, use_container_width=True)
            
            # Download results
            st.subheader("Export Results")
            
            # Create downloadable results
            company_names = []
            for cid in results['company_revenues'].keys():
                company_data = analyzer.ads_data[analyzer.ads_data['company_id'] == cid]
                if not company_data.empty:
                    # Handle both CSV and sample data structures
                    if 'company_name' in company_data.columns:
                        company_names.append(company_data['company_name'].values[0])
                    elif 'advertiser' in company_data.columns:
                        company_names.append(company_data['advertiser'].values[0])
                    else:
                        company_names.append('Unknown')
                else:
                    company_names.append('Unknown')
            
            results_df = pd.DataFrame({
                'Company': company_names,
                'Revenue': list(results['company_revenues'].values()),
                'Revenue_Share': [rev/results['total_revenue']*100 for rev in results['company_revenues'].values()]
            })
            
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="kochin_metro_ad_analysis.csv",
                mime="text/csv",
            )
    
    else:
        st.info("Please upload advertisement data or use sample data to get started.")
        
        # Show sample data preview
        if st.button("Preview Sample Data"):
            sample_data = initialize_sample_data()
            st.dataframe(sample_data, use_container_width=True)
            
            # Show sample analysis
            if st.button("Run Sample Analysis"):
                analyzer.load_ads_data(sample_data)
                st.session_state.analyze_clicked = True
                with st.spinner("Analyzing sample data..."):
                    st.session_state.results = analyzer.get_optimal_ads_allocation(30)
                st.rerun()


if __name__ == "__main__":
    create_adverb()
