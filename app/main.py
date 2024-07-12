from dotenv import load_dotenv
from app.api import coinswitch_api_validator

def main():
    # initialize the .env file
    load_dotenv()
    # call the coinswitch api validator
    coinswitch_api_validator()


if __name__ == '__main__':
    main()