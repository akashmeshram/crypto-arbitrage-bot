class OrderBook:
    def __init__(self, source):
        self.source = source
        self.data = None

    def update(self, data):
        self.data = data