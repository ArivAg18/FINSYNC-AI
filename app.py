from flask import Flask, request, jsonify
from flask_cors import CORS

# Existing imports
from backend.emi import calculate_emi_details
from backend.eligibility import analyze_eligibility, generate_suggestions
from backend.credit_score import calculate_credit_score

# Gemini AI imports
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "FinSync AI Backend Running"


# ---------------- LOAN ANALYSIS ----------------
@app.route("/analyze-loan", methods=["POST"])
def analyze_loan():
    data = request.json

    emi_info = calculate_emi_details(
        data["amount"], data["interest"], data["tenure"]
    )

    eligibility = analyze_eligibility(
        data["income"], data["expenses"], emi_info["emi"]
    )

    suggestions = generate_suggestions(
        data["income"],
        data["expenses"],
        eligibility["emi_ratio"],
        eligibility["stress_score"]
    )

    return jsonify({
        **emi_info,
        **eligibility,
        "suggestions": suggestions
    })


# ---------------- CREDIT SCORE ----------------
@app.route("/credit-score", methods=["POST"])
def credit_score():
    d = request.json
    return jsonify(
        calculate_credit_score(
            d["income"], d["expenses"], d["emi"], d["stress_score"]
        )
    )


# ---------------- LOAN COMPARISON ----------------
@app.route("/compare-loans", methods=["POST"])
def compare_loans():
    d = request.json

    loan1 = calculate_emi_details(d["amount1"], d["rate1"], d["tenure1"])
    loan2 = calculate_emi_details(d["amount2"], d["rate2"], d["tenure2"])

    better = "Loan 1" if loan1["total_payable"] < loan2["total_payable"] else "Loan 2"

    return jsonify({
        "loan1": loan1,
        "loan2": loan2,
        "better_option": better
    })


# ---------------- GEMINI SMART AI ----------------
@app.route("/ask-ai-gemini", methods=["POST"])
def ask_ai_gemini():
    d = request.json

    prompt = f"""
You are FinSync AI Smart Advisor powered by Gemini.

User question:
{d['question']}

Loan details:
- EMI: {d['emi']}
- Eligibility Score: {d['eligibility_score']}
- Stress Score: {d['stress_score']}
- Credit Score: {d['credit_score']}

Give a simple, clear explanation with advice.
"""

    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception:
        return jsonify({"reply": "Gemini AI could not respond. Try again."})


if __name__ == "__main__":
    app.run(debug=True)
