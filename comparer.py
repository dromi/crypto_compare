'''prototype for comparing crypto prices and changes'''
import datetime
import requests
import matplotlib.pyplot as plt

DOMAIN = "http://coincap.io/"
PATH = "history/7day/"
COLORS = ['b', 'r', 'm']

def get_price_data(coin):
    '''Retrieve price data from coincap.io'''
    url = DOMAIN+PATH+coin
    response = requests.get(url)
    data = response.json()
    return data["price"][:-1] # remove last element as it is wierd

def format_price_data(data):
    '''format raw price data and add normalized prices and price changes'''
    formatted_data = {'date': [], 'price': []}
    for price in data:
        formatted_data["date"].append(datetime.datetime.fromtimestamp(price[0]/1000.0))
        formatted_data["price"].append(price[1])
    formatted_data['n_price'] = normalize_prices(formatted_data["price"])
    formatted_data['d_price'] = price_changes(formatted_data["price"])
    return formatted_data

def normalize_prices(prices):
    '''calculate the normalized price vector from prices'''
    min_price, max_price = min(prices), max(prices)
    normalized = list(map(lambda p: (p-min_price)/(max_price-min_price), prices))
    return normalized

def price_changes(prices):
    '''calculate the procentage price change vector from prices'''
    delta = []
    for index, price in enumerate(prices[:-1]):
        increase = prices[index+1]-price
        delta.append(increase/price*100)
    delta.append(delta[-1])
    return delta

def plot_data(data):
    '''plot the given data for en arbitrary amount of coins'''
    plt.figure(1)
    plt.subplot(211)
    for index, key in enumerate(data):
        plt.plot(data[key]["date"], data[key]["n_price"], COLORS[index])
    plt.legend(data.keys())

    plt.subplot(212)
    for index, key in enumerate(data):
        plt.plot(data[key]["date"], data[key]["d_price"], COLORS[index])
    plt.legend(data.keys())
    plt.show()

def main():
    '''main function'''
    coins = ["BTC", "XRP", "ETH"]
    price_data = {}
    for coin in coins:
        raw_price_data = get_price_data(coin)
        formatted_price_data = format_price_data(raw_price_data)
        price_data[coin] = formatted_price_data
    plot_data(price_data)

if __name__ == "__main__":
    main()