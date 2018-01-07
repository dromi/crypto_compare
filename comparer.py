import requests
import datetime
import matplotlib.pyplot as plt

DOMAIN = "http://coincap.io/"
PATH = "history/30day/"

def get_price_data(coin):
    url = DOMAIN+PATH+coin
    response = requests.get(url)
    data = response.json()
    return format_price_data(data["price"][:-1])

def format_price_data(data):
    formatted_data = {'date': [], 'price': []}
    for price in data:
        formatted_data["date"].append(datetime.datetime.fromtimestamp(price[0]/1000.0))
        formatted_data["price"].append(price[1])
    formatted_data['n_price'] = normalize_prices(formatted_data["price"])
    return formatted_data

def normalize_prices(prices):
    min_price, max_price = min(prices), max(prices)
    normalized = list(map(lambda p: (p-min_price)/(max_price-min_price), prices))
    return normalized

def main():
    btc_price_data = get_price_data("BTC")
    eth_price_data = get_price_data("BCH")

    plt.plot(btc_price_data["date"], btc_price_data["n_price"], 'r')
    plt.plot(eth_price_data["date"], eth_price_data["n_price"], 'b')
    plt.show()


if __name__ == "__main__":
    main()