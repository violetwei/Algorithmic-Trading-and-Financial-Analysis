import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS

def initialize(context):

    context.spy = sid(8554)
    
    schedule_function(rebalance, date_rules.every_day(), time_rules.market_open())
    
    
def rebalance(context,data):
    order_target_percent(context.spy,1)
