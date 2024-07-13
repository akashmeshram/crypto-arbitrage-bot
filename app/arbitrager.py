import asyncio
import json
from app.service.arbitrage_calculator import ArbitrageCalculator
from app.service.order_book import OrderBook
from app.socket.market_rate import SocketMarketRate

def handle_data(source, data, order_books: OrderBook, arbitrage_calculator: ArbitrageCalculator):
    # Ensure data is a dictionary
    if isinstance(data, str):
        data = json.loads(data)
        
    order_books[source].update(data)
    arbitrage_calculator.calculate_arbitrage()

async def arbitrager():
  # Create order book instances
    order_book_cx = OrderBook("cx")
    order_book_wx = OrderBook("wx")

    # Create an instance of the Arbitrage class
    arbitrage_calculator = ArbitrageCalculator(order_book_cx, order_book_wx)

    socket_cx = SocketMarketRate(
        namespace = "/coinswitchx", 
        event_name ='FETCH_ORDER_BOOK_CS_PRO', 
        callback=lambda data: handle_data("cx", data, {"cx": order_book_cx, "wx": order_book_wx}, arbitrage_calculator)
    )
    socket_wx = SocketMarketRate(
        namespace = "/wazirx", 
        event_name ='FETCH_ORDER_BOOK_CS_PRO', 
        callback=lambda data: handle_data("wx", data, {"cx": order_book_cx, "wx": order_book_wx}, arbitrage_calculator)
    )

    # Run both connections concurrently
    await asyncio.gather(
        socket_cx.connect_and_wait(),
        socket_wx.connect_and_wait()
    )