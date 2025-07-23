import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

def load_data(filepath):
    df = pd.read_csv(filepath)
    df.dropna(subset=['Date', 'Amount', 'Category'], inplace=True)
    df = df[df['Amount'] > 0]
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df.dropna(subset=['Amount'], inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df.dropna(subset=['Date'], inplace=True)
    df['Category'] = df['Category'].str.capitalize().str.strip()
    df['Description'] = df['Description'].fillna('No description')
    return df

def total_spending(df):
    return df['Amount'].sum()

def spending_by_category(df):
    return df.groupby('Category')['Amount'].sum().sort_values(ascending=False)

def monthly_trend(df):
    df['Month'] = df['Date'].dt.to_period('M')
    return df.groupby('Month')['Amount'].sum()

def weekly_pattern(df):
    df['DayOfWeek'] = df['Date'].dt.day_name()
    return df.groupby('DayOfWeek')['Amount'].mean().sort_values()

def top_expenses(df, n=5):
    return df.sort_values(by='Amount', ascending=False).head(n)

def detect_anomalies(df):
    mean = df['Amount'].mean()
    std = df['Amount'].std()
    threshold = mean + 2 * std
    return df[df['Amount'] > threshold]

def category_summary(df):
    return df.groupby('Category').agg(
        Total_Spend=('Amount', 'sum'),
        Average_Spend=('Amount', 'mean'),
        Transaction_Count=('Amount', 'count')
    ).sort_values(by='Total_Spend', ascending=False)

def savings_goal_nudge(df, income, goal):
    total = total_spending(df)
    allowed = income - goal
    if total <= allowed:
        return "You're on track with your saving goal!"
    else:
        gap = total - allowed
        suggestions = spending_by_category(df).head(3) * 0.2
        return {
            "message": f"You need to reduce ₹{gap:.2f} to meet your goal.",
            "suggest_cuts": suggestions
        }

def generate_monthly_regression_data(df):
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    grouped = df.groupby(['Month', 'Category']).agg(
        Total_Spend=('Amount', 'sum'),
        Transaction_Count=('Amount', 'count'),
        Avg_Spend=('Amount', 'mean')
    ).reset_index()
    return grouped

def train_regression_model(data, category_name):
    cat_data = data[data['Category'] == category_name].copy()
    cat_data['Month_Num'] = pd.to_datetime(cat_data['Month']).dt.month
    X = cat_data[['Month_Num', 'Transaction_Count', 'Avg_Spend']]
    y = cat_data['Total_Spend']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return model, mse

def predict_next_month_spending(model, month_num, transaction_count, avg_spend):
    return model.predict([[month_num, transaction_count, avg_spend]])[0]
