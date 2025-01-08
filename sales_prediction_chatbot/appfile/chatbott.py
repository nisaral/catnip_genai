import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors
from typing import Dict, List, Optional

class Product:
    def __init__(self, id: str, name: str, category: str, subcategory: str, 
                 base_price: float, min_price: float, max_price: float,
                 stock_limit: int, reorder_point: int, supplier_lead_time: int,
                 gst_rate: float):
        self.id = id
        self.name = name
        self.category = category
        self.subcategory = subcategory
        self.base_price = base_price  # in INR
        self.min_price = min_price
        self.max_price = max_price
        self.stock_limit = stock_limit
        self.reorder_point = reorder_point
        self.supplier_lead_time = supplier_lead_time  # in days
        self.gst_rate = gst_rate  # GST rate in percentage

class IndianBusinessRules:
    def __init__(self):
        self.max_discount_percentage = 40  # Higher discounts during festivals
        self.min_margin_percentage = 12
        self.bulk_order_threshold = 25
        self.bulk_order_discount = 15
        self.festive_markup = 20
        self.max_stock_age = 180  # days
        self.minimum_stock_level = 10
        self.maximum_order_quantity = 1000
        
        # Festival-specific rules
        self.festival_discounts = {
            'Diwali': 15,
            'Dhanteras': 25,
            'Dussehra': 20,
            'Ganesh Chaturthi': 10,
            'Republic Day': 16,
            'Independence Day': 12,
            'Raksha Bandhan': 7
        }
        
        # EMI thresholds (in INR)
        self.min_emi_amount = 3000
        self.emi_tenures = [3, 6, 9, 12,18]

