

print("✅ Script is running")

def main():
    print("🚀 Script started...")  # <-- Add this line
    file_path = input("Enter path to the Sage-exported CSV file: ")
    print("📂 Loading data from:", file_path) 
# Import the pandas library so we can work with CSV data and perform data analysis
import pandas as pd

# Define a function to load CSV data
def load_data(file_path):
    """
    Loads a CSV file from the given file path and returns a pandas DataFrame.
    If it fails, it prints an error message and returns None.
    """
    try:
        df = pd.read_csv(file_path)  # read the CSV into a DataFrame
        print("✅ Data loaded successfully.")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

# Define a function to clean the data
def clean_data(df):
    """
    Cleans the DataFrame by:
    - Removing extra spaces and standardizing column names to lowercase with underscores
    - Converting 'date' column to datetime format (if exists)
    - Converting 'amount' column to numeric values (if exists)
    - Dropping any rows where 'amount' is missing
    """
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if 'amount' in df.columns:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    df = df.dropna(subset=['amount'])
    return df

# Define a function to analyze the data
def analyze_data(df):
    """
    Calculates and returns a summary dictionary:
    - Total revenue (sum of positive amounts)
    - Total expenses (sum of negative amounts)
    - Net profit (total revenue + total expenses)
    - Top 5 expense categories (if 'category' column exists)
    """
    summary = {}

    # Calculate total revenue
    summary['total_revenue'] = df[df['amount'] > 0]['amount'].sum()

    # Calculate total expenses
    summary['total_expenses'] = df[df['amount'] < 0]['amount'].sum()

    # Calculate net profit
    summary['net_profit'] = summary['total_revenue'] + summary['total_expenses']

    # Get top 5 expense categories if 'category' exists
    if 'category' in df.columns:
        top_expenses = (
            df[df['amount'] < 0]
            .groupby('category')['amount']
            .sum()
            .sort_values()
            .head(5)
        )
        summary['top_expense_categories'] = top_expenses.to_dict()
    else:
        summary['top_expense_categories'] = {}

    return summary

# Define a function to export the summary to a text file
def export_summary(summary, file_path='financial_summary.txt'):
    """
    Writes the summary dictionary to a text file.
    """
    with open(file_path, 'w') as f:
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")
    print("📄 Summary exported to", file_path)

# Define the main function that will run when you execute the script
def main():
    # Ask the user for the CSV file path
    file_path = input("Enter path to the Sage-exported CSV file: ")
    df = load_data(file_path)

    if df is not None:
        # Clean the data
        df_clean = clean_data(df)

        # Analyze the data
        summary = analyze_data(df_clean)

        # Print the summary to the console
        print("\n📊 Financial Summary:")
        for k, v in summary.items():
            print(f"{k}: {v}")

        # Export summary and cleaned data
        export_summary(summary)
        df_clean.to_csv("cleaned_data.csv", index=False)
        print("📁 Cleaned data exported to cleaned_data.csv")

# Run the main function if this script is run directly
if __name__ == "__main__":
    main()
