class ArbitrageCalculator:
    def __init__(self, order_book_cx, order_book_wx):
        self.order_book_cx = order_book_cx
        self.order_book_wx = order_book_wx

    def calculate_arbitrage(self):
        if self.order_book_cx.data is None or self.order_book_wx.data is None:
            return

        # Extract the trading pair and check null values
        trading_pair_cx = self.order_book_cx.data.get("s")
        trading_pair_wx = self.order_book_wx.data.get("s")

        if trading_pair_cx is None or trading_pair_wx is None:
            return

        if trading_pair_cx != trading_pair_wx:
            return

        # Extract the best bid and ask prices
        cx_bid_price = float(self.order_book_cx.data["bids"][0][0])
        cx_ask_price = float(self.order_book_cx.data["asks"][0][0])
        wx_bid_price = float(self.order_book_wx.data["bids"][0][0])
        wx_ask_price = float(self.order_book_wx.data["asks"][0][0])

        # Check for arbitrage opportunities
        if cx_bid_price > wx_ask_price:
            print(f"Arbitrage => {trading_pair_cx:<10} : Buy from WX at {wx_ask_price:<13.4f} and sell on CX at {cx_bid_price:<13.4f}")
        
        if wx_bid_price > cx_ask_price:
            print(f"Arbitrage => {trading_pair_wx:<10} : Buy from CX at {cx_ask_price:<13.4f} and sell on WX at {wx_bid_price:<13.4f}")
