import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date

# Title and introduction
st.title('Personal Finance Tracker')
st.subheader('Track your income, expenses, and savings')

# Sidebar for navigation or input controls
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Home', 'Income', 'Expenses', 'Savings'])

# Sample data
income_data = {
    'Date': ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15'],
    'Source': ['Salary', 'Freelance', 'Salary', 'Freelance'],
    'Amount': [2000, 500, 2000, 700]
}

expense_data = {
    'Date': ['2023-01-02', '2023-01-03', '2023-01-10', '2023-01-15', '2023-01-20', 
             '2023-02-02', '2023-02-05', '2023-02-10'],
    'Category': ['Food', 'Transport', 'Rent', 'Entertainment', 'Bills', 
                 'Food', 'Transport', 'Bills'],
    'Amount': [50, 20, 1000, 70, 100, 45, 15, 120]
}

savings_data = {
    'Date': ['2023-01-31', '2023-02-28'],
    'Amount': [500, 700]
}

# Convert sample data to DataFrame
income_df = pd.DataFrame(income_data)
expense_df = pd.DataFrame(expense_data)
savings_df = pd.DataFrame(savings_data)

# Main content area based on selected page
if page == 'Home':
    st.write('Welcome to your personal finance tracker!')
    st.write('Use the sidebar to navigate.')

elif page == 'Income':
    st.subheader('Income Tracker')

    # Show income data
    st.write("Income Data:")
    st.write(income_df)

    # Input fields to add new income
    st.write("Add New Income:")
    income_date = st.date_input("Date", date.today())
    income_source = st.text_input("Source")
    income_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    if st.button("Add Income"):
        new_income = pd.DataFrame({
            'Date': [income_date],
            'Source': [income_source],
            'Amount': [income_amount]
        })
        income_df = pd.concat([income_df, new_income], ignore_index=True)
        st.write("Updated Income Data:")
        st.write(income_df)

elif page == 'Expenses':
    st.subheader('Expenses Tracker')

    # Show expense data
    st.write("Expense Data:")
    st.write(expense_df)

    # Input fields to add new expense
    st.write("Add New Expense:")
    expense_date = st.date_input("Date", date.today())
    expense_category = st.text_input("Category")
    expense_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    if st.button("Add Expense"):
        new_expense = pd.DataFrame({
            'Date': [expense_date],
            'Category': [expense_category],
            'Amount': [expense_amount]
        })
        expense_df = pd.concat([expense_df, new_expense], ignore_index=True)
        st.write("Updated Expense Data:")
        st.write(expense_df)

elif page == 'Savings':
    st.subheader('Savings Tracker')

    # Show savings data
    st.write("Savings Data:")
    st.write(savings_df)

    # Input fields to add new savings
    st.write("Add New Savings:")
    savings_date = st.date_input("Date", date.today())
    savings_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    if st.button("Add Savings"):
        new_savings = pd.DataFrame({
            'Date': [savings_date],
            'Amount': [savings_amount]
        })
        savings_df = pd.concat([savings_df, new_savings], ignore_index=True)
        st.write("Updated Savings Data:")
        st.write(savings_df)

    # Summary and visualization of savings
    st.write("Total Savings Over Time:")
    total_savings = savings_df['Amount'].sum()
    st.write(f"Total Savings: ${total_savings:.2f}")

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=savings_df, x='Date', y='Amount')
    plt.title("Savings Over Time")
    st.pyplot(plt)
