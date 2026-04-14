let lastAnalysis = null;

// Loan Analysis
async function analyzeLoan() {
    const res = await fetch("http://127.0.0.1:5000/analyze-loan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            income: Number(income.value),
            expenses: Number(expenses.value),
            amount: Number(amount.value),
            tenure: Number(tenure.value),
            interest: Number(interest.value)
        })
    });

    const data = await res.json();
    lastAnalysis = data;

    result.innerHTML = `
        <p><b>EMI:</b> ₹${data.emi}</p>
        <p><b>Total Payable:</b> ₹${data.total_payable}</p>
        <p><b>Total Interest:</b> ₹${data.total_interest}</p>
        <p><b>Eligibility:</b> ${data.eligibility_score}</p>
        <p><b>Stress Score:</b> ${data.stress_score}</p>
    `;

    // Risk Alerts
    if (data.stress_score < 40) {
        risk_alert.innerHTML = "⚠️ HIGH RISK: Loan may cause financial stress";
        risk_alert.style.background = "#ff4d4d";
    } else if (data.stress_score < 70) {
        risk_alert.innerHTML = "⚠️ MODERATE RISK: Consider safer terms";
        risk_alert.style.background = "#ffae42";
    } else {
        risk_alert.innerHTML = "✅ SAFE: Loan profile looks healthy";
        risk_alert.style.background = "#2ecc71";
    }

    // Dashboard values
    d_emi.innerText = "₹" + data.emi;
    d_stress.innerText = data.stress_score;
    d_eligibility.innerText = data.eligibility_score;

    drawChart(data.emi, data.total_interest);
}

// Credit Score
async function calculateCreditScore() {
    const res = await fetch("http://127.0.0.1:5000/credit-score", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            income: Number(income.value),
            expenses: Number(expenses.value),
            emi: lastAnalysis.emi,
            stress_score: lastAnalysis.stress_score
        })
    });

    const data = await res.json();
    credit_score_output.innerHTML = `
        <p><b>Score:</b> ${data.score}</p>
        <p><b>Status:</b> ${data.status}</p>
    `;
    d_credit.innerText = data.score;
}

// Loan Comparison
async function compareLoans() {
    const res = await fetch("http://127.0.0.1:5000/compare-loans", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            amount1: 300000,
            rate1: 12,
            tenure1: 36,
            amount2: 300000,
            rate2: 10,
            tenure2: 48
        })
    });

    const data = await res.json();
    compare_output.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
}

// AI Advisor (unchanged)
function askAI() {
    ai_reply.innerText =
        lastAnalysis.eligibility_score > 60
        ? "This loan looks financially safe."
        : "This loan may cause financial stress.";
}

// History placeholder
function loadHistory() {
    history.innerHTML = "<p>(History feature coming soon)</p>";
}

// Chart
function drawChart(emi, interest) {
    new Chart(myChart, {
        type: "pie",
        data: {
            labels: ["Monthly EMI", "Total Interest"],
            datasets: [{
                data: [emi, interest],
                backgroundColor: ["#00ffbb", "#ff6384"]
            }]
        }
    });
}
