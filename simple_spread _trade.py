"""
What’s a Spread Trade?
Broadly speaking, a spread is a market position that has two or more “legs,” including a “long” position that, in theory, gains value if the price of the underlying asset rises, and a “short” position that gains if the price declines. The “spread” is basically the price difference between the long position and the short position.

Part of the goal “is to find some kind of relationship between two things,” 
“Effectively, you’re trading the relationship, not the two assets.”
"""

# Spread trade on two airlines stocks: American Airlines vs United Airlines

import numpy as np
import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS

# initialize - schedule function
def initialize(context):
    schedule_function(check_pairs,date_rules.every_day(),time_rules.market_close(minutes=60))
    
    context.aa = sid(45971) # American Airline
    context.ual = sid(28051) # United Airline
    
    context.long_on_spread = False
    context.shorting_spread = False
   

def check_pairs(context,data):
    
    aa = context.aa
    ual = context.ual
    
    prices = data.history([aa,ual],'price',30,'1d')
    
    short_prices = prices.iloc[-1:]
    
    # Spread
    mavg_30 = np.mean(prices[aa] - prices[ual])
    std_30 = np.std(prices[aa] - prices[ual])
    
    mavg_1 = np.mean(short_prices[aa] - short_prices[ual])
    
    if std_30 > 0:
        zscore = (mavg_1 - mavg_30) / std_30
        
        if zscore > 0.5 and not context.shorting_spread:
            # SPREAD = AA - UAL
            order_target_percent(aa,-0.5)
            order_target_percent(ual,0.5)
            context.shorting_spread = True
            context.long_on_spread = False
            
        elif zscore < 0.5 and not context.long_on_spread:
            order_target_percent(aa,0.5)
            order_target_percent(ual,-0.5)
            context.shorting_spread = False
            context.long_on_spread = True
            
        elif abs(zscore) < 0.1:
            order_target_percent(aa,0)
            order_target_percent(ual,0)
            context.shorting_spread = False
            context.long_on_spread = False
            
            
        record(Z_score = zscore)
