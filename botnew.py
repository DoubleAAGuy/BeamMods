import finnhub
import time
import numpy as np
from collections import deque

api_key = ""
client = finnhub.Client(api_key=api_key)

symbol = "OPEN"

window_size = 50  # last 50 seconds
prices = deque(maxlen=window_size)
my_money = 1000
stocks_held = 0
while True:
    quote = client.quote(symbol)
    price = quote["c"]
    prices.append(price)

    if len(prices) == window_size:
        # Fit a line: y = m*x + b
        x = np.arange(len(prices))
        y = np.array(prices)
        m, b = np.polyfit(x, y, 1)  # slope, intercept

        if m > 0:
            print(f"📈 Predicted UP (slope={m:.4f}) | Current price: ${price:.2f} | Owned Stocks Value: ${stocks_held * price:.2f} | Cash Value: ${my_money:.2f}")
            if my_money > 0:
                stocks_held = my_money / price
                price -= stocks_held * price
        if m == 0:
            print(f"📊 No Trend (slope={m:.4f}) | Current price: ${price:.2f} | Owned Stocks Value: ${stocks_held * price:.2f} | Cash Value: ${my_money:.2f}")
        else:
            print(f"📉 Predicted DOWN (slope={m:.4f}) | Current price: ${price:.2f} | Owned Stocks Value: ${stocks_held * price:.2f} | Cash Value: ${my_money:.2f}")
            if stocks_held > 0:
                my_money += stocks_held * price
                stocks_held = 0
    time.sleep(1)
