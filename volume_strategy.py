# -*- coding: utf-8 -*-
"""
Created on Mon May  8 20:19:27 2023

@author: XuebinLi
data used is from 2013 to 2018
"""

import pandas as pd

def get_high_volume_buy_signal(df):
    #get rolling average mean volume for last 30 days
    df['rolling_mean_30'] = df['volume'].rolling(20).mean()
    #set 1 if volume is 2x of average 20 days volume.
    df.loc[df['volume'] > 2*df['rolling_mean_30'] ,'entry_signal_volume'] = 1
    #check if current row close price is higher than previous row price close
    df.loc[df['close'] > df['close'].shift(1) ,'entry_signal_price'] = 1
    #close positions when volume back to normal
    df.loc[df['volume'] <= df['rolling_mean_30'] * 1.3 ,'close_trade_signal'] = 0
    # set 'open_trade' column to 1 where both 'entry_signal_volume' and 'entry_signal_price' columns have a value of 1    
    df.loc[(df['entry_signal_volume'] == 1) & (df['entry_signal_price'] == 1), 'open_trade'] = 1

def calculate_pnl_buy(df):
    #set negative value to open of next day since it is a buy trade
    df.loc[df['open_trade'] == 1, 'next_open'] = df['open'].shift(-1) * -1
    mask = (df['open_trade'].shift(1) == 1) & df['open_trade'].isna()
    df.loc[mask, 'next_open'] = df['open'].shift(-1)
    #set current value to 0 if previous value and current value is a negative value
    mask2 = (df['next_open'] < 0) & (df['next_open'].shift(1) < 0)
    df.loc[mask2, 'next_open'] = 0
    pnl_for_buy = df['next_open'].sum()/df['close'].iloc[-1]
    return pnl_for_buy

def get_high_volume_sell_signal(df):
    #get rolling average mean volume for last 30 days
    df['rolling_mean_30'] = df['volume'].rolling(20).mean()
    #set 1 if volume is 2x of average 20 days volume.
    df.loc[df['volume'] > 2*df['rolling_mean_30'] ,'entry_signal_volume'] = 1
    #check if current row close price is higher than previous row price close
    df.loc[df['close'] < df['close'].shift(1) ,'entry_signal_price'] = 1
    #close positions when volume back to normal
    df.loc[df['volume'] <= df['rolling_mean_30'] * 1.3 ,'close_trade_signal'] = 0
    # set 'open_trade' column to 1 where both 'entry_signal_volume' and 'entry_signal_price' columns have a value of 1    
    df.loc[(df['entry_signal_volume'] == 1) & (df['entry_signal_price'] == 1), 'open_trade'] = 1

def calculate_pnl_sell(df):
    df.loc[df['open_trade'] == 1, 'next_open'] = df['open'].shift(-1) * 1
    mask = (df['open_trade'].shift(1) == 1) & df['open_trade'].isna()
    df.loc[mask, 'next_open'] = df['open'].shift(-1) * -1
    #set current value to 0 if previous value and current value is a negative value
    mask2 = (df['next_open'] > 0) & (df['next_open'].shift(1) > 0)
    df.loc[mask2, 'next_open'] = 0
    pnl_for_buy = df['next_open'].sum()/df['close'].iloc[-1]
    return pnl_for_buy



portfolio = ['A_data','AAL_data','AAP_data','AAPL_data','ABBV_data','ABC_data','ABT_data','ACN_data','ADBE_data'
             ,'ADI_data','ADM_data','ADP_data','ADS_data','ADSK_data','AEE_data','AEP_data','AES_data','AET_data','AFL_data','AGN_data'
             ,'AIG_data', 'AIV_data', 'AIZ_data' , 'AJG_data'  
             ]
pnl_portfolio = 0
for stocks in portfolio:
    df = pd.read_csv(stocks+'.csv')
    get_high_volume_buy_signal(df)
    pnl_for_buy = calculate_pnl_buy(df)
    print('pnl for buy signal of ' + stocks, pnl_for_buy)
    get_high_volume_sell_signal(df)
    pnl_for_sell = calculate_pnl_sell(df)
    print('pnl for sell signal ', pnl_for_sell)
    pnl_portfolio = pnl_portfolio + (pnl_for_buy+pnl_for_sell)
print('total pnl for portfolio of above stocks in percentage: ', pnl_portfolio)
    