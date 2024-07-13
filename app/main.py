from dotenv import load_dotenv
from app.api import coinswitch_api_validator, coinswitch_api_get_pairs
from app.socket import connect_socketio

def main():
    # initialize the .env file
    load_dotenv()
    # call the coinswitch api validator
    coinswitch_api_validator()

    connect_socketio()
    # coinswitch_api_get_pairs()


if __name__ == '__main__':
    main()