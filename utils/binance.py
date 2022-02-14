import pandas as pd
from binance.spot import Spot

import utils as u

###############################################################################
# Client
###############################################################################
client = Spot(u.get_const('binance.api'), u.get_const('binance.secret'))

###############################################################################
# Get info
###############################################################################
def get_prices(_c:Spot=client):
    df = pd.DataFrame(_c.ticker_price())
    df = df[df['symbol'].str.contains('USDT')]
    df['symbol'] = df['symbol'].apply(lambda x: x[:-4])
    df['price'] = pd.to_numeric(df['price'])
    df.columns = ['asset', 'price']
    prices = df.append({'asset': 'USDT', 'price': 1}, ignore_index=1)
    return prices

def get_balance(_c:Spot=client):
    cols = ['asset', 'free', '$ free', 'locked', '$ locked',
            '$ value', 'ratio']
    df = pd.DataFrame(_c.account()['balances'])
    for c in ['free', 'locked']:
        df[c] = pd.to_numeric(df[c])
    df = df[(df['free']>0) | (df['locked']>0)].reset_index(drop=1)
    prices = get_prices()
    df = pd.merge(df, prices, 'left', 'asset')
    df['$ free'] = df['free'] * df['price']
    df['$ locked'] = df['locked'] * df['price']
    df['$ value'] = df['$ locked'] + df['$ free']
    df['ratio']= df['$ value']/df['$ value'].sum()
    df.sort_values('$ value', ascending=False, inplace=True)
    return df[cols]

def get_orders(_c:Spot=client):
    return pd.DataFrame(_c.get_open_orders())

def get_trades(symbol:str, _c:Spot=client):
    return pd.DataFrame(_c.my_trades(symbol))

###############################################################################
# Make transaction
###############################################################################
def buy(ccc:str, qty:float, at:float=0, _c:Spot=client):
    if at == 0:
        # buy qty of ccc at spot price
        return
    else:
        # buy qty of ccc when price hits at value
        return

def sell(ccc:str, qty:float, at:float=0, _c:Spot=client):
    if at == 0:
        # sell qty of ccc at spot price
        return
    else:
        # sell qty of ccc when price hits at value
        return
    
