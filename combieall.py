import subprocess
import os
import pandas as pd
from backtesting import Backtest, Strategy
import random as rn

question_ask = input("You wanna download data(yes) or you wanna continue with old one(no)?: ")
if question_ask == 'yes':
    def run_dukascopy(instrument, date_from, date_to, timeframe, format, output_dir, date_format, file_name):
        # Command to run npx dukascopy-node
        command = [
            'npx', 'dukascopy-node',
            '-i', instrument,
            '--date-from', date_from,
            '--date-to', date_to,
            '-t', timeframe,
            '-f', format,
            '-dir', output_dir,
            '--date-format', date_format,
            '-fn', file_name,
            '-v'
        ]
        
        #Run the command and manage the exit
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            print("Comanda a fost executată cu succes:")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Eroare la executarea comenzii:")
            print(e.stderr)

    # Set the parametrs
    instrument = input('enter the instrument name (ex:eurusd): ')
    date_from = input('enter the from date (ex: YYYY-MM-DD): ')
    date_to = input('enter the to date (ex: YYYY-MM-DD): ')
    timeframe = input('enter the timeframe (ex: h1): ')
    format = 'csv'
    output_dir = os.path.expanduser('~/Desktop/pyprojects')
    date_format = 'YYYY-MM-DD HH:mm:ss'
    file_name = input('enter the filename: ')

    # Run the command with the specified parametrs
    run_dukascopy(instrument, date_from, date_to, timeframe, format, output_dir, date_format, file_name)

    # Load the CSV file
    file_path = file_name + '.csv'
    df = pd.read_csv(file_path)

    # Rename the 'timestamp' column to 'Date' and other columns
    df.rename(columns={'timestamp': 'Date'}, inplace=True)
    df.rename(columns={'open': 'Open'}, inplace=True)
    df.rename(columns={'high': 'High'}, inplace=True)
    df.rename(columns={'low': 'Low'}, inplace=True)
    df.rename(columns={'close': 'Close'}, inplace=True)
    df.rename(columns={'volume': 'Volume'}, inplace=True)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

    print("Column renamed and file saved successfully.")

    #npx dukascopy-node -i eurusd --date-from 2024-01-02 --date-to 2024-07-01 -t h1 -f csv -dir ~/Desktop/pyprojects --date-format "YYYY-MM-DD HH:mm:ss" -v
else:   
    file_way = input("Enter the way to the csv data: ")
    file_way = file_way + '.csv'


#npx dukascopy-node -i eurusd --date-from 2024-01-02 --date-to 2024-07-01 -t h1 -f csv -dir ~/Desktop/pyprojects --date-format "YYYY-MM-DD HH:mm:ss" -v

class BuySell(Strategy):
    
    def init(self):
        pass

    def next(self):
        price = self.data.Close[-1]
        decision_trade = rn.choice(['buy', "sell"])
        
        if self.position:
            pass
        else:
            if decision_trade == 'buy':
                sl = price - 0.005
                tp = price + 0.005
                self.buy(size=1, sl=sl, tp=tp)
            else:
                sl = price + 0.005
                tp = price - 0.005
                self.sell(size=1, sl=sl, tp=tp)

# Load data
if question_ask == 'yes':
    data_csv_file = file_path
else:
    data_csv_file = file_way
data = pd.read_csv(data_csv_file, parse_dates=True, index_col='Date')

# Initialize and run backtest
bt = Backtest(data, BuySell, cash=10_000)
stats = bt.run()
print(stats)
