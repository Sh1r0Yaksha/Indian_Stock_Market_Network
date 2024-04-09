import pandas as pd
import numpy as np
# from jugaad_data.nse import stock_df, bhavcopy_save
import os

# bhavcopy_save(date(2020,1,1), "./")

# start_date = date(2020,1,1)
# end_date = date(2023,1,1)
# series = "EQ"
# number_of_samples = 150
folder_path = 'data_clean'


# bhavcopy_df = pd.read_csv('cm01Jan2020bhav.csv')

# stocks = bhavcopy_df.iloc[:,0].to_list()

# for i in range(number_of_samples):
#     while True:
#         current = random.choice(stocks)
#         file_name = current + '.csv'
#         file_path = os.path.join(folder_path, file_name)

#         if not os.path.exists(file_path):
#             try:
#                 data = stock_df(symbol=current, from_date=start_date,
#                         to_date=end_date, series=series)  # Adjust the start and end dates as needed
#                 data.to_csv('data/' + current + '.csv', index=False)
#                 print(f'Data saved for {current}')
#                 break
#             except Exception as e:
#                 print(f"Error fetching data for {current}: {e}")
#                 continue

csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# def calculate_log_difference(folder_path, column_name):
#     log_diff_data = []
#     file_names = []

#     for filename in os.listdir(folder_path):
#         if filename.endswith('.csv'):
#             file_path = os.path.join(folder_path, filename)
#             df = pd.read_csv(file_path)
#             if column_name in df.columns:
#                 log_diff = np.log(df[column_name]) - np.log(df[column_name].shift(1))
#                 log_diff_data.append(log_diff)
#                 file_names.append(os.path.splitext(filename)[0])
#         print(f"Log df of {filename} calculated")

#     log_diff_df = pd.concat(log_diff_data, axis=1)
#     log_diff_df.columns = file_names
#     return log_diff_df

# def calculate_correlation(log_diff_df, output_path):
#     correlation_matrix = log_diff_df.corr()
#     correlation_df = correlation_matrix.unstack().reset_index()
#     correlation_df.columns = ['FILENAME1', 'FILENAME2', 'CORRELATION']
#     correlation_df.to_csv(output_path, index=False)

def calculate_log_difference(folder_path, column_name):
    log_diff_data = []
    file_names = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            # Convert 'CH_TIMESTAMP' to datetime and set as index
            df['CH_TIMESTAMP'] = pd.to_datetime(df['CH_TIMESTAMP'])
            df.set_index('CH_TIMESTAMP', inplace=True)

            if column_name in df.columns:
                log_diff = np.log(df[column_name]) - np.log(df[column_name].shift(1))
                log_diff_data.append(log_diff)
                file_names.append(os.path.splitext(filename)[0])
        print(f"Log df of {filename} calculated")

    log_diff_df = pd.concat(log_diff_data, axis=1)
    log_diff_df.columns = file_names
    return log_diff_df

def calculate_correlation(log_diff_df, output_path):
    correlation_matrix = log_diff_df.corr()
    correlation_df = correlation_matrix.unstack().reset_index()
    correlation_df.columns = ['FILENAME1', 'FILENAME2', 'CORRELATION']
    correlation_df.to_csv(output_path, index=False)



column_names = ['CH_TRADE_HIGH_PRICE', 'CH_TRADE_LOW_PRICE',
                'CH_OPENING_PRICE', 'CH_TOT_TRADED_QTY',
                'CH_CLOSING_PRICE', 'CH_TOT_TRADED_VAL']

for colname in column_names:
    output_path = 'correlation_data/correlation_log_diff_' + colname  +'.csv'
    log_diff_df = calculate_log_difference(folder_path, colname)
    calculate_correlation(log_diff_df, output_path)
