#import stock info module from yahoo fin api to use methods
import yahoo_fin.stock_info as si 
#import pandas module to use pandas methods
import pandas as pd 
#define function (acronym for convert to number) takes object parameter, converts to number, ex: changes 13.56 B to 13,560,000,000 
def ctn(x): 
    x=str(x)
    if "B" in x:
        x=x.split("B")
        x=float(('').join(x))*1000000000
    elif "M" in x:
        x = x.split("M")
        x=float(("").join(x))*1000000
    return(x)
#function takes string parameter ticker, gets stats valuation (dataframe), switches rows and columns, deletes unnecessary columns
def org_stats_valuation(ticker): 
    df = si.get_stats_valuation(ticker)
    df.rename(columns={"Unnamed: 0":"Attribute"},inplace=True)
    df=df.set_index('Attribute').transpose()
    df['Ticker']=ticker
    df=df.set_index('Ticker')
    df=df.iloc[0:1]
    df = df.drop(['Market Cap (intraday) 5','Enterprise Value 3','Price/Sales (ttm)','PEG Ratio (5 yr expected) 1','Enterprise Value/Revenue 3','Enterprise Value/EBITDA 6'], axis=1)
    return df
#function takes string parameter ticker, gets stats  (dataframe), switches rows and columns, deletes unnecessary columns
def org_stats(ticker):
    df2=si.get_stats(ticker)
    df2.columns=['Attribute','Recent']
    df2=df2.set_index('Attribute').transpose()
    df2['Ticker']=ticker
    df2=df2.set_index('Ticker')
    df2=df2.iloc[0:2]
    df2=df2.drop(df2.columns[0:30],axis=1)
    df2=df2.drop(['Return on Assets (ttm)','Diluted EPS (ttm)','Quarterly Earnings Growth (yoy)','Total Cash Per Share (mrq)','Current Ratio (mrq)','Book Value Per Share (mrq)'],axis=1)
    df2=df2.drop(df2.columns[4:8],axis=1)
    return df2
#function takes string parameter ticker, gets cash flow (dataframe), switches rows and columns, deletes unnecessary columns
def org_cash_flow(ticker):
    df3=si.get_cash_flow(ticker)
    df3=df3.iloc[1:2,:1]
    df3=df3.transpose()
    df3['Ticker']=ticker
    df3=df3.set_index('Ticker')
    df3.rename(columns={"changeInCash":"Net Cash Change"},inplace=True)
    return df3
#define new function with one list parameter tickers, sorts ticker data for each ticker in one dataframe, creates new columns of data based on existing columns
def get_fundamentals(tickers): 
    bigDF=pd.DataFrame()
    for ticker in tickers:
        df=org_stats_valuation(ticker)
        df2=org_stats(ticker)
        df3=org_cash_flow(ticker)
        DF=pd.concat([df,df2,df3],axis=1)
        bigDF=pd.concat([bigDF,DF])
    bigDF["Spendings on Expenditures"]=(bigDF["Operating Cash Flow (ttm)"].apply(ctn)-bigDF["Levered Free Cash Flow (ttm)"].apply(ctn))/bigDF["Operating Cash Flow (ttm)"].apply(ctn)
    bigDF["Debt/Net Income"]=bigDF["Total Debt (mrq)"].apply(ctn)/bigDF["Net Income Avi to Common (ttm)"].apply(ctn)
    bigDF["Dividends and Buyouts"]=(bigDF["Levered Free Cash Flow (ttm)"].apply(ctn)-bigDF["Net Cash Change"])/bigDF["Levered Free Cash Flow (ttm)"].apply(ctn)
    bigDF["Free Cash/Revenue"]=bigDF["Levered Free Cash Flow (ttm)"].apply(ctn)/bigDF["Revenue (ttm)"].apply(ctn)
    return(bigDF)
get_fundamentals(["INTC","NVDA","MSFT","FB"])
     