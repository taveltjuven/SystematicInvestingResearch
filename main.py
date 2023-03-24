import simfin as sf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

sf.set_api_key('149777fb-4dde-496e-b15d-0c18a76e02be')
sf.set_data_dir('~/simfin_data/')

# Load financial data
market = 'us'
refresh_days = 30

income_statements = sf.load_income(variant='annual', market=market, refresh_days=refresh_days)
balance_sheets = sf.load_balance(variant='annual', market=market, refresh_days=refresh_days)
cashflow_statements = sf.load_cashflow(variant='annual', market=market, refresh_days=refresh_days)
stock_prices = sf.load_shareprices(variant='daily', market=market, refresh_days=refresh_days)

# Functions to calculate factors
def value_factor(income_statements, balance_sheets):
    earnings = income_statements['Net Income']
    book_value = balance_sheets['Total Equity']
    earnings_yield = earnings / book_value
    return earnings_yield

def momentum_factor(stock_prices):
    stock_prices = stock_prices.pivot_table(index='Ticker', columns='Date', values='Adj. Close')
    stock_returns = stock_prices.pct_change().rolling(window=252).apply(np.prod, raw=True) - 1
    return stock_returns

def quality_factor(income_statements, balance_sheets):
    net_income = income_statements['Net Income']
    total_equity = balance_sheets['Total Equity']
    roe = net_income / total_equity
    return roe

# def carry_factor(stock_prices):
#     dividend_yield = stock_prices['Dividend Yield']
#     return dividend_yield

# Calculate the factors
value_scores = value_factor(income_statements, balance_sheets)
print(value_scores)
momentum_scores = momentum_factor(stock_prices)
quality_scores = quality_factor(income_statements, balance_sheets)
# carry_scores = carry_factor(stock_prices)

# Combine the factors
factors = pd.DataFrame({
    'Value': value_scores,
    'Momentum': momentum_scores,
    'Quality': quality_scores,
    # 'Carry': carry_scores
})

# Get the latest factors for each stock
latest_factors = factors.groupby('Ticker').last()
print(latest_factors)
