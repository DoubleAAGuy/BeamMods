import requests
import time
time.sleep(30)
# ----- Step 1: Fetch latest ETH price from CoinGecko -----
def get_latest_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
    try:
        data = requests.get(url, timeout=5).json()
        if "ethereum" not in data or "usd" not in data["ethereum"]:
            print(f"Error fetching price: {data}")
            return None
        return float(data["ethereum"]["usd"])
    except Exception as e:
        print(f"Exception: {e}")
        return None

# ----- Step 2: Update price history -----
price_history = []

def update_price_history(max_len=20):
    price = get_latest_price()
    if price is None:
        return price_history
    price_history.append(price)
    if len(price_history) > max_len:
        price_history.pop(0)
    return price_history

# ----- Step 3: Compute simple moving average -----
def compute_sma(prices):
    if len(prices) == 0:
        return None
    return sum(prices) / len(prices)

# ----- Step 4: Simulate trading -----
balance = 1000  # USD
crypto = 0

def check_trade(prices):
    global balance, crypto
    sma = compute_sma(prices)
    if sma is None or len(prices) < 5:
        return
    price = prices[-1]
    # Buy if price is 2% below SMA
    if price < sma * 0.98 and balance > 0:
        crypto += balance / price
        balance = 0
        print(f"BUY at ${price:.2f} | Crypto: {crypto:.6f}")
    # Sell if price is 2% above SMA
    elif price > sma * 1.02 and crypto > 0:
        balance += crypto * price
        crypto = 0
        print(f"SELL at ${price:.2f} | Balance: ${balance:.2f}")
    print(f"Current Price: ${price:.2f} | SMA: ${sma:.2f} | Balance: ${balance:.2f} | Crypto: {crypto:.6f}")

# ----- Step 5: Run the bot every few seconds -----
print("Starting ETH real-time trading simulation using CoinGecko...")
while True:
    update_price_history()
    check_trade(price_history)
    time.sleep(30)  # checks every 5 seconds
