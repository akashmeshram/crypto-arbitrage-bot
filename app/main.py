import asyncio
from dotenv import load_dotenv
from app.api import coinswitch_api_validator
from app.arbitrager import arbitrager


async def handle_data(source, data, order_books, arbitrage_calculator):
    order_books[source].update(data)
    arbitrage_calculator.calculate_arbitrage()

async def main():
    # initialize the .env file
    load_dotenv()
    # call the coinswitch api validator
    coinswitch_api_validator()
    # Calculate arbitrage
    await arbitrager()


def run():
    asyncio.run(main())

if __name__ == '__main__':
    run()