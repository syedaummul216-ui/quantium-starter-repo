import pandas as pd

# Define the file paths
files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv"
]

# Using the columns we identified
column_names = ['product', 'price', 'quantity', 'date', 'region']

dataframes = []

for file in files:
    # Read the file
    df = pd.read_csv(file)

    # 1. Filter for only Pink Morsels
    # We use .str.lower() to be safe against 'Pink Morsel' vs 'pink morsel'
    df = df[df['product'].str.lower() == 'pink morsel']

    # 2. Clean Price: Remove '$' and convert to float
    df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)

    # 3. FIX: Convert quantity to numeric (this stops the error you saw)
    df['quantity'] = pd.to_numeric(df['quantity'])

    # 4. Calculate Sales
    df['sales'] = df['price'] * df['quantity']

    # 5. Keep only requested columns
    df = df[['sales', 'date', 'region']]

    dataframes.append(df)

# Combine everything
output_df = pd.concat(dataframes, ignore_index=True)

# Save output
output_df.to_csv("formatted_sales_data.csv", index=False)

print("Success! 'formatted_sales_data.csv' has been created without errors.")

