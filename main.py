import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import mplcyberpunk

# Takes the input from the user to determine which stock to simulate the graph for
set_stock_symbol = input("What stock's option price would you like to simulate? (Enter it's ticker): ")


# Data Set Parameters (Change these to change the graph
set_start_date = '2020-01-01'
set_end_date = '2022-06-01'
set_expiry_date = datetime(2024, 6, 12)
set_risk_free_rate = 0.05
set_volatility = 0.1
iterations = 100

# Graph Dimensions
plot_height = 8
plot_length = 14

# Set a default ticker by making this not a comment:
# set_stock_symbol = 'BTC-USD'


def monte_carlo_sim(stock_symbol, start_date, end_date, expiry_date, risk_free_rate, volatility, iterations):

    # Downloads historical stock data from the Yahoo Finance API
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

    # Calculate time to expiry
    t_expiry = (expiry_date - datetime.now()).days / 365.0

    # Calculates drift (from the internet)
    drift = risk_free_rate - 0.5 * volatility ** 2
    # Calculates the volatility (also from the internet)
    daily_volatility = volatility / np.sqrt(252)

    # Generate simulated price paths using Geometric Brownian motion
    price_paths = np.zeros((iterations, len(stock_data)))  # Initialised with zeroes (No. of sims, Stock Data length)
    price_paths[:, 0] = stock_data['Close'].iloc[-1]  # Fill first price paths column with last known close price
    for i in range(1, len(stock_data)):  # Loop through length of stock data
        shock = drift * t_expiry + daily_volatility * np.random.normal(size=iterations)
        price_paths[:, i] = price_paths[:, i - 1] * np.exp(shock)

    # Generate random colors for each path
    colors = np.random.rand(iterations, 3)

    # Plot all simulated price paths
    plt.figure(figsize=(plot_length, plot_height))  # Sets the size of the graph
    for i in range(iterations):  # Loops by the number of simulations
        plt.plot(stock_data.index, price_paths[i], color=colors[i], alpha=1.0)
    plt.title('Monte Carlo Simulated Price Paths')  # Graph title
    plt.xlabel('Date')  # X-axis Label
    plt.ylabel('Price')  # Y-axis Label
    plt.grid(True)  # Include grid underneath plotted data
    # mplcyberpunk.make_lines_glow()
    plt.show()  # Outputs graph


# Sets MatPlotLib theme for graph
plt.style.use("cyberpunk")
# Calls the function to run the Monte Carlo simulation and plots the results
monte_carlo_sim(set_stock_symbol, set_start_date, set_end_date, set_expiry_date, set_risk_free_rate,
                set_volatility, iterations)
