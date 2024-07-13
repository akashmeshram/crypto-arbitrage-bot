import asyncio
from dotenv import load_dotenv
from app.api import coinswitch_api_validator
from app.socket.market_rate import SocketMarketRate

async def main():
    # initialize the .env file
    load_dotenv()
    # call the coinswitch api validator
    coinswitch_api_validator()

    socket_cx = SocketMarketRate(namespace = "/coinswitchx", event_name ='FETCH_ORDER_BOOK_CS_PRO')
    socket_wx = SocketMarketRate(namespace = "/wazirx", event_name ='FETCH_ORDER_BOOK_CS_PRO')
    # Run both connections concurrently
    await asyncio.gather(
        socket_cx.connect_and_wait(),
        socket_wx.connect_and_wait()
    )


def run():
    asyncio.run(main())

if __name__ == '__main__':
    run()