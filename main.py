from flask import Flask, jsonify
import pandas as pd
import requests
from io import StringIO
import csv

app = Flask(__name__)

@app.route('/analyze', methods=['GET'])
def analyze_csv():
    # Replace this with your direct downloadable link
    download_url = "https://drive.google.com/uc?id=1fmp7K5fM9PgE0hWyg2MuJETA_g54oMYK&export=download"

    try:
        # Step 1: Download CSV content
        try:
            response = requests.get(download_url, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Failed to download file: {str(e)}"}), 500

        # Step 2: Try decoding the CSV
        try:
            content = response.content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                content = response.content.decode('latin-1')
            except Exception as e:
                return jsonify({"error": f"Failed to decode file: {str(e)}"}), 400
                

        # Step 3: Read into pandas
        try:
            csv_data = StringIO(content)
            df = pd.read_csv(
                csv_data,
                sep=None,           # Let pandas auto-detect separator
                engine='python',    # Use Python engine to handle malformed lines
                quoting=csv.QUOTE_MINIMAL,
                on_bad_lines='skip' # For pandas >= 1.3
            )
        except Exception as e:
            return jsonify({"error": f"Failed to parse CSV: {str(e)}"}), 400

    
        return jsonify({"columns": list(df.columns) })

        

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
