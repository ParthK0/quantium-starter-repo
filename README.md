# Soul Foods - Pink Morsel Sales Analysis

## Overview
This project analyzes sales data for Soul Foods' Pink Morsel product line to answer the key business question: **Were sales higher before or after the Pink Morsel price increase on January 15, 2021?**

## Answer
**Sales increased by 35.85% after the price increase!**
- Average daily sales BEFORE Jan 15, 2021: **$6,604.14**
- Average daily sales AFTER Jan 15, 2021: **$8,971.57**

## Project Structure
```
quantium-starter-repo/
├── data/
│   ├── daily_sales_data_0.csv    # Raw sales data (2018)
│   ├── daily_sales_data_1.csv    # Raw sales data (2019)
│   ├── daily_sales_data_2.csv    # Raw sales data (2020-2021)
│   └── output.csv                 # Processed Pink Morsel sales data
├── process_sales_data.py          # Data processing script
├── app.py                         # Dash visualization app
└── requirements.txt               # Python dependencies
```

## Installation

### Prerequisites
- Python 3.9+ (Python 3.13 used in this project)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/ParthK0/quantium-starter-repo.git
cd quantium-starter-repo
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Data Processing
Process the raw CSV files to extract Pink Morsel sales data:
```bash
python process_sales_data.py
```

This script:
- Reads all three CSV files
- Filters for Pink Morsel products only
- Calculates sales (price × quantity)
- Outputs formatted data to `data/output.csv`

### Visualization
Launch the Dash app to visualize the sales data:
```bash
python app.py
```

Then open your browser to: http://127.0.0.1:8050/

The dashboard includes:
- **Header**: Clear title and subtitle
- **Main Chart**: Total daily sales with price increase marker
- **Regional Breakdown**: Sales by region (North, South, East, West)
- **Key Insights**: Statistical summary showing the impact of the price increase

## Data Processing Details

### Input Format
Each CSV file contains:
- `product`: Morsel type (pink morsel, gold morsel, etc.)
- `price`: Price per unit (e.g., $3.00)
- `quantity`: Units sold
- `date`: Transaction date
- `region`: Sales region (north, south, east, west)

### Output Format
Processed `output.csv` contains:
- `sales`: Total sales amount (price × quantity)
- `date`: Transaction date
- `region`: Sales region

### Filtering Criteria
- **Product**: Only "pink morsel" (case-insensitive)
- **Date Range**: 2018-02-06 to 2021-11-12
- **Total Records**: 5,880 Pink Morsel transactions (from 41,160 total)

## Key Findings

The visualization clearly demonstrates that the price increase on January 15, 2021 had a **positive impact** on sales revenue:

1. **Revenue Growth**: 35.85% increase in average daily sales
2. **Sustained Performance**: Sales remained consistently higher after the increase
3. **Regional Consistency**: The increase was observed across all regions

This suggests that the price elasticity for Pink Morsels was favorable, and customers were willing to pay the higher price without significantly reducing quantity purchased.

## Technologies Used
- **Python 3.13**: Core programming language
- **Pandas**: Data processing and analysis
- **Dash**: Interactive web application framework
- **Plotly**: Data visualization library

## Repository
https://github.com/ParthK0/quantium-starter-repo
