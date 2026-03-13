
# 💸 Autonomous AI Expense Management Agent

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![Pandas](https://img.shields.io/badge/Data-Pandas-green)
![Plotly](https://img.shields.io/badge/Visualization-Plotly-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

An AI-powered expense analysis web application that processes bank statement CSV files, automatically categorizes transactions, and generates financial insights with interactive dashboards.

Built using **Python, Streamlit, Pandas, and Plotly**.

---

## 🚀 Features

- Upload bank statement CSV files  
- Automatic transaction categorization  
- Interactive spending visualization  
- Category-wise expense analysis  
- AI-generated financial insights  
- Clean and responsive dashboard  

---

## 🖥️ Application Preview

### Upload Bank Statement
Upload your bank statement CSV to automatically analyze expenses.

![Upload Interface](images/upload_interface.png)

### Categorized Transactions
Transactions are automatically categorized into categories like:
- Food & Dining
- Shopping & Groceries
- Investments
- Transport
- Subscriptions
- Transfers & Cash

![Categorized Transactions](images/categorized_transactions.png)

### Expense Dashboard

Pie chart and bar chart visualizations show spending distribution across categories.

![Expense Dashboard](images/expense_dashboard.png)

---

## 💡 AI Financial Insights

The system automatically generates financial insights such as:

Total Spending and Highest Spending Category.

Example:

Total Spending: ₹184,971.92  
Most of your spending is on Investments.

---

## 🛠️ Tech Stack

| Technology | Usage |
|------------|------|
| Python | Core programming language |
| Streamlit | Web application framework |
| Pandas | Data processing |
| Plotly | Interactive data visualization |

---

## 📂 Project Structure

AI-Expense-Agent
│
├── app.py
├── requirements.txt
├── sample_data
│   └── balanced_monthly_bank_statement.csv
│
├── images
│   ├── upload_interface.png
│   ├── categorized_transactions.png
│   └── expense_dashboard.png
│
└── README.md

---

## ⚙️ Installation

### Clone the Repository

git clone https://github.com/yourusername/AI-Expense-Agent.git  
cd AI-Expense-Agent

### Install Dependencies

pip install -r requirements.txt

### Run the Application

streamlit run app.py

---

## 📊 Example CSV Format

Date,Description,Amount,Type  
2025-01-01,Netflix/Autopay,649,Debit  
2025-01-01,UPI/Merchant/Flipkart,3227.27,Debit  
2025-01-02,Swiggy/UPI,242.76,Debit  
2025-01-02,SIP/MutualFund/SBI_MF,5000,Debit  

---

## 🔮 Future Improvements

- Machine learning transaction classification  
- Monthly expense prediction  
- Budget alerts and savings recommendations  
- AI financial advisor chatbot  

---

## 👨‍💻 Author

Your Name  
AI & ML Student
