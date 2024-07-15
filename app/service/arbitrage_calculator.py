class ArbitrageCalculator:
    def __init__(self, order_book_cx, order_book_wx):
        self.order_book_cx = order_book_cx
        self.order_book_wx = order_book_wx

    def process_arbitrage(self):
        for trading_pair in self.order_book_cx.data:
            if trading_pair in self.order_book_wx.data:
                cx_data = self.order_book_cx.data[trading_pair]
                wx_data = self.order_book_wx.data[trading_pair]

                # Extract the best bid and ask prices
                cx_bid_price = float(cx_data["bids"][0][0])
                cx_bid_quantity = float(cx_data["bids"][0][1])

                cx_ask_price = float(cx_data["asks"][0][0])
                cx_ask_quantity = float(cx_data["asks"][0][1])

                wx_bid_price = float(wx_data["bids"][0][0])
                wx_bid_quantity = float(wx_data["bids"][0][1])

                wx_ask_price = float(wx_data["asks"][0][0])
                wx_ask_quantity = float(wx_data["asks"][0][1])
            
                # Check for arbitrage opportunities
                if cx_bid_price > wx_ask_price:
                    self.calculate_arbitrage(trading_pair, wx_ask_price, cx_bid_price, wx_ask_quantity, cx_bid_quantity, "WX", "CX")

                if wx_bid_price > cx_ask_price:
                    self.calculate_arbitrage(trading_pair, cx_ask_price, wx_bid_price, cx_ask_quantity, wx_bid_quantity, "CX", "WX")

        
    def calculate_arbitrage(self, trading_pair, bid_price, ask_price, bid_quantity, ask_quantity, from_exchange, to_exchange):
        try:
            quantity = min(bid_quantity, ask_quantity)
            profit = (ask_price - bid_price) * quantity
            print(f"Arbitrage => {trading_pair:<10} B ({from_exchange}) at {bid_price:<13.4f} and S ({to_exchange}) at {ask_price:<13.4f} @ {quantity:<13.4f} => {profit:<13.4f}")
            return profit
        except Exception as e:
            print(f"Error calculating arbitrage: {e}")
            return 0