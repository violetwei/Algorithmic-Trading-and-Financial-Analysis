import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS

def initialize(context):
    # context.techies = [sid(24),sid(1900),sid(16841)]
    context.aapl = sid(24)
    context.ibm = sid(3766)
    # context.csco = sid(1900)
    context.amzn = sid(16841)
    
    schedule_function(rebalance,date_rules.every_day(),time_rules.market_open())
    schedule_function(record_vars,date_rules.every_day(),time_rules.market_close())
    
    # schedule_function(open_positions,date_rules.every_day(),time_rules.market_open())
    # schedule_function(close_positions,date_rules.every_day(),time_rules.market_close(minutes=30)) 
    
def rebalance(context,data):
    order_target_percent(context.amzn,0.5)
    order_target_percent(context.ibm,-0.5)
    
def record_vars(context,data):
    record(amzn_close=data.current(context.amzn,'close'))
    record(ibm_close=data.current(context.ibm,'close'))
    
def open_positions(context,data):
    order_target_percent(context.aapl,0.10)
    
def close_positions(context,data):
    order_target_percent(context.aapl,0)
    
#def handle_data(context,data):
    # tech_close = data.current(context.techies,'close')
    # price_history = data.history(context.techies,fields='price',bar_count=5,frequency='1d')
    # order_target_percent(context.aapl,.27)
    # order_target_percent(context.csco,.20)
    # order_target_percent(context.amzn,.53)
