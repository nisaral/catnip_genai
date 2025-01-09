venv\Scripts\activate
import random
import string
import pandas as pd

# Helper function to generate random string for IDs and names
def random_string(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Generate customer support data
def generate_customer_support_data(order_ids):
    customer_support_data = []
    for order_id in order_ids:
        customer_support_data.append({
            'Ticket ID': random_string(),
            'Customer ID': random_string(),
            'Customer Name': f'Customer_{random_string(5)}',
            'Email Address': f'{random_string(5)}@example.com',
            'Phone Number': f'+1-{random.randint(1000000000, 9999999999)}',
            'Support Issue Category': random.choice(['Refund', 'Inquiry', 'Complaint', 'Feedback']),
            'Issue Description': f'Issue description for order {order_id}',
            'Ticket Priority': random.choice(['High', 'Medium', 'Low']),
            'Ticket Status': random.choice(['Open', 'Closed', 'In Progress']),
            'Support Representative': f'Representative_{random_string(5)}',
            'Resolution Description': f'Resolution for order {order_id}',
            'Resolution Date': random.choice(['2023-12-10', '2023-12-15', '2023-12-20']),
            'Ticket Created Date': random.choice(['2023-12-01', '2023-12-10', '2023-12-20']),
            'Ticket Closed Date': random.choice(['2023-12-10', '2023-12-25', '2023-12-30']),
            'Customer Satisfaction Rating': random.randint(1, 5),
            'Follow-up Status': random.choice(['Pending', 'Completed']),
            'Customer Location': f'Location_{random_string(5)}',
            'Product ID (Linked to Issue)': random_string(),
            'Communication Channel': random.choice(['Email', 'Phone', 'Chat']),
            'Escalation Level': random.choice(['Level 1', 'Level 2', 'Level 3']),
            'Resolution Time': random.randint(1, 10),
            'Assigned Team': f'Team_{random_string(3)}'
        })
    return customer_support_data

# Generate FAQ data
def generate_faq_data(order_ids):
    faq_data = []
    for order_id in order_ids:
        faq_data.append({
            'FAQ ID': random_string(),
            'Question': random.choice(['How to track my order?', 'How can I get a refund?', 'How do I cancel my order?']),
            'Answer': random.choice(['Visit your account page.', 'Refund is processed in 3-5 business days.', 'Orders can be canceled within 24 hours.']),
            'Category': random.choice(['Order Management', 'Returns', 'Shipping']),
            'Last Updated Date': random.choice(['2023-12-01', '2023-12-10', '2023-12-20']),
            'Status': random.choice(['Active', 'Inactive']),
            'Related Links': f'www.example.com/{random_string(5)}',
            'Tags': f'{random_string(5)},{random_string(5)}',
            'FAQ Views': random.randint(100, 1000),
            'Related Articles': f'Article_{random_string(5)}',
            'FAQ Type': random.choice(['General', 'Product-related']),
            'Language': random.choice(['English', 'Spanish', 'French']),
            'FAQ Author': f'Author_{random_string(5)}'
        })
    return faq_data

# Generate order data
def generate_order_data(order_ids):
    order_data = []
    for order_id in order_ids:
        order_data.append({
            'Order ID': order_id,
            'Order Date': random.choice(['2023-12-01', '2023-12-10', '2023-12-15']),
            'Customer Name': f'Customer_{random_string(5)}',
            'Order Status': random.choice(['Processing', 'Shipped', 'Delivered']),
            'Delivery Date': random.choice(['2023-12-10', '2023-12-15', '2023-12-20']),
            'Shipment Mode': random.choice(['Air', 'Sea', 'Land']),
            'Order Value': round(random.uniform(10.0, 500.0), 2),
            'Product Description': f'Product_{random_string(5)}',
            'Project Code': random_string(5),
            'Tracking ID': random_string(),
            'Customer Email': f'{random_string(5)}@example.com',
            'Shipping Address': f'{random_string(10)} Street, City, Country',
            'Payment Status': random.choice(['Paid', 'Unpaid']),
            'Order Total': round(random.uniform(50.0, 1000.0), 2),
            'Tracking URL': f'www.example.com/{random_string(5)}',
            'Order Priority': random.choice(['High', 'Medium', 'Low']),
            'Customer Rating': random.randint(1, 5),
            'Product ID': random_string(),
            'Shipping Cost': round(random.uniform(5.0, 50.0), 2),
            'Return Status': random.choice(['Returned', 'Not Returned']),
            'Discount Applied': random.choice(['Yes', 'No']),
            'Payment Method': random.choice(['Credit Card', 'PayPal', 'Bank Transfer']),
            'Coupon Code': f'CODE{random.randint(1000, 9999)}',
            'Billing Address': f'{random_string(10)} Street, City, Country',
            'Gift Option': random.choice(['Yes', 'No']),
            'Estimated Delivery Date': random.choice(['2023-12-10', '2023-12-15', '2023-12-20']),
            'Shipping Carrier': random.choice(['FedEx', 'UPS', 'DHL']),
            'Tracking Status': random.choice(['In Transit', 'Out for Delivery', 'Delivered'])
        })
    return order_data

# Generate shipment data
def generate_shipment_data(order_ids):
    shipment_data = []
    for order_id in order_ids:
        shipment_data.append({
            'Order ID': order_id,
            'Tracking ID': random_string(),
            'Shipment Mode': random.choice(['Air', 'Sea', 'Land']),
            'Shipping Address': f'{random_string(10)} Street, City, Country',
            'Customer Email': f'{random_string(5)}@example.com',
            'Delivery Date': random.choice(['2023-12-10', '2023-12-15', '2023-12-20']),
            'Order Value': round(random.uniform(50.0, 500.0), 2),
            'Product Description': f'Product_{random_string(5)}',
            'Shipment Status': random.choice(['Shipped', 'In Transit', 'Delivered']),
            'Order Total': round(random.uniform(50.0, 1000.0), 2),
            'Tracking URL': f'www.example.com/{random_string(5)}',
            'Product ID': random_string(),
            'Return Status': random.choice(['Returned', 'Not Returned']),
            'Estimated Delivery Date': random.choice(['2023-12-10', '2023-12-15', '2023-12-20']),
            'Delivery Time Window': f'{random.randint(8, 12)}:00 - {random.randint(12, 17)}:00',
            'Shipping Carrier': random.choice(['FedEx', 'UPS', 'DHL']),
            'Customs Clearance Status': random.choice(['Cleared', 'Pending']),
            'Tracking Events': f'Event_{random_string(5)}',
            'Shipment Cost': round(random.uniform(10.0, 50.0), 2)
        })
    return shipment_data

# Generate product data
def generate_product_data(order_ids):
    product_data = []
    for order_id in order_ids:
        product_data.append({
            'Product ID': random_string(),
            'Product Name': random.choice(['Laptop', 'Smartphone', 'Headphones', 'Monitor']),
            'Product Category': random.choice(['Electronics', 'Home Appliances', 'Clothing']),
            'Product Description': f'Product_{random_string(5)}',
            'Price': round(random.uniform(10.0, 500.0), 2),
            'Stock Quantity': random.randint(1, 100),
            'Supplier Name': f'Supplier_{random_string(3)}',
            'Supplier Contact': f'{random_string(5)}@supplier.com',
            'Warranty Period': random.randint(1, 3),
            'Product Dimensions': f'{random.randint(5, 20)}x{random.randint(5, 20)}x{random.randint(5, 20)} cm',
            'Manufacturing Date': random.choice(['2023-01-01', '2023-03-15', '2023-07-30']),
            'Expiration Date': random.choice(['2024-01-01', '2025-01-01', '2026-01-01']),
            'SKU': random_string(6),
            'Product Tags': f'{random_string(3)},{random_string(3)}',
            'Color/Size Variations': random.choice(['Red/Small', 'Blue/Medium', 'Green/Large']),
            'Product Availability (Online/Store)': random.choice(['Online', 'Store', 'Both']),
            'Minimum Order Quantity': random.randint(1, 5),
            'Return Policy': random.choice(['30 Days', 'No Returns', 'Exchange Only']),
            'Seasonal Product': random.choice(['Yes', 'No']),
            'Supplier Location': f'Location_{random_string(5)}',
            'Manufacturing Process': random.choice(['Automated', 'Manual']),
            'Product Ratings': random.randint(1, 5),
            'Product Images': f'img_{random_string(5)}.jpg'
        })
    return product_data

# Generate common order_ids
order_ids = [random_string(10) for _ in range(10000)]

# Generate data
customer_support_data = generate_customer_support_data(order_ids)
faq_data = generate_faq_data(order_ids)
order_data = generate_order_data(order_ids)
shipment_data = generate_shipment_data(order_ids)
product_data = generate_product_data(order_ids)

# Save to CSV files
customer_support_df = pd.DataFrame(customer_support_data)
faq_df = pd.DataFrame(faq_data)
order_df = pd.DataFrame(order_data)
shipment_df = pd.DataFrame(shipment_data)
product_df = pd.DataFrame(product_data)

# Specify file paths
base_path = '/Users/krishilparikh/Desktop/SynCom-FinanceMitra/KB'
customer_support_file = base_path + 'customer_support.csv'
faq_file = base_path + 'faq.csv'
orders_file = base_path + 'orders.csv'
shipments_file = base_path + 'shipments.csv'
products_file = base_path + 'products.csv'

# Save DataFrames to CSV files
customer_support_df.to_csv(customer_support_file, index=False)
faq_df.to_csv(faq_file, index=False)
order_df.to_csv(orders_file, index=False)
shipment_df.to_csv(shipments_file, index=False)
product_df.to_csv(products_file, index=False)

# Print paths to saved files
print(f"Customer Support file saved to: {customer_support_file}")
print(f"FAQ file saved to: {faq_file}")
print(f"Orders file saved to: {orders_file}")
print(f"Shipments file saved to: {shipments_file}")
print(f"Products file saved to: {products_file}")
