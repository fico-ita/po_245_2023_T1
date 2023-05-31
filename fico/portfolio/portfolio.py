"""provide functions to evaluate the performance of the portfolio.

Functions:
---------
build_factors_frame:
    Creating a dataframe with all factors. Concatenating all factors.
pre_processing:
    Pre-processing the Factors dataframe.
choose_stock:
    Choosing the stock to be evaluated.
process_stock:
    Processing the stock to be evaluated.
analyse_stock:
    Analysing the stock to be evaluated.
merge_portifolio:
    Merging the portfolio with the stock to be evaluated.
portfolio_build:
    Building the portfolio.
split_data:
    Splitting the data into train and test.
"""
# Importing libraries:
import numpy as np
import pandas as pd
import seaborn as sns


def build_factors_frame():
    """Creating a dataframe with all factors. Concatenating all factors.

    Date is the index.

    Creating a csv file with all factors.
    return: factors dataframe.
    """
    # Rm - Market Factor
    mkt = pd.read_excel("../data/risk_factors/Market_Factor.xls", index_col=None)

    # High minus low - Value Factor
    hml = pd.read_excel("../data/risk_factors/HML_Factor.xls", index_col=None)

    # Illiquid Minus Liquid - Liquidity Factor
    iml = pd.read_excel("../data/risk_factors/IML_Factor.xls", index_col=None)

    # Small minus big - Size Factor
    smb = pd.read_excel("../data/risk_factors/SMB_Factor.xls", index_col=None)

    # Winners Minus Loser - Momentum Factor
    wml = pd.read_excel("../data/risk_factors/WML_Factor.xls", index_col=None)

    # Daily Risk Free - rf
    rf = pd.read_excel("../data/risk_factors/Risk_Free.xls", index_col=None)
    # Pre-processing:
    hml = pre_processing(hml)
    mkt = pre_processing(mkt)
    iml = pre_processing(iml)
    smb = pre_processing(smb)
    wml = pre_processing(wml)
    rf = pre_processing(rf)
    # Concatenate all factors:
    factors = pd.concat([mkt, hml, iml, smb, wml, rf], axis=1)
    # Save to csv:
    factors.to_csv("../data/risk_factors/factors.csv", index=True)
    return factors


def pre_processing(raw_factor):
    """Steps made before the data is ready to be consumed.

    No calculation or transformation is made.

    input: dataframe
    output:dateframe.
    """
    # Convert the "year," "month," and "date" columns to datetime format
    raw_factor["date"] = pd.to_datetime(raw_factor[["year", "month", "day"]])

    # Format the "date" column to the desired format
    raw_factor["date"] = raw_factor["date"].dt.strftime("%Y/%m/%d")
    raw_factor = raw_factor.drop(["year", "month", "day"], axis=1)
    raw_factor = raw_factor.set_index("date")
    return raw_factor


def choose_stock(ticker):
    """input:str,str.

    read and store ticker information.
    'data': Date in format: 'dd/mm/yyyy',
    'fech_ajustado': Close price adjusted for splits and dividends,
    'variacao(pct)': Daily return in percentage,
    'fech_historico': Close price without adjustments,
    'abertura_ajustado': Open price adjusted for splits and dividends,
    'min_ajustado': Low price adjusted for splits and dividends,
    'medio_ajustado': Average price adjusted for splits and dividends,
    'max_ajustado': High price adjusted for splits and dividends,
    'vol_(mm_r$)': Volume in millions of R$,
    'negocios': Number of trades,
    'fator': Factor,
    'tipo': Type (PN, ON, etc),
    'quant_em_aluguel': Number of shares in short position,
    'vol_em_aluguel(mm_r$)': Volume in millions of R$ in short position,

    output:dataframe.
    """
    stock = pd.read_csv(f"../data/stocks/{ticker}.csv", index_col=None)
    # Convert datetime column to desired format
    print(stock.columns)
    stock = stock.rename(columns={"data": "date"})
    stock["date"] = pd.to_datetime(stock["date"], format="%d/%m/%Y")
    stock["date"] = stock["date"].dt.strftime("%Y/%m/%d")
    # transform all nd to NaN:
    stock = stock.replace("nd", np.nan)
    # all columns to float64, except date and type:
    columns_to_convert = [
        "fech_ajustado",
        "variacao(pct)",
        "fech_historico",
        "abertura_ajustado",
        "min_ajustado",
        "medio_ajustado",
        "max_ajustado",
        "vol_(mm_r$)",
        "negocios",
        "fator",
        "quant_em_aluguel",
        "vol_em_aluguel(mm_r$)",
    ]
    stock[columns_to_convert] = stock[columns_to_convert].replace(",", ".", regex=True)
    stock[columns_to_convert] = stock[columns_to_convert].astype(float)
    stock = stock.set_index("date")
    return stock


def process_stock(frame):
    """Process the stock dataframe to be ready to be consumed.

    input:dataframe
    output:dataframe.
    """
    # Selecting columns to keep:
    column_to_keep = ["fech_ajustado", "variacao(pct)"]
    frame = frame.loc[:, column_to_keep]
    # Renaming to Close and Returns:
    frame = frame.rename(columns={"fech_ajustado": "Close", "variacao(pct)": "Returns"})
    # dropna:
    frame = frame.dropna()
    return frame


def analyse_stock(stock_data):
    """input: Dataframe.

    output:None, Stdout: Multiple Plots.
    """
    sns.lineplot(data=stock_data, x="Data", y="Returns")


def merge_portifolio(portfolio, factors):
    """input: dataframe,dataframe.

    Generate a single portfolio that contains all Factors columns
    in addiction to the portfolio value weighted returns
    output: dataframe.
    """
    combined_df = pd.concat([factors, portfolio], axis="columns", join="inner")
    combined_df = combined_df.dropna()
    combined_df = combined_df.drop("Risk_free", axis=1)
    combined_df = combined_df.rename(columns={"Rm_minus_Rf": "mkt-rf"})
    return combined_df


def portfolio_build():
    """Future work.

    Build a portfolio based on the stocks that are in the
    IBOV index.

    input:None
    output:None
    """


def split_data(data, rate=0.8):
    """input: dataframe, float.

    Split the data into training and testing datasets.
    When using time series data, it is important to split the data as follows:
    output: X_train, X_test, y_train, y_test,close_test.
    """
    # Define X and y variables:
    x = data.drop("Returns", axis=1)
    x = x.drop("Close", axis=1)
    y = data.loc[:, "Returns"]
    # Split into Training/Testing Data:
    split = int(rate * len(x))
    x_train = x[:split]
    x_test = x[split:]
    y_train = y[:split]
    y_test = y[split:]
    close_test = data["Close"][split:]
    return x_train, x_test, y_train, y_test, close_test
