from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/analyze-loans', methods=['POST'])
def analyze_loans():
    try:
        # Get JSON input
        data = request.get_json()

        # Validate input is a list of dicts
        if not isinstance(data, list):
            return jsonify({"error": "Expected a list of records (list of dictionaries)"}), 400

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Check required columns
        #required_cols = ['customer_ID','Loan_Amount','Loan_Status','Interest_Rate','Tenure_Months','Monthly_Income','EMI','Defaulted','Region','Loan_Type','Disbursal_Date']
        #if not all(col in df.columns for col in required_cols):
            #return jsonify({"error": "Missing required columns in data"}), 400

        # Convert to numeric and date
        df['Loan_Amount'] = pd.to_numeric(df['Loan_Amount'], errors='coerce')
        df['Interest_Rate'] = pd.to_numeric(df['Interest_Rate'], errors='coerce')
        df['customer_ID'] = pd.to_numeric(df['customer_ID'], errors='coerce')
        df['Tenure_Months'] = pd.to_numeric(df['Tenure_Months'], errors='coerce')
        df['Monthly_Income'] = pd.to_numeric(df['Monthly_Income'], errors='coerce')
        df['EMI'] = pd.to_numeric(df['EMI'], errors='coerce')
        df['Disbursal_Date'] = pd.to_numeric(df['Disbursal_Date'], errors='coerce')
        
        

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
