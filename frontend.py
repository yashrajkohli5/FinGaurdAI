import streamlit as st
import requests
import joblib

# Page Config
st.set_page_config(page_title="FinGuard AI | Dashboard", page_icon="🛡️", layout="wide")

# Load encoders
try:
    encoders = joblib.load('artifacts/encoders.pkl')
except Exception as e:
    st.error(f"Error loading artifacts: {e}")
    st.stop()

# --- ENHANCED PROFESSIONAL SIDEBAR ---
with st.sidebar:
    # 1. Branding & Logo Area
    st.markdown("""
        <div style='text-align: center;'>
            <h1 style='color: #007bff; margin-bottom: 0;'>🛡️ FinGuard AI</h1>
            <p style='color: #6c757d; font-size: 0.9rem;'>Risk Decision Engine v1.2.0</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("---")

    # 2. Real-Time System Health Monitoring
    st.subheader("🌐 System Health")
    try:
        # Pinging the FastAPI root to check connectivity
        backend_check = requests.get("http://127.0.0.1:8000/", timeout=1)
        if backend_check.status_code == 200:
            st.success("● API Backend: CONNECTED")
        else:
            st.warning("● API Backend: ERROR 500")
    except:
        st.error("● API Backend: DISCONNECTED")
    
    # 3. Model Specifications (Read-only Info)
    st.subheader("⚙️ Analysis Engine")
    with st.container():
        st.write("**Model:** XGBoost Classifier")
        st.write("**Sensitivity:** High (Recall-Focused)")
        st.write("**Threshold:** 0.30")
        st.caption("Threshold is tuned to minimize False Negatives in credit lending.")

    st.write("---")

    # 4. Contextual Documentation (Interactive)
    st.subheader("📖 Reference Guide")
    with st.expander("Risk Classification"):
        st.write("🟢 **Safe (0.0 - 0.3):** Standard approval.")
        st.write("🔴 **High Risk (> 0.3):** Requires manual review or higher collateral.")
    
    with st.expander("Key Features Explained"):
        st.write("**Loan Grade:** Internal risk score from A (best) to G (worst).")
        st.write("**Debt-to-Income:** Ratio of requested loan vs. annual earnings.")

    st.write("---")
    
    # 5. Footer / Session Info
    st.caption("FinGuard AI is a predictive tool. Final lending decisions should involve human oversight.")
    st.markdown("<div style='text-align: center; font-size: 0.8rem; color: #999;'>© 2026 FinGuard Solutions</div>", unsafe_allow_html=True)

# --- MAIN INTERFACE ---
st.title("Credit Risk Assessment Portal")
st.write("Enter applicant details below to generate a risk profile.")

with st.form("input_form"):
    # Personal Information Section
    st.subheader("👤 Applicant Personal Profile")
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age", 18, 100, 25, help="Current age of the applicant in years.")
    with c2:
        income = st.number_input("Annual Income ($)", min_value= 1 , value= 50000, help="Total yearly earnings before taxes.")
    with c3:
        emp_len = st.number_input("Employment (Years)", 0, 50, 2, help="Years at current job.")
    
    c4, c5 = st.columns(2)
    with c4:
        home = st.selectbox("Home Ownership", options=encoders['person_home_ownership'].classes_, help="Housing status (Rent, Own, Mortgage, etc.).")
    with c5:
        cred_hist = st.number_input("Credit History (Years)", 0, 50, 5, help="Years since first credit account was opened.")

    st.markdown("---")
    
    # Loan Information Section
    st.subheader("💰 Loan & Financial Details")
    l1, l2, l3 = st.columns(3)
    with l1:
        amount = st.number_input("Loan Amount ($)", 1, 500000, 10000, help="Total amount requested for the loan.")
    with l2:
        int_rate = st.number_input("Interest Rate (%)", 0.0, 30.0, 11.0, help="Annual interest rate (APR) for this loan.")
    with l3:
        intent = st.selectbox("Loan Intent", options=encoders['loan_intent'].classes_, help="Primary purpose for the loan.")
    
    l4, l5 = st.columns(2)
    with l4:
        grade = st.selectbox("Loan Grade", options=encoders['loan_grade'].classes_, help="Risk rating (A is safest, G is highest risk).")
    with l5:
        default = st.selectbox("Historical Default?", options=encoders['cb_person_default_on_file'].classes_, help="Has the applicant ever defaulted before?")

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.form_submit_button("Analyze Risk")

# --- RESULTS AREA ---
if submit:
    # Prepare payload for FastAPI
    payload = {
        "person_age": int(age),
        "person_income": float(income),
        "person_home_ownership": str(home),
        "person_emp_length": float(emp_len),
        "loan_intent": str(intent),
        "loan_grade": str(grade),
        "loan_amnt": float(amount),
        "loan_int_rate": float(int_rate),
        "loan_percent_income": float(amount / income),
        "cb_person_default_on_file": str(default),
        "cb_person_cred_hist_length": int(cred_hist)
    }
    
    try:
        # Request to Backend
        res = requests.post("http://127.0.0.1:8000/predict", json=payload)
        
        if res.status_code == 200:
            data = res.json()
            st.markdown("### 📊 Analysis Report")
            
            m1, m2, m3 = st.columns(3)
            prob = data['risk_probability']
            is_high = prob > 0.3
            
            # Display results in metrics
            m1.metric("Risk Status", data['prediction'], delta="CRITICAL" if is_high else "SECURE", delta_color="inverse" if is_high else "normal")
            m2.metric("Default Probability", f"{prob:.2%}")
            m3.metric("Debt-to-Income", f"{(amount/income):.2f}")

            # Summary alerts
            if is_high:
                st.error(f"🚨 **High Risk Warning:** Probability of {prob:.2%} exceeds safety threshold.")
            else:
                st.success(f"✅ **Safe Profile:** Applicant meets criteria with {prob:.2%} default probability.")
        else:
            st.error(f"Backend Error: {res.json().get('detail', 'Unknown error')}")
            
    except Exception as e:
        st.error("Connection Error: Is the FastAPI server running on port 8000?")