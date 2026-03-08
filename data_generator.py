import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

def generate_synthetic_data(num_rows=100, output_file="messy_bank_statements.csv"):
    fake = Faker('en_IN')
    data = []
    
    # Base real-world Indian banking transaction templates
    transaction_templates = [
        "UPI/Merchant/{merchant}",
        "NEFT/Transfer/{name}",
        "Netflix/Autopay",
        "Spotify/Autopay",
        "SIP/MutualFund/{amc}",
        "POS/Retail/{merchant}",
        "ATM/Withdrawal/Cash",
        "Zomato/UPI",
        "Swiggy/UPI"
    ]
    
    merchants = ["Amazon", "Flipkart", "RelianceMart", "DMart", "BigBasket", "Uber", "Ola"]
    amcs = ["HDFC_MF", "SBI_MF", "Zerodha_Coin", "Groww", "ICICI_Prudential"]
    
    start_date = datetime.now() - timedelta(days=90)
    
    for _ in range(num_rows - 4):  # Save 4 rows for intentional duplicates
        template = random.choice(transaction_templates)
        
        # Fill in the templates
        if "{merchant}" in template:
            desc = template.format(merchant=random.choice(merchants))
            amount = round(random.uniform(100, 5000), 2)
        elif "{name}" in template:
            desc = template.format(name=fake.first_name())
            amount = round(random.uniform(500, 20000), 2)
        elif "{amc}" in template:
            desc = template.format(amc=random.choice(amcs))
            amount = round(random.choice([1000, 2000, 5000, 10000]), 2)
        elif "Autopay" in template:
            desc = template
            amount = 649.00 if "Netflix" in template else 119.00
        else:
            desc = template
            amount = round(random.uniform(100, 3000), 2)
            
        date = start_date + timedelta(days=random.randint(0, 90))
        
        data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Description": desc,
            "Amount": amount,
            "Type": "Debit"
        })
        
    # Injecting intentional duplicate subscription charges
    duplicates = [
        {"Date": (start_date + timedelta(days=15)).strftime("%Y-%m-%d"), "Description": "Netflix/Autopay", "Amount": 649.00, "Type": "Debit"},
        {"Date": (start_date + timedelta(days=16)).strftime("%Y-%m-%d"), "Description": "Netflix/Autopay", "Amount": 649.00, "Type": "Debit"}, # Duplicate!
        {"Date": (start_date + timedelta(days=40)).strftime("%Y-%m-%d"), "Description": "Spotify/Autopay", "Amount": 119.00, "Type": "Debit"},
        {"Date": (start_date + timedelta(days=40)).strftime("%Y-%m-%d"), "Description": "Spotify/Autopay", "Amount": 119.00, "Type": "Debit"}  # Duplicate!
    ]
    data.extend(duplicates)
    
    df = pd.DataFrame(data)
    # Shuffle the dataset to make it messy
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv(output_file, index=False)
    print(f"Generated {len(df)} rows of synthetic data in '{output_file}'")

if __name__ == "__main__":
    generate_synthetic_data()
