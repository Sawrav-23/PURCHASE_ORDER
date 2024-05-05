from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Read the dataset
df = pd.read_csv("C:\\Users\\sawra\\Downloads\\decobee\\inventory.csv")

# Calculate quantity sold (inventory size - current stock)
df['Quantity Sold'] = df['Inventory Size'] - df['Current Stock']

# Sort products by quantity sold in descending order
df_sorted_quantity = df.sort_values(by='Quantity Sold', ascending=False)

# Function to generate purchase order based on quantity sold
def generate_purchase_order_quantity(amount):
    remaining_amount = amount
    purchase_order = []
    
    for index, row in df_sorted_quantity.iterrows():
        product_id = row['Product ID']
        product_name = row['Product Name']
        selling_price = row['Selling Price']
        current_stock = row['Current Stock']
        inventory_size = row['Inventory Size']
        cost_price = row['Cost Price']
        quantity_sold = row['Quantity Sold']
        
        if remaining_amount <= 0:
            break
        
        # Determine quantity to purchase
        quantity_to_purchase = min(inventory_size - current_stock, remaining_amount // cost_price)
        quantity_to_purchase = min(quantity_sold, quantity_to_purchase)
        
        # Add to purchase order
        if quantity_to_purchase > 0:
            purchase_order.append({
                'Product ID': product_id,
                'Product Name': product_name,
                'Quantity': quantity_to_purchase,
                'Cost': quantity_to_purchase * cost_price,
                'Selling Price': selling_price,
                'Total Cost': quantity_to_purchase * cost_price
            })
            remaining_amount -= quantity_to_purchase * selling_price
    
    return purchase_order

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_purchase_order', methods=['POST'])
def generate_purchase_order():
    total_amount_quantity = int(request.form['total_amount'])
    purchase_order_quantity = generate_purchase_order_quantity(total_amount_quantity)
    return render_template('purchase_order.html', purchase_order=purchase_order_quantity)

