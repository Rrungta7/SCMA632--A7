import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date

# Sample data
income_data = {
    'Date': ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15'],
    'Source': ['Salary', 'Freelance', 'Salary', 'Freelance'],
    'Category': ['Primary', 'Secondary', 'Primary', 'Secondary'],
    'Amount': [2000, 500, 2000, 700]
}

expense_data = {
    'Date': ['2023-01-02', '2023-01-03', '2023-01-10', '2023-01-15', '2023-01-20', 
             '2023-02-02', '2023-02-05', '2023-02-10'],
    'Category': ['Food', 'Transport', 'Rent', 'Entertainment', 'Bills', 
                 'Food', 'Transport', 'Bills'],
    'Subcategory': ['Groceries', 'Bus', 'Monthly Rent', 'Movies', 'Electricity',
                    'Groceries', 'Taxi', 'Internet'],
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

# Set the title and introduction
st.title('Personal Finance Tracker')
st.subheader('Track your income, expenses, and savings with ease!')

# Sidebar for navigation or input controls
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Home', 'Income', 'Expenses', 'Savings'])

# Main content area based on selected page
if page == 'Home':
    st.write('Welcome to your personal finance tracker!')
    st.write('Use the sidebar to navigate through different sections.')

    # Display summary statistics
    total_income = income_df['Amount'].sum()
    total_expense = expense_df['Amount'].sum()
    net_savings = total_income - total_expense
    avg_monthly_income = income_df.groupby(income_df['Date'].str[:7])['Amount'].sum().mean()
    avg_monthly_expense = expense_df.groupby(expense_df['Date'].str[:7])['Amount'].sum().mean()

    st.write(f"**Total Income:** ${total_income:.2f}")
    st.write(f"**Total Expenses:** ${total_expense:.2f}")
    st.write(f"**Net Savings:** ${net_savings:.2f}")
    st.write(f"**Average Monthly Income:** ${avg_monthly_income:.2f}")
    st.write(f"**Average Monthly Expenses:** ${avg_monthly_expense:.2f}")

    # Monthly summary chart
    income_df['Month'] = pd.to_datetime(income_df['Date']).dt.to_period('M')
    expense_df['Month'] = pd.to_datetime(expense_df['Date']).dt.to_period('M')

    monthly_summary = pd.DataFrame({
        'Income': income_df.groupby('Month')['Amount'].sum(),
        'Expenses': expense_df.groupby('Month')['Amount'].sum()
    }).reset_index()

    monthly_summary['Month'] = monthly_summary['Month'].astype(str)  # Convert Period to string

    st.write("### Monthly Summary")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=monthly_summary, x='Month', y='Income', marker='o', label='Income')
    sns.lineplot(data=monthly_summary, x='Month', y='Expenses', marker='o', label='Expenses')
    plt.title("Monthly Income vs. Expenses")
    plt.xticks(rotation=45)
    st.pyplot(plt)

elif page == 'Income':
    st.subheader('Income Tracker')

    # Show income data
    st.write("Income Data:")
    st.write(income_df)

    # Input fields to add new income
    st.write("Add New Income:")
    income_date = st.date_input("Date", date.today())
    income_source = st.text_input("Source")
    income_category = st.selectbox("Category", ['Primary', 'Secondary', 'Other'])
    income_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    if st.button("Add Income"):
        new_income = pd.DataFrame({
            'Date': [income_date],
            'Source': [income_source],
            'Category': [income_category],
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
    expense_category = st.selectbox("Category", ['Food', 'Transport', 'Rent', 'Entertainment', 'Bills', 'Other'])
    expense_subcategory = st.text_input("Subcategory")
    expense_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    if st.button("Add Expense"):
        new_expense = pd.DataFrame({
            'Date': [expense_date],
            'Category': [expense_category],
            'Subcategory': [expense_subcategory],
            'Amount': [expense_amount]
        })
        expense_df = pd.concat([expense_df, new_expense], ignore_index=True)
        st.write("Updated Expense Data:")
        st.write(expense_df)

    # Visualize expenses by category
    st.write("### Expenses by Category")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=expense_df, x='Category', y='Amount', estimator=sum, ci=None)
    plt.title("Total Expenses by Category")
    st.pyplot(plt)

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
    st.write("### Total Savings Over Time")
    total_savings = savings_df['Amount'].sum()
    st.write(f"**Total Savings:** ${total_savings:.2f}")

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=savings_df, x='Date', y='Amount', marker='o')
    plt.title("Savings Over Time")
    st.pyplot(plt)

    # Savings goal
    st.write("### Savings Goal")
    savings_goal = st.number_input("Set your savings goal", min_value=0.0, format="%.2f")
    progress = (total_savings / savings_goal) * 100 if savings_goal > 0 else 0
    st.write(f"Progress towards goal: {progress:.2f}%")
    st.progress(progress / 100)
