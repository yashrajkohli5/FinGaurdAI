# 🛡️ FinGuard AI: End-to-End Credit Risk Pipeline

FinGuard AI is a full-stack machine learning solution designed to predict loan default probability. This project covers the entire ML lifecycle: from **structured data ingestion** and **Exploratory Data Analysis (EDA)** to **high-performance model training** and **real-time deployment**.

## 📋 Project Overview
Credit risk assessment is critical for financial institutions to minimize capital loss. This project builds a decision-support system that identifies high-risk applicants by analyzing variables like debt-to-income ratios, employment history, and historical credit behavior.

---

## 🔬 Methodology & Model Development

### 1. Data Acquisition & SQL Integration
* **Source:** Historical credit risk data containing 32,000+ records.
* **Storage:** Data was managed via a relational database (SQL) to ensure ACID compliance and structured querying during the ingestion phase.

### 2. Exploratory Data Analysis (EDA)
* **Outlier Detection:** Identified and handled extreme values in `person_income` and `person_emp_length` using the Interquartile Range (IQR) method.
* **Feature Correlation:** Utilized Seaborn heatmaps to identify that **Loan-to-Income Ratio** and **Loan Interest Rate** were the strongest predictors of default.
* **Class Imbalance:** Discovered a significant skew toward non-defaulters (80/20 split), necessitating a shift in evaluation metrics from Accuracy to **Recall and F1-Score**.

### 3. Feature Engineering & Preprocessing
* **Encoding:** Implemented `LabelEncoder` for categorical variables (`Home Ownership`, `Loan Intent`, `Loan Grade`).
* **Scaling:** Normalized numerical features to ensure the XGBoost algorithm converges efficiently.
* **Feature Selection:** Selected 11 core features based on mutual information gain.

### 4. Model Training (XGBoost)
* **Algorithm:** Chose **XGBoost (Extreme Gradient Boosting)** for its superior performance with tabular data and its ability to handle missing values natively.
* **Threshold Tuning:** To prioritize risk mitigation, the classification threshold was tuned to **0.3**. This increases **Recall**, ensuring that potential defaulters are flagged even at the cost of slight over-classification of risk.

---

## 🛠️ Tech Stack
* **Data Science:** Python (Pandas, NumPy, Scikit-Learn, XGBoost).
* **Visualization:** Matplotlib, Seaborn.
* **Backend API:** FastAPI, Uvicorn, Pydantic.
* **Frontend UI:** Streamlit (Customized CSS for Financial Dashboards).
  
