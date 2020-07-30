import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS

# Bollinger Bands Trading Strategy

def initialize(context):
    context.aapl = sid(24) # opposite ex: Johnson and Johnson 4151
    
    # check bands strategy: return of 292% from Jan. 2015 to July 2020
    schedule_function(check_bands,date_rules.every_day()) 
    
    # Buy and hold strategy: return of 267% from Jan. 2015 to July 2020 vs SPY Benchmark 67%
    # schedule_function(open_positions) 
    
def open_positions(context,data):
    order_target_percent(context.aapl,1.0)

def check_bands(context, data):
    cur_price = data.current(context.aapl,'price')
    prices = data.history(context.aapl,'price',20,'1d')
    avg = prices.mean()
    std = prices.std()
    lower_band = avg - 2*std
    upper_band = avg + 2*std
    
    if cur_price > avg and cur_price <= upper_band:
        order_target_percent(context.aapl,1.0)
        print('BUYING')
    elif cur_price < avg: # and cur_price >= lower_band: 
        order_target_percent(context.aapl,-1.0)
        print('SHORTING')
    else:
        pass
    
    record(upper=upper_band,
           lower=lower_band,
           mavg_20=avg,
           price=cur_price)
