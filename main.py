from flask import Flask, request, jsonify
import pandas as pd
from io import StringIO

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Check if 'data' file was uploaded
    if 'data' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    csv_file = request.files['data']

    try:
        # Read CSV file directly (no need for StringIO if Flask handles file stream)
        df = pd.read_csv(csv_file)

        # Safety checks (optional but good)
        required_cols = {'Revenue', 'Region', 'Product', 'Unit_Price', 'Date'}
        if not required_cols.issubset(df.columns):
            return jsonify({'error': 'Missing required columns in the dataset'}), 400

        # Key metrics
        total_rows = len(df)
        total_revenue = df['Revenue'].sum()
        top_region = df.groupby('Region')['Revenue'].sum().idxmax()
        top_product = df.groupby('Product')['Revenue'].sum().idxmax()
        avg_unit_price = df['Unit_Price'].mean()
        daily_revenue = df.groupby('Date')['Revenue'].sum().reset_index()

        # Format summary
        summary = f"""Total rows: {total_rows}
Total Revenue: ${total_revenue:,.2f}
Top Region by Revenue: {top_region}
Top Product by Revenue: {top_product}
Average Unit Price: ${avg_unit_price:.2f}

Daily Revenue:
{daily_revenue.to_string(index=False)}"""

        return jsonify({"metrics_summary": summary})

    except Exception as e:
        # Log actual error message (can log it somewhere in production)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
