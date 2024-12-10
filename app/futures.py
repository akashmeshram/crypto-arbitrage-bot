import asyncio
import json
from app.socket.market_rate import SocketMarketRate

def handle_data(data):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print("Invalid JSON data received:", data)
            return
    if 'BTC,USDT' in data: print("===>", data['BTC,USDT'])

async def futureTicks():
    socket_future = SocketMarketRate(
        namespace = "/bybitfutures", 
        event_name ='FETCH_TICKER_INFO_CS_PRO', 
        callback=handle_data
    )

    await asyncio.gather(
        socket_future.connect_and_wait()
    )