import pandas as pd
from datetime import timedelta 

# Load the CSV file into a DataFrame
try:
    df = pd.read_csv('Assignment_Timecard.xlsx - Sheet1.csv')
except FileNotFoundError:
    print("Error: File not found.")
    exit()

# Function to check if an employee has worked for 7 consecutive days
def consecutive_days(employee_data):
    dates = pd.to_datetime(employee_data['Time']).dt.date.unique()
    return any((dates[i + 6] - dates[i]).days == 6 for i in range(len(dates) - 6))

# Function to check if an employee has less than 10 hours but more than 1 hour between shifts
def time_between_shifts(employee_data):
    time_diffs = pd.to_datetime(employee_data['Time']).diff().dropna()
    return any(timedelta(hours=1) < diff < timedelta(hours=10) for diff in time_diffs)

# Filter data and extract unique employee names
consecutive_employee_names = df.groupby('Employee Name').filter(consecutive_days)['Employee Name'].unique()
time_between_shifts_employee_names = df.groupby('Employee Name').filter(time_between_shifts)['Employee Name'].unique()
long_shift_employee_names = df[pd.to_timedelta(df['Timecard Hours (as Time)'].str.replace(':', ' hours ') + ' minutes') > timedelta(hours=14)]['Employee Name'].unique()

# Write the output to a text file
with open('output.txt', 'w') as f:
    f.write(f"Employees who have worked for 7 consecutive days:\n{', '.join(consecutive_employee_names)}\n\n")
    f.write(f"Employees who have less than 10 hours between shifts but greater than 1 hour:\n{', '.join(time_between_shifts_employee_names)}\n\n")
    f.write(f"Employees who have worked for more than 14 hours in a single shift:\n{', '.join(long_shift_employee_names)}\n")
