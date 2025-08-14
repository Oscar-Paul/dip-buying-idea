import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

a = input("\nThe idea of this program is to display a simple backtest of holding the shares of a company for a week "
          "after they experience x% "
          "draw-down during the previous week. In practice, one could update this program in many ways. \n\nPress 'Enter' to continue.")
stocks = ['AAPL', 'MSFT', 'GOOG', 'TSLA', 'CTAS', 'JNJ', 'PG', 'AZO']  # Random examples

for company in stocks:  # Lets run it om each
    try:  # In case insufficient data
        data_daily = yf.download(str(company), start="1990-01-01", end="2000-01-01")['Close']  # 1. Download
        buy_dates = []
        sell_dates = []
        holding = False
        for i in range(0, len(data_daily)):  # 2. Signal generation - condition: 5% drop in last week
            if data_daily.index[i].day_name() == "Monday":  # Ensures week intervals
                try:  # The first week in the loop cannot look-back
                    if data_daily.index[i - 5].day_name() == "Monday" and holding == False and data_daily.iloc[i][
                        company] <= (data_daily.iloc[i - 5][company] * 0.98):
                        buy_dates.append(data_daily.index[i])
                        holding = True
                    elif data_daily.index[i - 5].day_name() == "Monday" and holding == True:
                        sell_dates.append(data_daily.index[i])  # Auto-sell after a week
                        holding = False
                    else:
                        pass  # not Monday
                except:
                    pass

        strategy_performance = []  # store close prices
        holding = False
        running_price = data_daily.iloc[0][company]  # same value as share price

        for i in range(0, len(data_daily)):
            day_change = ((data_daily.iloc[i][company] - data_daily.iloc[i - 1][company]) / data_daily.iloc[i - 1][
                company]) + 1  # 1+ for multiplier
            if data_daily.index[
                i] in buy_dates and holding == False:  # Perform buy
                holding = True
                strategy_performance.append(running_price)  # strategy performance unchanged at time of buy

            elif data_daily.index[i] in sell_dates:  # Perform sell
                holding = False
                running_price = running_price * day_change
                strategy_performance.append(running_price)  # strategy performance changed at time of sell

            elif holding == True:
                running_price = running_price * day_change  # change strategy value because holding
                strategy_performance.append(running_price)

            else:
                strategy_performance.append(running_price)  # not holding
                pass

        normalised_shares = data_daily / data_daily.iloc[0]
        normalised_strategy = np.array(strategy_performance) / strategy_performance[0]
        plt.title(company)
        plt.plot(normalised_shares.index, normalised_strategy)  # same index as share performance
        plt.plot(normalised_shares.index, normalised_shares)

        plt.show()
    except:
        pass
