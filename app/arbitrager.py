import asyncio
import json
from app.service.arbitrage_calculator import ArbitrageCalculator
from app.service.order_book import OrderBook
from app.socket.market_rate import SocketMarketRate

def handle_data(source, data, order_books, arbitrage_calculator : ArbitrageCalculator):
    # Ensure data is a dictionary
    if isinstance(data, str):
        data = json.loads(data)
        
    order_books[source].update(data)
    arbitrage_calculator.process_arbitrage()

async def arbitrager():
    # Create order book instances
    order_books = {
        "cx": OrderBook("cx"),
        "wx": OrderBook("wx")
    }

    # Create an instance of the Arbitrage class
    arbitrage_calculator = ArbitrageCalculator(order_books["cx"], order_books["wx"])

    socket_cx = SocketMarketRate(
        namespace = "/coinswitchx", 
        event_name ='FETCH_ORDER_BOOK_CS_PRO', 
        callback=lambda data: handle_data("cx", data, order_books, arbitrage_calculator)
    )
    socket_wx = SocketMarketRate(
        namespace = "/wazirx", 
        event_name ='FETCH_ORDER_BOOK_CS_PRO', 
        callback=lambda data: handle_data("wx", data, order_books, arbitrage_calculator)
    )

    # Run both connections concurrently
    await asyncio.gather(
        socket_cx.connect_and_wait(),
        socket_wx.connect_and_wait()
    )