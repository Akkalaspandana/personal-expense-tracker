import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
from datetime import datetime, timedelta
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .expense-form {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

class ExpenseTracker:
    def __init__(self):
        self.db_path = "expenses.db"
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with expenses table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                amount REAL NOT NULL,
                payment_method TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_expense(self, date, category, description, amount, payment_method):
        """Add a new expense to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (date, category, description, amount, payment_method)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, category, description, amount, payment_method))
        
        conn.commit()
        conn.close()
    
    def get_expenses(self, start_date=None, end_date=None):
        """Retrieve expenses from database with optional date filtering"""
        conn = sqlite3.connect(self.db_path)
        
        if start_date and end_date:
            query = '''
                SELECT * FROM expenses 
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC
            '''
            df = pd.read_sql_query(query, conn, params=[start_date, end_date])
        else:
            df = pd.read_sql_query('SELECT * FROM expenses ORDER BY date DESC', conn)
        
        conn.close()
        return df
    
    def delete_expense(self, expense_id):
        """Delete an expense by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
        
        conn.commit()
        conn.close()

def main():
    # Initialize expense tracker
    tracker = ExpenseTracker()
    
    # Header
    st.markdown('<h1 class="main-header">💰 Personal Expense Tracker</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["📊 Dashboard", "➕ Add Expense", "📋 View Expenses", "📈 Analytics", "⚙️ Settings"]
    )
    
    if page == "📊 Dashboard":
        show_dashboard(tracker)
    elif page == "➕ Add Expense":
        show_add_expense(tracker)
    elif page == "📋 View Expenses":
        show_view_expenses(tracker)
    elif page == "📈 Analytics":
        show_analytics(tracker)
    elif page == "⚙️ Settings":
        show_settings(tracker)

def show_dashboard(tracker):
    """Display the main dashboard with key metrics and charts"""
    st.header("📊 Dashboard")
    
    # Date range selector
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now().replace(day=1))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    with col3:
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Get expenses for the selected date range
    expenses_df = tracker.get_expenses(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
    
    if expenses_df.empty:
        st.warning("No expenses found for the selected date range.")
        return
    
    # Key metrics
    total_expenses = expenses_df['amount'].sum()
    avg_expense = expenses_df['amount'].mean()
    num_expenses = len(expenses_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Expenses", f"₹{total_expenses:,.2f}")
    with col2:
        st.metric("Average Expense", f"₹{avg_expense:,.2f}")
    with col3:
        st.metric("Number of Expenses", num_expenses)
    with col4:
        st.metric("Date Range", f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Category breakdown pie chart
        category_totals = expenses_df.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        fig_pie = px.pie(
            values=category_totals.values,
            names=category_totals.index,
            title="Expenses by Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Daily expenses line chart
        daily_expenses = expenses_df.groupby('date')['amount'].sum().reset_index()
        daily_expenses['date'] = pd.to_datetime(daily_expenses['date'])
        
        fig_line = px.line(
            daily_expenses,
            x='date',
            y='amount',
            title="Daily Expenses Trend",
            labels={'amount': 'Amount (₹)', 'date': 'Date'}
        )
        fig_line.update_layout(xaxis_title="Date", yaxis_title="Amount (₹)")
        st.plotly_chart(fig_line, use_container_width=True)
    
    # Recent expenses table
    st.subheader("Recent Expenses")
    recent_expenses = expenses_df.head(10)[['date', 'category', 'description', 'amount', 'payment_method']]
    st.dataframe(recent_expenses, use_container_width=True)

def show_add_expense(tracker):
    """Form to add new expenses"""
    st.header("➕ Add New Expense")
    
    with st.container():
        st.markdown('<div class="expense-form">', unsafe_allow_html=True)
        
        # Form inputs
        col1, col2 = st.columns(2)
        
        with col1:
            date = st.date_input("Date", value=datetime.now())
            category = st.selectbox(
                "Category",
                ["Food & Dining", "Transportation", "Shopping", "Entertainment", 
                 "Healthcare", "Utilities", "Housing", "Education", "Travel", "Mobile & Internet", "Other"]
            )
            amount = st.number_input("Amount (₹)", min_value=0.01, value=0.01, step=0.01)
        
        with col2:
            description = st.text_input("Description", placeholder="Enter expense description")
            payment_method = st.selectbox(
                "Payment Method",
                ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "Digital Wallet", "Other"]
            )
        
        # Submit button
        if st.button("💾 Save Expense", type="primary"):
            if description.strip():
                tracker.add_expense(
                    date.strftime('%Y-%m-%d'),
                    category,
                    description,
                    amount,
                    payment_method
                )
                st.success("✅ Expense added successfully!")
                st.balloons()
            else:
                st.error("Please enter a description for the expense.")

def show_view_expenses(tracker):
    """View and manage existing expenses"""
    st.header("📋 View & Manage Expenses")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All Categories"] + ["Food & Dining", "Transportation", "Shopping", "Entertainment", 
                                "Healthcare", "Utilities", "Housing", "Education", "Travel", "Mobile & Internet", "Other"]
        )
    
    with col2:
        payment_filter = st.selectbox(
            "Filter by Payment Method",
            ["All Methods"] + ["Cash", "Credit Card", "Debit Card", "Bank Transfer", "Digital Wallet", "Other"]
        )
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Amount (High to Low)", "Amount (Low to High)"])
    
    # Get all expenses
    expenses_df = tracker.get_expenses()
    
    if expenses_df.empty:
        st.info("No expenses found. Add some expenses to get started!")
        return
    
    # Apply filters
    if category_filter != "All Categories":
        expenses_df = expenses_df[expenses_df['category'] == category_filter]
    
    if payment_filter != "All Methods":
        expenses_df = expenses_df[expenses_df['payment_method'] == payment_filter]
    
    # Apply sorting
    if sort_by == "Date (Newest)":
        expenses_df = expenses_df.sort_values('date', ascending=False)
    elif sort_by == "Date (Oldest)":
        expenses_df = expenses_df.sort_values('date', ascending=True)
    elif sort_by == "Amount (High to Low)":
        expenses_df = expenses_df.sort_values('amount', ascending=False)
    elif sort_by == "Amount (Low to High)":
        expenses_df = expenses_df.sort_values('amount', ascending=True)
    
    # Display expenses
    st.subheader(f"Found {len(expenses_df)} expenses")
    
    # Add delete functionality
    for index, row in expenses_df.iterrows():
        col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 3, 1, 1, 1])
        
        with col1:
            st.write(row['date'])
        with col2:
            st.write(f"**{row['category']}**")
        with col3:
            st.write(row['description'])
        with col4:
            st.write(f"₹{row['amount']:.2f}")
        with col5:
            st.write(row['payment_method'])
        with col6:
            if st.button(f"🗑️", key=f"delete_{row['id']}"):
                tracker.delete_expense(row['id'])
                st.success("Expense deleted!")
                st.rerun()
        
        st.divider()

