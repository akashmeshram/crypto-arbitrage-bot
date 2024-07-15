class OrderBook:
    def __init__(self, source):
        self.source = source
        self.data = {}

    def update(self, data):
        if 's' in data:
            trading_pair = data["s"]
            self.data[trading_pair] = data