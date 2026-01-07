import pandas as pd
import glob

# Read all three CSV files
csv_files = glob.glob('data/daily_sales_data_*.csv')
dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Combine all dataframes
combined_df = pd.concat(dataframes, ignore_index=True)

# Filter for Pink Morsels only (case insensitive)
pink_morsels_df = combined_df[combined_df['product'].str.lower() == 'pink morsel'].copy()

# Remove dollar sign from price and convert to float
pink_morsels_df['price'] = pink_morsels_df['price'].str.replace('$', '').astype(float)

# Calculate sales (price * quantity)
pink_morsels_df['sales'] = pink_morsels_df['price'] * pink_morsels_df['quantity']

# Select only the required columns and rename them
output_df = pink_morsels_df[['sales', 'date', 'region']].copy()
output_df.columns = ['sales', 'date', 'region']

# Sort by date for better organization
output_df = output_df.sort_values('date')

# Save to output file
output_df.to_csv('data/output.csv', index=False)

print(f"Processing complete!")
print(f"Total rows in combined data: {len(combined_df)}")
print(f"Pink Morsel rows: {len(pink_morsels_df)}")
print(f"Output saved to data/output.csv")
print(f"\nFirst few rows of output:")
print(output_df.head(10))
