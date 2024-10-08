import time
import datetime as dt

import yfinance as yf 

short_window = 20 
long_window = 50

initial_balance = 10000 # USD
balance = initial_balance
position = 0 # EUR

forex_pair = 'EURUSD=X'

try:
    while True:
        data = yf.download(forex_pair, period='1d', interval='1m', progress=False)

        data['SMA_Short'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
        data['SMA_Long'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

        latest_entry = data.iloc[-1]
        if latest_entry['SMA_Short'] > latest_entry['SMA_Long'] and position == 0:
            units_to_buy = balance // latest_entry['Close']
            balance -= units_to_buy * latest_entry['Close']
            position += units_to_buy
            print(f'{dt.datetime.now()}: Bought{units_to_buy} EUR for {latest_entry["Close"]:.2f} USD per unit')
        elif latest_entry['SMA_Short'] < latest_entry['SMA_Long'] and position > 1:
            balance += position * latest_entry['Close']
            print(f'{dt.datetime.now()}: Sold {position} EUR for {latest_entry["Close"]:.2f} USD per unit')
            position = 0
        else:
            print(f'{dt.datetime.now()}: No trading action EUR at {latest_entry["Close"]:.2f} USD per unit)')    

        time.sleep(60)    
except KeyboardInterrupt:
    print("Interrupted by user")

final_balance = balance + position * latest_entry['Close']
print(f'Final balance: ${final_balance}')

if final_balance > initial_balance:
    print(f'final balance was increased by {(final_balance / initial_balance -1)* 100:.2f}%')
elif final_balance > initial_balance:
    print(f'balance was decreased by {(1 - final_balance / initial_balance )* 100:.2f}%')    
else:
    print('No significant change in balance')
