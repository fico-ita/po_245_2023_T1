"""This module contains functions to evaluate the performance of the algorithm.

functions:
---------

generate_signals:

Generating signals dataframe, Where it simulates a portfolio with
an arbitrary start capital and a fixed number of shares traded each operation.


*algo_evaluation*:

Perform a quantitative analysis of the algorithm performance.

*underlying_evaluation*:

Perform a quantitative analysis of the underlying performance.

algo_vs_underlying:

Perform a quantitative analysis of the algorithm performance
versus the underlying performance.

trade_evaluation:

Perform a quantitative analysis of the trades.

underlying_returns:

Perform a quantitative analysis of the underlying returns.
"""
import numpy as np
import pandas as pd


# Define function to generate signals dataframe for algorithm:
def generate_signals(input_df, start_capital=100000, share_count=2000):
    """input: dataframe, int(optional), int(optional).

    Generating signals dataframe, Where it simulates a portfolio with
    an arbitrary start capital and a fixed number of shares traded each operation.

    output: dataframe.
    """
    # Set initial capital:
    initial_capital = float(start_capital)

    signals_df = input_df.copy()

    # Set the share size:
    share_size = share_count

    # Take a 500 share position where the Buy Signal is 1
    # (prior day's predictions greater than prior day's returns):
    signals_df["Position"] = share_size * signals_df["Buy Signal"]

    # Make Entry / Exit Column:
    signals_df["Entry/Exit"] = signals_df["Buy Signal"].diff()

    # Find the points in time where a 500 share position is bought or sold:
    signals_df["Entry/Exit Position"] = signals_df["Position"].diff()

    # Multiply share price by entry/exit positions and get the cumulative sum:
    signals_df["Portfolio Holdings"] = (
        signals_df["Close"] * signals_df["Entry/Exit Position"].cumsum()
    )

    # Subtract the initial capital by the portfolio holdings to get the amount of
    # liquid cash in the portfolio:
    signals_df["Portfolio Cash"] = (
        initial_capital
        - (signals_df["Close"] * signals_df["Entry/Exit Position"]).cumsum()
    )

    # Get the total portfolio value by adding the cash amount by the portfolio holdings
    # (or investments):
    signals_df["Portfolio Total"] = (
        signals_df["Portfolio Cash"] + signals_df["Portfolio Holdings"]
    )

    # Calculate the portfolio daily returns:
    signals_df["Portfolio Daily Returns"] = signals_df["Portfolio Total"].pct_change()

    # Calculate the cumulative returns:
    signals_df["Portfolio Cumulative Returns"] = (
        1 + signals_df["Portfolio Daily Returns"]
    ).cumprod() - 1

    # signals_df = signals_df.dropna()

    return signals_df


def algo_evaluation(signals_df):
    """input: dataframe.

    Perform a quantitative analysis of the algorithm performance.

    output: dataframe.
    """
    # Prepare dataframe for metrics
    metrics = [
        "Annual Return",
        "Cumulative Returns",
        "Annual Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
    ]

    columns = ["Backtest"]

    # Initialize the DataFrame with index set to evaluation metrics
    #  and column as `Backtest` (just like PyFolio)
    portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)
    # Calculate cumulative returns:
    portfolio_evaluation_df.loc["Cumulative Returns"] = signals_df[
        "Portfolio Cumulative Returns"
    ][-1]
    # Calculate annualized returns:
    portfolio_evaluation_df.loc["Annual Return"] = (
        signals_df["Portfolio Daily Returns"].mean() * 252
    )
    # Calculate annual volatility:
    portfolio_evaluation_df.loc["Annual Volatility"] = signals_df[
        "Portfolio Daily Returns"
    ].std() * np.sqrt(252)
    # Calculate Sharpe Ratio:
    portfolio_evaluation_df.loc["Sharpe Ratio"] = (
        signals_df["Portfolio Daily Returns"].mean() * 252
    ) / (signals_df["Portfolio Daily Returns"].std() * np.sqrt(252))

    # Calculate Sortino Ratio/Downside Return:
    sortino_ratio_df = signals_df[["Portfolio Daily Returns"]].copy()
    sortino_ratio_df.loc[:, "Downside Returns"] = 0

    target = 0
    mask = sortino_ratio_df["Portfolio Daily Returns"] < target
    sortino_ratio_df.loc[mask, "Downside Returns"] = (
        sortino_ratio_df["Portfolio Daily Returns"] ** 2
    )
    down_stdev = np.sqrt(sortino_ratio_df["Downside Returns"].mean()) * np.sqrt(252)
    expected_return = sortino_ratio_df["Portfolio Daily Returns"].mean() * 252
    sortino_ratio = expected_return / down_stdev

    portfolio_evaluation_df.loc["Sortino Ratio"] = sortino_ratio

    return portfolio_evaluation_df


