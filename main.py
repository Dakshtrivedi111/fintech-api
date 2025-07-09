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

        # Step 4: Calculate metrics
        try:
            total_loans = len(df)
            approved_rate = (df['Loan_Status'] == 'Approved').mean()
            rejected_rate = (df['Loan_Status'] == 'Rejected').mean()
            default_rate = (df['Defaulted'] == 'Yes').mean()
            avg_loan_amount = df['Loan_Amount'].mean()
            avg_interest = df['Interest_Rate'].mean()
            top_loan_type = df['Loan_Type'].value_counts().idxmax()
            top_region = df['Region'].value_counts().idxmax()
        except Exception as e:
            return jsonify({"error": f"Error during metric calculation: {str(e)}"}), 500

        # Step 5: Format results
        try:
            summary = {
    "Total Loans": total_loans,
    "Approval Rate (%)": round(approved_rate * 100, 2),
    "Rejection Rate (%)": round(rejected_rate * 100, 2),
    "Default Rate (%)": round(default_rate * 100, 2),
    "Average Loan Amount": round(avg_loan_amount, 2),
    "Average Interest Rate (%)": round(avg_interest, 2),
    "Most Common Loan Type": top_loan_type,
    "Top Region": top_region
}
        except Exception as e:
            return jsonify({"error": f"Error formatting summary: {str(e)}"}), 500

        return jsonify({"metrics_summary": summary})

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
