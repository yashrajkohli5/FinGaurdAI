import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, Numeric, MetaData, Table

DB_URL = "postgresql://postgres:admin1234@localhost:5432/finance_db"
engine = create_engine(DB_URL)
metadata = MetaData()

credit_risk_table = Table(
    'credit_risk_data', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('person_age', Integer),
    Column('person_income', Numeric(12, 2)),
    Column('person_home_ownership', String(20)),
    Column('person_emp_length', Float),
    Column('loan_intent', String(50)),
    Column('loan_grade', String(5)),
    Column('loan_amnt', Numeric(12, 2)),
    Column('loan_int_rate', Float),
    Column('loan_status', Integer),
    Column('loan_percent_income', Float),
    Column('cb_person_default_on_file', String(5)),
    Column('cb_person_cred_hist_length', Integer)
)

def init_db():
    metadata.create_all(engine)
    df = pd.read_csv('credit_risk_dataset.csv')
    df.columns = [c.lower().replace(' ', '-') for c in df.columns]
    df.dropna()
    df.to_sql('credit_risk_data', engine, if_exists= 'append', index=False)
    print("Database Initialized and Data Migrated.")

if __name__ == "__main__":
    init_db()