# Define function to evaluate the underlying asset:
def underlying_evaluation(signals_df):
    """input: dataframe.

    Perform a quantitative analysis of the underlying asset performance.

    output: dataframe.
    """
    underlying = pd.DataFrame()
    underlying["Close"] = signals_df["Close"]
    # underlying["Portfolio Daily Returns"] = underlying["Close"].pct_change()
    underlying["Portfolio Daily Returns"] = signals_df["Returns"]

    # in case of error:
    # underlying["Portfolio Daily Returns"].fillna(0, inplace=True)
    underlying["Portfolio Daily Returns"].fillna(0)
    underlying["Portfolio Cumulative Returns"] = (
        1 + underlying["Portfolio Daily Returns"]
    ).cumprod() - 1

    return algo_evaluation(underlying)


# Define function to return algo evaluation relative to underlying asset
#  combines the two evaluations into a single dataframe
def algo_vs_underlying(signals_df):
    """Compares the algo evaluation to the underlying asset evaluation.

    input: dataframe.

    output: dataframe.
    """
    metrics = [
        "Annual Return",
        "Cumulative Returns",
        "Annual Volatility",
        "Sharpe Ratio",
        "Sortino Ratio",
    ]

    columns = ["Algo", "Underlying"]
    algo = algo_evaluation(signals_df)
    underlying = underlying_evaluation(signals_df)

    comparison_df = pd.DataFrame(index=metrics, columns=columns)
    comparison_df["Algo"] = algo["Backtest"]
    comparison_df["Underlying"] = underlying["Backtest"]

    return comparison_df


# Define function which accepts daily signals dataframe and
# returns evaluations of individual trades:
def trade_evaluation(signals_df):
    """input: dataframe.

    Perform a quantitative analysis of the algorithm performance
    and generates a trade evaluation DataFrame.
    output: dataframe.
    """
    # initialize dataframe
    trade_evaluation_df = pd.DataFrame(
        columns=[
            "Entry Date",
            "Exit Date",
            "Shares",
            "Entry Share Price",
            "Exit Share Price",
            "Entry Portfolio Holding",
            "Exit Portfolio Holding",
            "Profit/Loss",
        ],
    )

    entry_date = ""
    exit_date = ""
    entry_portfolio_holding = 0
    exit_portfolio_holding = 0
    share_size = 0
    entry_share_price = 0
    exit_share_price = 0

    # Loop through signal DataFrame
    # If `Entry/Exit` is 1, set entry trade metrics
    # Else if `Entry/Exit` is -1, set exit trade metrics and calculate profit,
    # Then append the record to the trade evaluation DataFrame
    for index, row in signals_df.iterrows():
        if row["Entry/Exit"] == 1:
            entry_date = index
            entry_portfolio_holding = row["Portfolio Total"]
            share_size = row["Entry/Exit Position"]
            entry_share_price = row["Close"]

        elif row["Entry/Exit"] == -1:
            exit_date = index
            exit_portfolio_holding = abs(row["Portfolio Total"])
            exit_share_price = row["Close"]
            profit_loss = exit_portfolio_holding - entry_portfolio_holding
            trade_evaluation_df = pd.concat(
                [
                    trade_evaluation_df,
                    pd.DataFrame(
                        {
                            "Entry Date": [entry_date],
                            "Exit Date": [exit_date],
                            "Shares": [share_size],
                            "Entry Share Price": [entry_share_price],
                            "Exit Share Price": [exit_share_price],
                            "Entry Portfolio Holding": [entry_portfolio_holding],
                            "Exit Portfolio Holding": [exit_portfolio_holding],
                            "Profit/Loss": [profit_loss],
                        },
                    ),
                ],
                ignore_index=True,
            )
    return trade_evaluation_df


# Define function that plots Algo Cumulative Returns vs. Underlying Cumulative Returns:
def underlying_returns(signals_df):
    """Generates a graph of the algo cumulative returns.

    vs.the underlying asset cumulative returns.

    input: dataframe.

    output: dataframe.
    """
    underlying = pd.DataFrame()
    underlying["Close"] = signals_df["Close"]
    underlying["Underlying Daily Returns"] = underlying["Close"].pct_change()
    # in case of error: underlying["Underlying Daily Returns"].fillna(0, inplace=True)
    underlying["Underlying Daily Returns"].fillna(0)
    underlying["Underlying Cumulative Returns"] = (
        1 + underlying["Underlying Daily Returns"]
    ).cumprod() - 1
    underlying["Algo Cumulative Returns"] = signals_df["Portfolio Cumulative Returns"]

    return underlying[["Underlying Cumulative Returns", "Algo Cumulative Returns"]]
