import pandas as pd
import random
from datetime import date
from jugaad_data.nse import stock_df, bhavcopy_save
import os

bhavcopy_save(date(2020,1,1), "./")

start_date = date(2020,1,1)
end_date = date(2023,1,1)
series = "EQ"
number_of_samples = 150
folder_path = 'data'

bhavcopy_df = pd.read_csv('cm01Jan2020bhav.csv')

stocks = bhavcopy_df.iloc[:,0].to_list()

for i in range(number_of_samples):
    while True:
        current = random.choice(stocks)
        file_name = current + '.csv'
        file_path = os.path.join(folder_path, file_name)

        if not os.path.exists(file_path):
            try:
                data = stock_df(symbol=current, from_date=start_date,
                        to_date=end_date, series=series)  # Adjust the start and end dates as needed
                data.to_csv('data/' + current + '.csv', index=False)
                print(f'Data saved for {current}')
                break
            except Exception as e:
                print(f"Error fetching data for {current}: {e}")
                continue

csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Initialize a list to store correlation values and file names
correlation_values = []

# Loop through each pair of CSV files and calculate correlation
for i in range(int(len(csv_files))):
    for j in range(i + 1, int(len(csv_files))):
        # Read CSV files and calculate logarithmic differences
        file1 = pd.read_csv(os.path.join(folder_path, csv_files[i]))
        file2 = pd.read_csv(os.path.join(folder_path, csv_files[j]))

        file1['Log Difference'] = np.log(file1['CLOSE']) - np.log(file1['PREV. CLOSE'])
        file2['Log Difference'] = np.log(file2['CLOSE']) - np.log(file2['PREV. CLOSE'])

        # Compute correlation between logarithmic differences
        correlation = file1['Log Difference'].corr(file2['Log Difference'])

        # Remove '.csv' extension from file names and append to the list
        file1_name = os.path.splitext(csv_files[i])[0]
        file2_name = os.path.splitext(csv_files[j])[0]
        correlation_values.append({'File1': file1_name, 'File2': file2_name, 'Correlation': correlation})

# Create a DataFrame from the correlation values list
correlation_df = pd.DataFrame(correlation_values)
correlation_df.to_csv('corr_closing_price.csv')
