from flask import Flask, request, jsonify
import pandas as pd
from io import StringIO

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'data' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    csv_file = request.files['data']
    df = pd.read_csv(csv_file)
    total_rows = len(df)
    total_revenue = df['Revenue'].sum()
    top_region = df.groupby('Region')['Revenue'].sum().idxmax()
    top_product = df.groupby('Product')['Revenue'].sum().idxmax()
    avg_unit_price = df['Unit_Price'].mean()
    daily_revenue = df.groupby('Date')['Revenue'].sum().reset_index()

    summary = f"""Total rows: {total_rows}\nTotal Revenue: ${total_revenue:,.2f}\nTop Region by Revenue: {top_region}\nTop Product by Revenue: {top_product}\nAverage Unit Price: ${avg_unit_price:.2f}\n\nDaily Revenue:\n{daily_revenue.to_string(index=False)}"""

    return jsonify({ "metrics_summary": summary })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
