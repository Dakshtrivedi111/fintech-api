from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_loans():
    try:
        # Parse JSON input
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Convert list of dicts to DataFrame
        df = pd.DataFrame(data)

        # Check required columns
        required_cols = ['Loan_Status', 'Defaulted', 'Loan_Amount', 'Interest_Rate', 'Loan_Type', 'Region']
        if not all(col in df.columns for col in required_cols):
            return jsonify({"error": "Missing required columns in data"}), 400

        # Calculate metrics
        total_loans = len(df)
        approved_rate = (df['Loan_Status'] == 'Approved').mean()
        rejected_rate = (df['Loan_Status'] == 'Rejected').mean()
        default_rate = (df['Defaulted'] == 'Yes').mean()
        avg_loan_amount = df['Loan_Amount'].mean()
        avg_interest = df['Interest_Rate'].mean()
        top_loan_type = df['Loan_Type'].value_counts().idxmax()
        top_region = df['Region'].value_counts().idxmax()

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

        return jsonify(summary)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
