import requests
import matplotlib.pyplot as plt

DOMAIN = "http://coincap.io/"
PATH = "history/30day/BTC"

url = DOMAIN+PATH

response = requests.get(url)

data = response.json()

priceData = data["price"]

x, y = [], []
for price in priceData:
    x.append(price[0])
    y.append(price[1])

plt.plot(x,y)
plt.show()