def show_analytics(tracker):
    """Advanced analytics and insights"""
    st.header("📈 Analytics & Insights")
    
    # Get all expenses
    expenses_df = tracker.get_expenses()
    
    if expenses_df.empty:
        st.info("No expenses found. Add some expenses to see analytics!")
        return
    
    # Convert date column
    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
    
    # Time period selector
    period = st.selectbox("Select Time Period", ["Last 30 Days", "Last 3 Months", "Last 6 Months", "Last Year", "All Time"])
    
    # Filter data based on period
    if period == "Last 30 Days":
        start_date = datetime.now() - timedelta(days=30)
        filtered_df = expenses_df[expenses_df['date'] >= start_date]
    elif period == "Last 3 Months":
        start_date = datetime.now() - timedelta(days=90)
        filtered_df = expenses_df[expenses_df['date'] >= start_date]
    elif period == "Last 6 Months":
        start_date = datetime.now() - timedelta(days=180)
        filtered_df = expenses_df[expenses_df['date'] >= start_date]
    elif period == "Last Year":
        start_date = datetime.now() - timedelta(days=365)
        filtered_df = expenses_df[expenses_df['date'] >= start_date]
    else:
        filtered_df = expenses_df
    
    if filtered_df.empty:
        st.warning(f"No expenses found for {period}")
        return
    
    # Key insights
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = filtered_df['amount'].sum()
        st.metric("Total Expenses", f"₹{total:,.2f}")
    
    with col2:
        avg = filtered_df['amount'].mean()
        st.metric("Average Expense", f"₹{avg:,.2f}")
    
    with col3:
        max_expense = filtered_df['amount'].max()
        st.metric("Highest Expense", f"₹{max_expense:,.2f}")
    
    with col4:
        most_common_category = filtered_df['category'].mode().iloc[0] if not filtered_df['category'].mode().empty else "N/A"
        st.metric("Most Common Category", most_common_category)
    
    # Advanced charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly trend
        monthly_expenses = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['amount'].sum().reset_index()
        monthly_expenses['date'] = monthly_expenses['date'].astype(str)
        
        fig_monthly = px.bar(
            monthly_expenses,
            x='date',
            y='amount',
            title="Monthly Expenses",
            labels={'amount': 'Amount (₹)', 'date': 'Month'}
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    with col2:
        # Payment method distribution
        payment_dist = filtered_df['payment_method'].value_counts()
        
        fig_payment = px.pie(
            values=payment_dist.values,
            names=payment_dist.index,
            title="Payment Method Distribution"
        )
        st.plotly_chart(fig_payment, use_container_width=True)
    
    # Category analysis
    st.subheader("Category Analysis")
    
    category_analysis = filtered_df.groupby('category').agg({
        'amount': ['sum', 'mean', 'count']
    }).round(2)
    category_analysis.columns = ['Total Amount', 'Average Amount', 'Number of Expenses']
    category_analysis = category_analysis.sort_values('Total Amount', ascending=False)
    
    st.dataframe(category_analysis, use_container_width=True)
    
    # Spending patterns
    st.subheader("Spending Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Day of week analysis
        filtered_df['day_of_week'] = filtered_df['date'].dt.day_name()
        day_analysis = filtered_df.groupby('day_of_week')['amount'].sum().reindex([
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ])
        
        fig_day = px.bar(
            x=day_analysis.index,
            y=day_analysis.values,
            title="Expenses by Day of Week",
            labels={'x': 'Day', 'y': 'Amount (₹)'}
        )
        st.plotly_chart(fig_day, use_container_width=True)
    
    with col2:
        # Hour analysis (if time data available)
        if 'created_at' in filtered_df.columns:
            filtered_df['hour'] = pd.to_datetime(filtered_df['created_at']).dt.hour
            hour_analysis = filtered_df.groupby('hour')['amount'].sum()
            
            fig_hour = px.line(
                x=hour_analysis.index,
                y=hour_analysis.values,
                title="Expenses by Hour of Day",
                labels={'x': 'Hour', 'y': 'Amount (₹)'}
            )
            st.plotly_chart(fig_hour, use_container_width=True)

def show_settings(tracker):
    """Settings and data management"""
    st.header("⚙️ Settings")
    
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export Data to CSV"):
            expenses_df = tracker.get_expenses()
            if not expenses_df.empty:
                csv = expenses_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data to export")
    
    with col2:
        if st.button("🗑️ Clear All Data"):
            if st.checkbox("I understand this will permanently delete all expense data"):
                conn = sqlite3.connect(tracker.db_path)
                cursor = conn.cursor()
                cursor.execute('DELETE FROM expenses')
                conn.commit()
                conn.close()
                st.success("All data cleared successfully!")
    
    st.subheader("App Information")
    st.info("""
    **Personal Expense Tracker v1.0**
    
    Features:
    - 📊 Dashboard with key metrics
    - ➕ Add and manage expenses
    - 📋 View and filter expenses
    - 📈 Advanced analytics and insights
    - 💾 Data export functionality
    
    Built with Streamlit, Pandas, and Plotly
    """)

if __name__ == "__main__":
    main() 