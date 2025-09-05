import finnhub
import time
import numpy as np
from collections import deque

api_key = ""
client = finnhub.Client(api_key=api_key)

symbol = "OPEN"
loop_time = 10
window_size = 10  # last 10 seconds
prices = deque(maxlen=window_size)
my_money = 1000
stocks_held = 0
while True:
    quote = client.quote(symbol)
    price = quote["c"]
    prices.append(price)
    print(price)
    if len(prices) == window_size:
        # # Define weights (more weight to recent prices)
        # weights = np.arange(1, len(prices)+1)

        # # Compute Weighted Moving Average (WMA)
        # wma = np.convolve(prices, weights/weights.sum(), mode='valid')

        # # Calculate slope of the WMA (last value minus first value)
        # m = wma[-1] - wma[0]  # positive if trending up, negative if down
        
        m = prices[-1] - prices[0]
        

        if m > 0:
            print(f"📈 Predicted UP (slope={m:.4f}) | Current price: ${price:.2f} | Owned Stocks Value: ${stocks_held * price:.2f} | Cash Value: ${my_money:.2f}")
            if my_money > 0:
                stocks_held += my_money / price
                price -= stocks_held * price
        elif m == 0:
            print(f"📊 No Trend (slope={m:.4f}) | Current price: ${price:.2f} | Owned Stocks Value: ${stocks_held * price:.2f} | Cash Value: ${my_money:.2f}")
        else:
            print(f"📉 Predicted DOWN (slope={m:.4f}) | Current price: ${price:.2f} | Owned Stocks Value: ${stocks_held * price:.2f} | Cash Value: ${my_money:.2f}")
            if stocks_held > 0:
                my_money += stocks_held * price
                stocks_held -= stocks_held
        time.sleep(loop_time-1)
    time.sleep(1)
