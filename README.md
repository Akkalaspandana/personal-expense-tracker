# 💰 Personal Expense Tracker

A comprehensive, user-friendly expense tracking application built with Streamlit that helps you monitor and analyze your personal finances.

## 🚀 Features

### 📊 Dashboard
- **Real-time Metrics**: Total expenses, average spending, and expense count
- **Interactive Charts**: Category breakdown pie chart and daily expense trends
- **Date Range Filtering**: Customizable date ranges for analysis
- **Recent Expenses Table**: Quick overview of latest transactions

### ➕ Expense Management
- **Easy Data Entry**: Simple form to add new expenses
- **Categorized Spending**: Pre-defined categories (Food, Transportation, Shopping, etc.)
- **Payment Method Tracking**: Record how you paid (Cash, Credit Card, etc.)
- **Description Field**: Add detailed notes for each expense

### 📋 View & Manage Expenses
- **Advanced Filtering**: Filter by category and payment method
- **Multiple Sort Options**: Sort by date, amount, or other criteria
- **Delete Functionality**: Remove unwanted expenses
- **Responsive Table**: Clean, organized view of all expenses

### 📈 Analytics & Insights
- **Time Period Analysis**: Last 30 days, 3 months, 6 months, or custom ranges
- **Category Analysis**: Detailed breakdown of spending by category
- **Payment Pattern Analysis**: Understanding your payment preferences
- **Spending Patterns**: Day of week and time-based analysis
- **Trend Visualization**: Monthly expense trends and patterns

### ⚙️ Data Management
- **CSV Export**: Download your expense data for external analysis
- **Data Backup**: Secure storage in SQLite database
- **Data Clearing**: Option to reset all data if needed

## 🛠️ Technical Skills Demonstrated

### Backend Development
- **SQLite Database**: Efficient data storage and retrieval
- **SQL Queries**: Complex filtering and aggregation operations
- **Data Processing**: Pandas for data manipulation and analysis
- **Object-Oriented Programming**: Clean, maintainable code structure

### Frontend Development
- **Streamlit Framework**: Modern web application development
- **Interactive UI**: Responsive design with user-friendly interface
- **Data Visualization**: Plotly charts for engaging data presentation
- **Custom CSS**: Professional styling and layout

### Data Analysis
- **Statistical Analysis**: Mean, sum, count, and trend calculations
- **Data Aggregation**: Grouping and summarizing expense data
- **Time Series Analysis**: Date-based filtering and trend analysis
- **Category Analysis**: Spending pattern identification

### Real-World Application Features
- **CRUD Operations**: Create, Read, Update, Delete expense records
- **Data Validation**: Input validation and error handling
- **User Experience**: Intuitive navigation and feedback
- **Data Export**: CSV export functionality for external use

## 📦 Installation

1. **Clone or download the project files**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

## 🎯 Usage Guide

### Getting Started
1. **Add Your First Expense**: Go to "Add Expense" and fill out the form
2. **Explore the Dashboard**: View your spending overview and trends
3. **Analyze Your Data**: Use the Analytics page for deeper insights
4. **Manage Your Expenses**: View and edit existing expenses as needed

### Best Practices
- **Regular Updates**: Add expenses daily or weekly for accurate tracking
- **Use Categories**: Properly categorize expenses for better analysis
- **Add Descriptions**: Include details to remember what each expense was for
- **Review Regularly**: Check your dashboard and analytics monthly

## 🏗️ Project Structure

```
music/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
├── expenses.db        # SQLite database (created automatically)
└── venv/              # Virtual environment
```

## 🔧 Customization

### Adding New Categories
Edit the category list in the `show_add_expense()` function:
```python
category = st.selectbox(
    "Category",
    ["Food & Dining", "Transportation", "Shopping", "Entertainment", 
     "Healthcare", "Utilities", "Housing", "Education", "Travel", "Other"]
)
```

### Modifying Charts
The application uses Plotly for visualizations. You can customize colors, layouts, and chart types in the respective functions.

### Database Schema
The SQLite database has a simple structure:
- `id`: Unique identifier
- `date`: Expense date
- `category`: Expense category
- `description`: Expense description
- `amount`: Expense amount
- `payment_method`: How the expense was paid
- `created_at`: Timestamp of record creation

## 🚀 Deployment

### Local Development
- Perfect for personal use
- Data stored locally in SQLite database
- No internet connection required

### Cloud Deployment
The application can be deployed to:
- **Streamlit Cloud**: Free hosting for Streamlit apps
- **Heroku**: Cloud platform deployment
- **AWS/GCP**: Enterprise cloud hosting

## 📊 Sample Data

To test the application, you can add sample expenses:
- **Food & Dining**: $25.50 - "Lunch at Chipotle"
- **Transportation**: $45.00 - "Uber ride to airport"
- **Shopping**: $89.99 - "New headphones"
- **Entertainment**: $15.00 - "Movie ticket"

## 🤝 Contributing

This project demonstrates real-world development skills and can be extended with:
- Budget setting and tracking
- Income tracking
- Bill reminders
- Financial goals
- Multi-currency support
- Receipt image upload
- Email notifications

## 📝 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Streamlit, Pandas, and Plotly** 