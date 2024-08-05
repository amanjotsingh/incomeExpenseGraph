from datetime import datetime
import pandas as pd 
import csv
from dataentry import get_date,get_amount,get_catgory,get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "pnl.csv"
    COLUMNS = ["date","amount","category","description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):

        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE,index=False)
    
    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry={
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_FILE,'a', newline="") as csvfile:
            writer =  csv.DictWriter(csvfile,fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
            print("Row added successfully")
            print(f"data Added{new_entry}")
            
    @classmethod
    def get_transaction(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] =  pd.to_datetime(df["date"],format=cls.FORMAT )
        start_date = datetime.strptime(start_date,cls.FORMAT)
        end_date = datetime.strptime(end_date,cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        print(mask)
        filtered_df = df.loc[mask]
        print(filtered_df)

        if filtered_df.empty:
            print("No Transactions found for the selected date")
        else:
            print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}")

            print(filtered_df.to_string(index=False, formatters={"date": lambda x : x.strftime(cls.FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()

            print("\n Summary: ")
            print (f"Total Income ${total_income:.2f}")
            print (f"Total expense ${total_expense:.2f}")
            print(f"net Savings ${(total_income-total_expense):.2f}")

            return filtered_df

def plot_transactions(df):
    df.set_index("date", inplace=True)

    income_df = (
        df[df["category"]=="Income"].resample("D").sum().reindex(df.index,fill_value=0)
    )
    expense_df = (
        df[df["category"]=="Expense"].resample("D").sum().reindex(df.index,fill_value=0)
    )
    plt.figure(figsize=(10,5))
    plt.plot (income_df.index, income_df["amount"],label="Income",color="g")
    plt.plot(expense_df.index, expense_df["amount"],label="Expense",color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.legend()
    plt.title("Income/ Expense Graph")
    plt.grid(True)
    plt.show()


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction or enter the todays date in dd-mm-yyyy format.", allow_default=True)
    amount = get_amount()
    category = get_catgory()
    description = get_description()

    CSV.add_entry(date,amount,category,description)

def main():
    while True:
        print("\n1. Add new Transaction")
        print("\n2. View transaction summary for a given time period")
        print("\n3. Exit ")
        choice = input("\nEnter your choice: ")

        if choice =="1":
            add()
        elif choice =="2":
            start_date = input("Enter the start date in dd-mm-yyyy format: ")
            end_date = input("Enter the end date in dd-mm-yyyy format: ")

            df = CSV.get_transaction(start_date,end_date)
            if input("Do you want to plot the graph y/n?").lower() == "y" :
                plot_transactions(df)
        elif choice =="3":
            print ("Exiting ....")
            break
        else:
            print(f"\nyou have entered: {choice}")
            print("Invalid Entry. Please enter 1,2 or 3")
        
if __name__ == "__main__":
    main()