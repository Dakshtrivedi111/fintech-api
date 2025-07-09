from flask import Flask, jsonify
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)

@app.route('/analyze', methods=['GET'])
def analyze_csv():
    # Replace with your actual direct-download link from Google Drive
    download_url = "https://drive.google.com/uc?id=1fmp7K5fM9PgE0hWyg2MuJETA_g54oMYK&export=download"

    try:
        # Step 1: Download CSV content
        try:
            response = requests.get(download_url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Failed to download file: {str(e)}"}), 500

        # Step 2: Parse CSV
        try:
            csv_data = StringIO(response.text)
            df = pd.read_csv(csv_data)
        except Exception as e:
            return jsonify({"error": f"Failed to decode and read CSV: {str(e)}"}), 400

        # Step 4: Perform metrics calculation
        try:
            
            total_rows = len(df)
            total_revenue = df['Revenue'].sum()
            top_region = df.groupby('Region')['Revenue'].sum().idxmax()
            top_product = df.groupby('Product')['Revenue'].sum().idxmax()
            avg_unit_price = df['Unit_Price'].mean()
            daily_revenue = df.groupby('Date')['Revenue'].sum().reset_index()
        except Exception as e:
            return jsonify({"error": f"Error during data aggregation: {str(e)}"}), 500

        # Step 5: Format response
        try:
             summary = f"""Total rows: {total_rows}\nTotal Revenue: ${total_revenue:,.2f}\nTop Region by Revenue: {top_region}\nTop Product by Revenue: {top_product}\nAverage Unit Price: ${avg_unit_price:.2f}\n\nDaily Revenue:\n{daily_revenue.to_string(index=False)}"""except Exception as e:
        except Exception as e:
            return jsonify({"error": f"Error formatting response: {str(e)}"}), 500

        return jsonify({"metrics_summary": summary})

    except Exception as e:
        # Fallback for any unexpected errors
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)