class SalesPredictionChatbot:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.sales_data = None
        self.embeddings = None
        self.knn = None
        self.products = {}
        self.business_rules = IndianBusinessRules()
        self.setup_product_catalog()
        
    def setup_product_catalog(self):
        """detailed product catalog for Indian market"""
        # Smartphones
        self.products['PH001'] = Product('PH001', 'iPhone 15', 'Electronics', 'Smartphones', 
                                       79999, 74999, 84999, 100, 20, 7, 18)
        self.products['PH002'] = Product('PH002', 'Samsung S24', 'Electronics', 'Smartphones',
                                       69999, 64999, 74999, 150, 30, 7, 18)
        self.products['PH003'] = Product('PH003', 'OnePlus 12', 'Electronics', 'Smartphones',
                                       59999, 54999, 64999, 200, 40, 7, 18)
        self.products['PH004'] = Product('PH004', 'RedmiNOte 13 pro+', 'Electronics', 'Smartphones',
                                       22999, 27999, 30000, 200, 40, 7, 18)                            
        
        # Laptops
        self.products['LP001'] = Product('LP001', 'MacBook Air', 'Electronics', 'Laptops',
                                       99999, 94999, 104999, 50, 10, 14, 18)
        self.products['LP002'] = Product('LP002', 'HP Pavilion', 'Electronics', 'Laptops',
                                       54999, 49999, 59999, 75, 15, 10, 18)
        self.products['LP003'] = Product('LP003', 'Asus vivobook16x', 'Electronics', 'Laptops',
                                       89999, 69999, 59999, 75, 15, 10, 18)
        # TVs
        self.products['TV001'] = Product('TV001', 'Samsung 55" Smart TV', 'Electronics', 'Television',
                                       59999, 54999, 64999, 40, 8, 14, 28)
        self.products['TV002'] = Product('TV002', 'MI 43" Smart TV', 'Electronics', 'Television',
                                       29999, 27999, 32999, 60, 12, 10, 28)
        
        # Home Appliances
        self.products['HA001'] = Product('HA001', 'LG 5 Star AC', 'Appliances', 'Air Conditioners',
                                       45999, 42999, 48999, 30, 6, 7, 28)
        self.products['HA002'] = Product('HA002', 'Samsung Double Door Fridge', 'Appliances', 'Refrigerators',
                                       38999, 35999, 41999, 25, 5, 7, 28)
        self.products['HA003'] = Product('HA003', 'Philips Air Purifier', 'Appliances', 'Air Treatment',
                                       12999, 11499, 14499, 35, 9, 11, 25) # Peak in pollution season

        #Home & Living
        self.products['HL001'] = Product('HL001', 'Memory Foam Mattress', 'Home', 'Bedroom',
                                       15999, 14499, 17499, 25, 4, 12, 30) # Wedding season peak
        self.products['HL002'] = Product('HL002', 'Air Tight Storage Containers', 'Home', 'Kitchen',
                                       1299, 999, 1499, 40, 3, 12, 50)     # Year-round necessity
        self.products['HL003'] = Product('HL003', 'Mosquito Net', 'Home', 'Protection',
                                       799, 599, 899, 45, 3, 8, 35)        # Monsoon season peak
        self.products['HL004'] = Product('HL004', 'Humidity Controller', 'Home', 'Air Treatment',
                                       4999, 4499, 5499, 35, 5, 9, 25)     # Monsoon demand
        self.products['HL005'] = Product('HL005', 'Electric Blanket', 'Home', 'Bedroom',
                                       2999, 2499, 3499, 40, 10, 2, 20)    # Winter season peak
        # Kitchen Appliances
        self.products['KA001'] = Product('KA001', 'Microwave Oven', 'Appliances', 'Kitchen',
                                       9999, 8999, 10999, 30, 4, 12, 35)   # Festival season peak
        self.products['KA002'] = Product('KA002', 'Food Processor', 'Appliances', 'Kitchen',
                                       5999, 5499, 6499, 35, 3, 12, 30)    # Wedding season demand
        self.products['KA003'] = Product('KA003', 'Coffee Maker', 'Appliances', 'Kitchen',
                                       3999, 3499, 4499, 40, 4, 12, 25)    # Year-round sales
        self.products['KA004'] = Product('KA004', 'Induction Cooktop', 'Appliances', 'Kitchen',
                                       2499, 2199, 2799, 45, 3, 12, 40)    # Consistent demand
        self.products['KA005'] = Product('KA005', 'Air Fryer', 'Appliances', 'Kitchen',
                                       6999, 6499, 7499, 35, 4, 12, 30)    # Festival season peak                                                    





    def get_indian_festivals(self, year):
        """Get major Indian festivals with dates for a given year"""
        # Note: Dates are approximate as many festivals follow lunar calendar
        festivals = {
            f'{year}-10-22': 'Dussehra',
            f'{year}-11-01': 'Dhanteras',
            f'{year}-11-03': 'Diwali',
            f'{year}-08-15': 'Independence Day',
            f'{year}-01-26': 'Republic Day',
            f'{year}-08-30': 'Raksha Bandhan',  # Approximate date
            f'{year}-09-19': 'Ganesh Chaturthi',  # Approximate date
            f'{year}-01-14': 'Makar Sankranti',
            f'{year}-08-29': 'Onam',  # Approximate date
            f'{year}-03-25': 'Holi',  # Approximate date
            f'{year}-04-14': 'New Year Sales'  # Multiple regional new years(eg.jain new year,parsi new year)
        }
        return festivals

    def load_sample_data(self):
        """ preparing  detailed sample sales data for Indian market"""
        
        dates = pd.date_range(start='2023-01-01', periods=730, freq='D')
        
        #seasonal patterns
        seasons = pd.cut(pd.Series(dates.month), 
                        bins=[0, 2, 5, 8, 11, 12],
                        labels=['Winter', 'Summer', 'Monsoon', 'Post-Monsoon', 'Winter'])
        
        # Combining festivals for both years
        festivals = {**self.get_indian_festivals(2022), **self.get_indian_festivals(2023)}
        
        data = []
        for date in dates:
            # Determining if it's a festival
            festival = festivals.get(date.strftime('%Y-%m-%d'), None)
            
            #  multiple sales records per day
            daily_records = np.random.randint(5, 15)  # Higher volume for Indian market
            
            for _ in range(daily_records):
                product = np.random.choice(list(self.products.values()))
                
                # Calculating base quantity with Indian market patterns
                base_quantity = np.random.normal(20, 8)
                
                # seasonal effects
                season = seasons[dates.get_loc(date)]
                if season == 'Summer' and product.category == 'Appliances':
                    base_quantity *= 1.5  # Higher AC/Fridge sales in summer
                elif season == 'Monsoon' and product.subcategory == 'Television':
                    base_quantity *= 1.3  # Higher indoor entertainment during monsoon
                
                
                # festival effects
                if festival:
                    festival_multiplier = 2.5 if festival in ['Diwali', 'Dhanteras'] else 1.8
                    base_quantity *= festival_multiplier
                
                
                # weekend effects
                if date.weekday() >= 5:
                    base_quantity *= 1.3  # Higher weekend sales in Indian market
                
                # Calculate price with promotions and festival discounts
                base_price = product.base_price
                promotion = np.random.choice([True, False], p=[0.4, 0.6])  # Higher promotion frequency
                
                if promotion:
                    if festival:
                        discount = self.business_rules.festival_discounts.get(festival, 15)
                    else:
                        discount = np.random.uniform(5, self.business_rules.max_discount_percentage)
                    price = base_price * (1 - discount/100)
                else:
                    price = base_price
                
                # Apply GST
                price_with_gst = price * (1 + product.gst_rate/100)
                
                # EMI availability
                emi_available = price_with_gst >= self.business_rules.min_emi_amount
                
                quantity = max(1, int(base_quantity + np.random.normal(0, 3)))
                quantity = min(quantity, self.business_rules.maximum_order_quantity)
                
                data.append({
                    'date': date,
                    'product_id': product.id,
                    'product_name': product.name,
                    'category': product.category,
                    'subcategory': product.subcategory,
                    'sales_quantity': quantity,
                    'base_price': base_price,
                    'price_before_gst': price,
                    'price_with_gst': price_with_gst,
                    'gst_rate': product.gst_rate,
                    'season': season,
                    'festival': festival,
                    'promotion': promotion,
                    'is_weekend': date.weekday() >= 5,
                    'stock_level': np.random.randint(product.reorder_point, product.stock_limit),
                    'emi_available': emi_available
                })
        
        self.sales_data = pd.DataFrame(data)
        self.sales_data['context'] = self.sales_data.apply(self.create_context_description, axis=1)
        self.embeddings = self.encoder.encode(self.sales_data['context'].tolist())
        
        self.knn = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.knn.fit(self.embeddings)

    def create_context_description(self, row):
        """Create detailed context description for each sale"""
        context = (
            f"On {row['date'].strftime('%Y-%m-%d')}, {row['product_name']} "
            f"({row['category']}/{row['subcategory']}) sold {row['sales_quantity']} units "
            f"at ₹{row['price_with_gst']:.2f} (Base: ₹{row['base_price']:.2f}, "
            f"GST: {row['gst_rate']}%) during {row['season']} season"
        )
        
        if row['festival']:
            context += f" during {row['festival']}"
        
        context += (
            f"{' with promotion' if row['promotion'] else ' without promotion'}"
            f"{' on weekend' if row['is_weekend'] else ' on weekday'}"
            f"{' (EMI available)' if row['emi_available'] else ''}"
            f" with stock level at {row['stock_level']}"
        )
        
        return context

    def predict_sales(self, query):
        """Generate sales prediction based on similar historical cases"""
        similar_cases, distances = self.get_similar_cases(query)
        
        weights = 1 / (distances + 1e-6)
        weighted_sales = np.average(similar_cases['sales_quantity'], weights=weights)
        
        confidence = (1 - np.mean(distances)) * 100
        
        avg_price = similar_cases['price_with_gst'].mean()
        avg_discount = ((similar_cases['base_price'] - similar_cases['price_before_gst']) / 
                       similar_cases['base_price'] * 100).mean()
        
        return {
            'predicted_sales': round(weighted_sales),
            'confidence': round(confidence, 2),
            'similar_cases': similar_cases,
            'avg_price': round(avg_price, 2),
            'avg_discount': round(avg_discount, 2),
            'total_revenue': round(weighted_sales * avg_price, 2)
        }

    def generate_response(self, query):
        """Generate a detailed response to the query"""
        if not isinstance(self.sales_data, pd.DataFrame):
            return "Please load sales data first using load_sample_data() method."
            
        prediction = self.predict_sales(query)
        
        response = (
            f"Based on Indian market patterns, I predict:\n"
            f"- Sales Volume: {prediction['predicted_sales']} units\n"
            f"- Average Price (with GST): ₹{prediction['avg_price']}\n"
            f"- Expected Revenue: ₹{prediction['total_revenue']}\n"
            f"- Average Discount: {prediction['avg_discount']}%\n"
            f"- Prediction Confidence: {prediction['confidence']}%\n\n"
            f"This prediction is based on these similar historical cases:\n"
        )
        
        for _, case in prediction['similar_cases'].iterrows():
            response += f"- {case['context']}\n"
            
        return response