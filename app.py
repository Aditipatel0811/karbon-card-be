from flask import Flask, request, jsonify
from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    financial_index = latest_financial_index(data)

    total_revenue_flag = total_revenue_5cr_flag(data, financial_index)
    borrowing_flag = borrowing_to_revenue_flag(data, financial_index)
    iscr_flag_value = iscr_flag(data, financial_index)

    return jsonify({
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_flag,
            "BORROWING_TO_REVENUE_FLAG": borrowing_flag,
            "ISCR_FLAG": iscr_flag_value
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
