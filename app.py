import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="AI Expense Manager", layout="wide")

st.title("💸 Autonomous AI Expense Management Agent")
st.write("Upload your bank statement CSV to analyze your expenses.")

# Sidebar
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key


# Upload CSV
uploaded_file = st.file_uploader("Upload Bank Statement CSV", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Clean column names
    df.columns = df.columns.str.strip().str.title()

    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    # -----------------------------
    # Automatic Column Detection
    # -----------------------------

    # Description column
    if "Description" not in df.columns:

        text_cols = df.select_dtypes(include="object").columns

        if len(text_cols) > 0:
            df["Description"] = df[text_cols[0]]
        else:
            df["Description"] = "Transaction"

    # Amount column
    if "Amount" not in df.columns:

        num_cols = df.select_dtypes(include=["int64", "float64"]).columns

        if len(num_cols) > 0:
            df["Amount"] = df[num_cols[0]]
        else:
            df["Amount"] = 0


    # -----------------------------
    # Categorization Logic
    # -----------------------------

    def categorize(desc):

        desc = str(desc).lower()

        if any(x in desc for x in ["swiggy","zomato","restaurant","food", "dining", "domino", "mcdonald"]):
            return "Food & Dining"

        elif any(x in desc for x in ["uber","ola","taxi","fuel", "petrol", "transport", "irctc", "metro"]):
            return "Transport"

        elif any(x in desc for x in ["amazon","flipkart","shopping", "myntra", "dmart", "reliance", "bigbasket"]):
            return "Shopping & Groceries"

        elif any(x in desc for x in ["netflix","spotify","prime", "hotstar", "autopay"]):
            return "Subscription"
            
        elif any(x in desc for x in ["mf", "mutual", "sip", "zerodha", "groww", "investment"]):
            return "Investments"
            
        elif any(x in desc for x in ["upi", "neft", "rtgs", "transfer", "cash", "atm"]):
            return "Transfers & Cash"

        elif any(x in desc for x in ["salary","credit", "income"]):
            return "Income"
            
        # Demo specific granular categories to visualize bank marketing dataset
        elif any(x in desc for x in ["management", "entrepreneur", "self-employed"]):
            return "Business"
            
        elif any(x in desc for x in ["admin", "clerk", "hr", "secretary"]):
            return "Officework"
            
        elif any(x in desc for x in ["blue-collar", "technician", "mechanic"]):
            return "Labour"
            
        elif any(x in desc for x in ["services", "housemaid", "cleaning", "retail"]):
            return "Services"
            
        elif any(x in desc for x in ["student", "unemployed", "retired"]):
            return "Unemployed/Student"

        else:
            return "Other"


    df["Category"] = df["Description"].apply(categorize)


    # -----------------------------
    # Dashboard
    # -----------------------------

    st.subheader("Categorized Transactions")
    st.dataframe(df.head(10))


    col1, col2 = st.columns(2)

    with col1:

        category_sum = df.groupby("Category")["Amount"].sum().reset_index()

        fig = px.pie(
            category_sum,
            values="Amount",
            names="Category",
            title="Expense Breakdown",
            hole=0.4
        )

        st.plotly_chart(fig, use_container_width=True)


    with col2:

        fig2 = px.bar(
            category_sum,
            x="Category",
            y="Amount",
            title="Category Spending"
        )

        st.plotly_chart(fig2, use_container_width=True)


    # -----------------------------
    # AI Insights
    # -----------------------------

    st.subheader("📊 AI Financial Insights")

    total_spend = df["Amount"].sum()

    st.metric("Total Spending", f"₹{total_spend:,.2f}")


    top_category = category_sum.sort_values(
        by="Amount",
        ascending=False
    ).iloc[0]["Category"]

    st.info(f"💡 Most of your spending is on **{top_category}**.")


    # Duplicate transaction detection has been removed per user request.