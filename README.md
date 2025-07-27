# 📈 Smart Expense Analyzer

A multi-page Streamlit application for personal finance management. This tool provides in-depth analysis of spending habits by processing expense data from a CSV file, helping users track their financial health and achieve savings goals.

---

## ✨ Features

-   **Multi-Page Interface**: A structured application with separate pages for onboarding, navigation, and detailed analysis.
-   **Comprehensive Analytics**: Delivers insights on total spending, category-wise breakdowns, and temporal trends (monthly and weekly).
-   **Savings Goal Management**: Allows users to set monthly income and savings goals, providing feedback and suggestions.
-   **Data-Driven Suggestions**: Identifies top spending categories to suggest areas for potential budget cuts.
-   **Backend Logic Separation**: Core data processing and analysis functions are modularized in a separate backend script.
-   **Predictive Analytics (Core Logic)**: The backend includes functions for training a linear regression model to predict future spending, which can be integrated into the UI.

---

## 🛠️ Tech Stack

-   **Language**: Python
-   **Frontend**: Streamlit
-   **Data Science**: pandas, scikit-learn
-   **Data Visualization**: matplotlib, seaborn

---

## 📂 File Structure

The application is organized into a multi-page structure, separating the core logic from the user interface.

-   `logic.py`: **(Backend)** Contains all data processing, financial calculations, and machine learning functions. It does not interact with the Streamlit frontend directly.
-   `main_1.py`: **(Frontend - Entrypoint)** The main script that serves as the landing page. It handles file uploads and user input for income and savings goals. It is recommended to rename this file to `app.py`.
-   `pages/dashboard.py`: **(Frontend - Navigation)** Acts as a central hub, presenting analysis options to the user and navigating them to the appropriate view.
-   `pages/analysis.py`: **(Frontend - Display)** A dynamic page that renders different charts and data tables based on the user's selection in the dashboard.

---

## 🚀 Setup

### ### 1. Prerequisites

-   Python 3.8+

### ### 2. Folder Structure

For the multi-page functionality to work correctly, your files must be organized in the following structure. Note that `dashboard.py` and `analysis.py` must be inside a `pages` directory.

### ### 3. Installation

1.  Create a file named `requirements.txt` in the root of your project directory with the following content:
    ```txt
    streamlit
    pandas
    scikit-learn
    matplotlib
    seaborn
    ```

2.  Open a terminal and install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## ▶️ Usage

1.  Ensure your project files are arranged according to the structure described in the **Setup** section.

2.  Run the application from your terminal:
    ```bash
    streamlit run app.py
    ```

3.  The application will open in your browser. Start by uploading your expense CSV file and entering your financial details on the homepage.

4.  Click "Continue to Dashboard" to access the main navigation panel and explore your expense data.
