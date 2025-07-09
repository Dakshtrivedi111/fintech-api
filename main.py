from flask import Flask, request, jsonify
import pandas as pd
import base64
from io import BytesIO

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Parse JSON payload
        try:
            data = request.get_json()
            if not data or 'filedata' not in data:
                return jsonify({'error': 'Missing "filedata" in request body'}), 400
        except Exception as e:
            return jsonify({'error': f'Invalid JSON payload: {str(e)}'}), 400

        # Decode base64 CSV content
        try:
            file_b64 = data['filedata']
            decoded_file = base64.b64decode(file_b64)
            csv_buffer = BytesIO(decoded_file)
            df = pd.read_csv(csv_buffer)
        except Exception as e:
            return jsonify({'error': f'Failed to decode and read CSV: {str(e)}'}), 400

        # Check required columns
        required_cols = {'Revenue', 'Region', 'Product', 'Unit_Price', 'Date'}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            return jsonify({'error': f'Missing required columns: {missing_cols}'}), 400

        # Calculate metrics with safety
        try:
            total_rows = len(df)
            total_revenue = df['Revenue'].sum()
            top_region = df.groupby('Region')['Revenue'].sum().idxmax()
            top_product = df.groupby('Product')['Revenue'].sum().idxmax()
            avg_unit_price = df['Unit_Price'].mean()
            daily_revenue = df.groupby('Date')['Revenue'].sum().reset_index()
        except Exception as e:
            return jsonify({'error': f'Error calculating metrics: {str(e)}'}), 500

        # Format summary
        try:
            summary = f"""Total rows: {total_rows}
Total Revenue: ${total_revenue:,.2f}
Top Region by Revenue: {top_region}
Top Product by Revenue: {top_product}
Average Unit Price: ${avg_unit_price:.2f}

Daily Revenue:
{daily_revenue.to_string(index=False)}"""
        except Exception as e:
            return jsonify({'error': f'Error formatting summary: {str(e)}'}), 500

        return jsonify({"metrics_summary": summary})

    except Exception as e:
        return jsonify({'error': f'Unexpected server error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
