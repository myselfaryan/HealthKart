# HealthKart Influencer Campaign ROI Dashboard

## Overview

The HealthKart Influencer Campaign ROI Dashboard is a comprehensive open-source analytics tool designed to track, analyze, and optimize the return on investment (ROI) of influencer marketing campaigns. Built specifically for HealthKart's multi-brand ecosystem including MuscleBlaze, HKVitals, and Gritzo, this dashboard provides deep insights into campaign performance, influencer effectiveness, and strategic recommendations for maximizing marketing ROI.

## Features

### Core Analytics
- **Real-time ROI Calculation**: Track return on investment across campaigns, influencers, and platforms
- **Incremental ROAS Analysis**: Measure incremental return on ad spend to understand true campaign impact
- **Performance Tracking**: Monitor key metrics including revenue, orders, engagement, and cost efficiency
- **Multi-dimensional Filtering**: Filter data by platform, category, campaign, product, and date ranges

### Advanced Insights
- **Influencer Performance Scoring**: Identify top and poor performing influencers with comprehensive efficiency metrics
- **Campaign Optimization**: Analyze campaign performance across different strategies and time periods
- **Platform Comparison**: Compare effectiveness across Instagram, YouTube, Twitter, and TikTok
- **Persona Analysis**: Understand which influencer categories and platform combinations drive best results

### Visualization & Reporting
- **Interactive Dashboards**: Streamlit-powered interface with real-time data visualization
- **Export Capabilities**: Download insights, performance data, and analysis reports in CSV format
- **Strategic Recommendations**: AI-generated actionable insights for campaign optimization
- **Executive Summary**: High-level overview for stakeholder reporting

## Technology Stack

- **Backend**: Python 3.11+
- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Analytics**: Custom ROI calculation engine

## Installation

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd healthkart_dashboard
   ```

2. **Install Dependencies**
   ```bash
   pip install streamlit pandas numpy plotly matplotlib seaborn
   ```

3. **Prepare Data**
   Ensure your data files are in the `data/` directory:
   - `influencers.csv`
   - `posts.csv`
   - `tracking_data.csv`
   - `payouts.csv`

4. **Generate Sample Data** (Optional)
   If you don't have real data, generate sample data:
   ```bash
   python simulate_data.py
   ```

5. **Validate Data**
   Verify data integrity:
   ```bash
   python validate_data.py
   ```

## Usage

### Starting the Dashboard

1. **Launch the Application**
   ```bash
   streamlit run enhanced_dashboard.py
   ```

2. **Access the Dashboard**
   Open your browser and navigate to `http://localhost:8501`

### Dashboard Navigation

#### Key Performance Metrics
The top section displays critical KPIs:
- Total Revenue
- Incremental Revenue
- Total Spend
- Overall ROI
- Incremental ROAS
- Poor Performers Count

#### Filters
Use the sidebar filters to customize your analysis:
- **Platform**: Filter by social media platform
- **Category**: Filter by influencer category
- **Campaign**: Filter by specific campaigns
- **Product**: Filter by product lines
- **Date Range**: Set custom date ranges for analysis

#### Analysis Tabs
- **Top Performers**: View highest-performing influencers
- **Poor Performers**: Identify underperforming influencers
- **Campaign Analysis**: Deep dive into campaign performance
- **Platform Analysis**: Compare platform effectiveness

## Data Model

### Influencers Dataset
```
- ID: Unique influencer identifier
- name: Influencer name
- category: Content category (Fitness, Beauty, Gaming, etc.)
- gender: Influencer gender
- follower_count: Number of followers
- platform: Primary platform (Instagram, YouTube, Twitter, TikTok)
```

### Posts Dataset
```
- influencer_id: Reference to influencer
- platform: Posting platform
- date: Post date
- URL: Post URL
- caption: Post caption
- reach: Post reach
- likes: Number of likes
- comments: Number of comments
```

### Tracking Data Dataset
```
- source: Traffic source platform
- campaign: Campaign identifier
- influencer_id: Reference to influencer
- user_id: User identifier
- product: Product purchased
- date: Transaction date
- orders: Number of orders
- revenue: Revenue generated
```

### Payouts Dataset
```
- influencer_id: Reference to influencer
- basis: Payment basis (post/order)
- rate: Payment rate
- orders: Number of orders (for order-based payments)
- total_payout: Total payment amount
```

## Analytics Methodology

### ROI Calculation
```
ROI = ((Revenue - Cost) / Cost) × 100
```

### Incremental ROAS Calculation
```
Incremental ROAS = Incremental Revenue / Total Spend
```
Where incremental revenue accounts for baseline conversion rates without influencer campaigns.

### Efficiency Metrics
- **Cost per Order**: Total payout divided by orders generated
- **Revenue per Follower**: Revenue divided by influencer follower count
- **Engagement Rate**: (Likes + Comments) / Reach × 100

### Performance Scoring
The dashboard uses a composite efficiency score combining:
- ROI (40% weight)
- ROAS (normalized, 40% weight)
- Revenue per follower (20% weight)

## Key Assumptions

1. **Baseline Conversion Rate**: 2% organic conversion rate without influencer campaigns
2. **Attribution Window**: All tracked conversions attributed to influencer campaigns
3. **Data Quality**: Assumes accurate tracking and reporting of all metrics
4. **Currency**: All financial metrics in Indian Rupees (₹)

## Insights and Recommendations

The dashboard generates strategic insights including:

### Performance Optimization
- Identification of high-ROI influencer segments
- Underperforming campaign analysis
- Budget reallocation recommendations

### Scaling Opportunities
- Top performer scaling potential
- Similar profile identification
- Investment prioritization

### Risk Management
- Poor performer identification
- Campaign optimization alerts
- Budget efficiency warnings

## Export and Reporting

### Available Exports
- **Insights Summary**: Key metrics and performance indicators
- **Top Performers**: Detailed influencer performance data
- **Campaign Analysis**: Campaign-level performance metrics
- **Platform Analysis**: Platform comparison data

### Report Generation
All exports are available in CSV format for further analysis in Excel, Google Sheets, or other analytics tools.

## Troubleshooting

### Common Issues

1. **Data Loading Errors**
   - Verify all CSV files are in the `data/` directory
   - Check file formatting and column names
   - Ensure no missing required columns

2. **Performance Issues**
   - Large datasets may require increased memory
   - Consider data filtering for better performance
   - Use date range filters to limit data scope

3. **Visualization Problems**
   - Clear browser cache if charts don't load
   - Ensure stable internet connection for Plotly charts
   - Check browser compatibility (Chrome recommended)

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Standards
- Follow PEP 8 Python style guidelines
- Add docstrings to all functions
- Include type hints where appropriate
- Write unit tests for new features

## License

This project is open-source and available under the MIT License.

## Support

For questions, issues, or feature requests:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed description
4. Contact the development team

## Acknowledgments

Built with modern data science and visualization tools to provide actionable insights for influencer marketing optimization. Special thanks to the open-source community for the foundational libraries that make this project possible.

---

**Version**: 1.0.0  
**Last Updated**: July 2025  

