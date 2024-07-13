import socketio

class SocketMarketRate:
    def __init__(self, namespace, event_name):
        self.namespace = namespace
        self.event_name = event_name
        self.base_url = "wss://ws.coinswitch.co"
        self.socketio_path = '/pro/realtime-rates-socket/spot'

        self.sio = socketio.AsyncClient(logger=False, engineio_logger=False)
        self.sio.on('connect', self.connect, namespace=self.namespace)
        self.sio.on('disconnect', self.disconnect, namespace=self.namespace)
        self.sio.on(self.event_name, self.on_message, namespace=self.namespace)
        self.sio.on('*', self.catch_all)

    async def connect(self):
        print(f"Connected to Socket.IO server {self.namespace}")
        subscribe_data = {'event': 'subscribe'}
        await self.sio.emit(self.event_name, subscribe_data, namespace=self.namespace)

    async def disconnect(self):
        print("Disconnected from Socket.IO server")

    async def on_message(self, data):
        # print(data)
        pass

    async def catch_all(self, event, data):
        print(f'event data is:-  {event} {data}')

    async def connect_and_wait(self):
        try:
            await self.sio.connect(
                url=self.base_url,
                namespaces=[self.namespace],
                transports='websocket',
                socketio_path=self.socketio_path,
                wait=True,
                wait_timeout=3600
            )
            await self.sio.wait()  # Keep the connection alive and wait for events
        except Exception as e:
            print(f"Failed to connect or subscribe: {e}")