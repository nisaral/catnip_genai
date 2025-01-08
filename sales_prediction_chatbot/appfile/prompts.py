from string import Template

# System prompts
SYSTEM_PROMPT = """You are an expert Indian retail market sales prediction AI assistant. You have deep knowledge of:
- Indian festival seasons and shopping patterns
- Regional market trends and preferences
- Product categories and pricing strategies
- GST rules and EMI offerings
- Seasonal buying behaviors
- Brand preferences across different regions

Analyze the given sales data and context to provide accurate predictions and insights.
"""

# Base prompt templates for different prediction scenarios
SALES_PREDICTION_TEMPLATE = Template("""
Based on the following context and historical data, predict sales for $product during $time_period:

Historical Data:
$historical_data

Current Context:
- Product: $product ($category)
- Base Price: ₹$base_price
- Current Season: $season
- Festival/Event: $festival
- Promotion Active: $has_promotion
- Region: $region

Consider these factors:
1. Historical sales patterns
2. Seasonal trends
3. Festival impact
4. Regional preferences
5. Current market conditions
6. Competitor pricing
7. Stock availability

Provide:
1. Predicted sales volume
2. Expected revenue
3. Key factors influencing prediction
4. Confidence level
5. Recommendations
""")

FESTIVAL_SPECIFIC_TEMPLATE = Template("""
Analyze festival-specific sales potential for $product during $festival:

Festival Details:
- Festival: $festival
- Typical Duration: $duration
- Shopping Period Starts: $shopping_start
- Peak Days: $peak_days

Historical Festival Performance:
$historical_festival_data

Product Details:
$product_details

Consider:
1. Traditional festival buying patterns
2. Regional significance
3. Gift-giving customs
4. Cultural preferences
5. Competition offerings
6. Historical festival performance
""")

REGIONAL_ANALYSIS_TEMPLATE = Template("""
Analyze regional sales potential for $product in $region:

Regional Context:
- Region: $region
- Primary Language: $language
- Key Cities: $cities
- Income Bracket: $income_bracket
- Competition Level: $competition_level

Regional Preferences:
$regional_preferences

Historical Regional Performance:
$historical_regional_data

Provide:
1. Region-specific sales forecast
2. Local market opportunities
3. Cultural considerations
4. Pricing recommendations
4. Marketing suggestions
""")

COMPETITOR_ANALYSIS_TEMPLATE = Template("""
Analyze competitive positioning for $product:

Market Context:
$market_context

Key Competitors:
$competitor_data

Product Comparison:
$product_comparison

Provide:
1. Competitive advantages
2. Price positioning
3. Feature comparison
4. Market share potential
5. Threat assessment
""")

PROMOTION_PLANNING_TEMPLATE = Template("""
Recommend promotion strategy for $product:

Product Details:
$product_details

Historical Promotion Performance:
$historical_promotions

Market Context:
$market_context

Suggest:
1. Optimal discount range
2. Promotion timing
3. Bundle opportunities
4. EMI offers
5. Expected uplift
""")

INVENTORY_PREDICTION_TEMPLATE = Template("""
Predict inventory requirements for $product:

Current Stock: $current_stock
Reorder Point: $reorder_point
Lead Time: $lead_time

Historical Sales Pattern:
$historical_sales

Upcoming Events:
$upcoming_events

Consider:
1. Seasonal demands
2. Festival impacts
3. Storage costs
4. Perishability
5. Supply chain constraints
""")

CUSTOMER_QUERY_TEMPLATES = {
    "price_prediction": Template("What will be the best price for $product during $period?"),
    "stock_recommendation": Template("How much stock of $product should we maintain for $period?"),
    "festival_planning": Template("How should we plan inventory for $product during $festival?"),
    "promotion_timing": Template("When is the best time to promote $product and what offers should we give?"),
    "regional_strategy": Template("How should we adjust our strategy for $product in $region?"),
    "competitor_response": Template("How should we position $product against $competitor_product?"),
    "seasonal_adjustment": Template("How should we adjust pricing for $product during $season?")
}

# Response templates for structured outputs
PREDICTION_RESPONSE_TEMPLATE = Template("""
Sales Prediction Analysis for $product

📊 Forecast:
- Expected Sales Volume: $sales_volume units
- Predicted Revenue: ₹$revenue
- Growth vs Previous Period: $growth%

🎯 Confidence Level: $confidence%

Key Factors:
$key_factors

📈 Trends:
$trends

💡 Recommendations:
$recommendations

⚠️ Risk Factors:
$risks
""")

FESTIVAL_RESPONSE_TEMPLATE = Template("""
Festival Sales Analysis for $product during $festival

🎉 Festival Impact:
- Expected Sales Uplift: $sales_uplift%
- Peak Shopping Days: $peak_days
- Recommended Stock: $recommended_stock units

💰 Pricing Strategy:
- Recommended MRP: ₹$recommended_mrp
- Optimal Discount: $discount%
- EMI Options: $emi_options

📢 Marketing Focus:
$marketing_suggestions

🎁 Bundle Opportunities:
$bundle_suggestions
""")

def get_prediction_prompt(product_data, context_data):
    """Generate complete prediction prompt based on product and context"""
    return SALES_PREDICTION_TEMPLATE.substitute(
        product=product_data['name'],
        time_period=context_data['time_period'],
        historical_data=context_data['historical_data'],
        category=product_data['category'],
        base_price=product_data['base_price'],
        season=context_data['season'],
        festival=context_data.get('festival', 'None'),
        has_promotion=context_data.get('has_promotion', False),
        region=context_data.get('region', 'National')
    )

def get_festival_prompt(product_data, festival_data):
    """Generate festival-specific analysis prompt"""
    return FESTIVAL_SPECIFIC_TEMPLATE.substitute(
        product=product_data['name'],
        festival=festival_data['name'],
        duration=festival_data['duration'],
        shopping_start=festival_data['shopping_start'],
        peak_days=festival_data['peak_days'],
        historical_festival_data=festival_data['historical_data'],
        product_details=product_data
    )

# Add more prompt generation functions as needed