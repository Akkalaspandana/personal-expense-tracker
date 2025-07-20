"""
Sample Data Generator for Personal Expense Tracker
This script populates the database with sample expense data for demonstration purposes.
"""

import sqlite3
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample expense data for demonstration"""
    
    # Sample categories and payment methods
    categories = [
        "Food & Dining", "Transportation", "Shopping", "Entertainment", 
        "Healthcare", "Utilities", "Housing", "Education", "Travel", "Mobile & Internet", "Other"
    ]
    
    payment_methods = [
        "Cash", "Credit Card", "Debit Card", "Bank Transfer", "Digital Wallet", "Other"
    ]
    
    # Sample descriptions for each category
    descriptions = {
        "Food & Dining": [
            "Lunch at Chipotle", "Dinner at Italian Restaurant", "Coffee at Starbucks",
            "Grocery shopping", "Fast food", "Pizza delivery", "Breakfast at diner",
            "Snacks at convenience store", "Dinner with friends", "Takeout Chinese"
        ],
        "Transportation": [
            "Uber ride", "Gas station", "Public transit", "Parking fee",
            "Car maintenance", "Taxi fare", "Bike rental", "Train ticket",
            "Airport shuttle", "Car wash"
        ],
        "Shopping": [
            "New headphones", "Clothing at mall", "Electronics store",
            "Home decor", "Books", "Shoes", "Accessories", "Gift for friend",
            "Kitchen supplies", "Office supplies"
        ],
        "Entertainment": [
            "Movie ticket", "Concert tickets", "Netflix subscription",
            "Video game", "Bowling", "Arcade games", "Theater show",
            "Sports event", "Museum admission", "Escape room"
        ],
        "Healthcare": [
            "Doctor visit", "Pharmacy", "Dental checkup", "Eye exam",
            "Prescription medication", "Vitamins", "First aid supplies",
            "Gym membership", "Physical therapy", "Medical supplies"
        ],
        "Utilities": [
            "Electricity bill", "Water bill", "Internet service",
            "Phone bill", "Gas bill", "Trash service", "Cable TV",
            "Home security", "Lawn service", "Cleaning service"
        ],
        "Housing": [
            "Rent payment", "Mortgage payment", "Home insurance",
            "Property tax", "Home repairs", "Furniture", "Appliances",
            "Moving expenses", "Storage unit", "Home improvement"
        ],
        "Education": [
            "Tuition payment", "Textbooks", "Online course",
            "Workshop fee", "Conference registration", "Study materials",
            "Software license", "Library fee", "Tutoring", "Certification exam"
        ],
        "Travel": [
            "Hotel booking", "Flight tickets", "Rental car",
            "Travel insurance", "Souvenirs", "Tour guide", "Airport parking",
            "Travel apps", "Luggage", "Travel adapter"
        ],
        "Other": [
            "ATM withdrawal", "Bank fee", "Charity donation",
            "Pet expenses", "Legal fees", "Tax preparation", "Insurance premium",
            "Investment", "Loan payment", "Emergency fund"
        ]
    }
    
    # Generate sample data for the last 3 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    # Connect to database
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    cursor.execute("DELETE FROM expenses")
    
    # Generate random expenses
    current_date = start_date
    expense_id = 1
    
    while current_date <= end_date:
        # Generate 1-5 expenses per day
        num_expenses = random.randint(1, 5)
        
        for _ in range(num_expenses):
            # Random category
            category = random.choice(categories)
            
            # Random description from the category
            description = random.choice(descriptions[category])
            
            # Random amount (different ranges for different categories)
            if category == "Housing":
                amount = round(random.uniform(800, 2500), 2)
            elif category == "Transportation":
                amount = round(random.uniform(20, 150), 2)
            elif category == "Food & Dining":
                amount = round(random.uniform(8, 80), 2)
            elif category == "Shopping":
                amount = round(random.uniform(15, 200), 2)
            elif category == "Entertainment":
                amount = round(random.uniform(10, 100), 2)
            elif category == "Healthcare":
                amount = round(random.uniform(15, 300), 2)
            elif category == "Utilities":
                amount = round(random.uniform(50, 200), 2)
            elif category == "Education":
                amount = round(random.uniform(20, 500), 2)
            elif category == "Travel":
                amount = round(random.uniform(50, 1000), 2)
            else:
                amount = round(random.uniform(5, 100), 2)
            
            # Random payment method
            payment_method = random.choice(payment_methods)
            
            # Insert expense
            cursor.execute('''
                INSERT INTO expenses (id, date, category, description, amount, payment_method)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (expense_id, current_date.strftime('%Y-%m-%d'), category, description, amount, payment_method))
            
            expense_id += 1
        
        # Move to next day
        current_date += timedelta(days=1)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully created {expense_id - 1} sample expenses!")
    print(f"📅 Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"💰 Total amount: ${sum([random.uniform(5, 200) for _ in range(expense_id - 1)]):,.2f} (approximate)")

if __name__ == "__main__":
    print("🎯 Generating sample data for Personal Expense Tracker...")
    create_sample_data()
    print("\n🚀 You can now run 'streamlit run app.py' to see your sample data!") 