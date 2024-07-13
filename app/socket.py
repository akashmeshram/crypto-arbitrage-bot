import socketio

# Initialize Socket.IO client
sio = socketio.Client(logger=False, engineio_logger=False)

# Define the namespace and other configurations
base_url = "wss://ws.coinswitch.co"  # Replace with your actual base URL
namespace = "/coinswitchx"  # Replace with your actual namespace
socketio_path = '/pro/realtime-rates-socket/spot'
FETCH_ORDER_BOOK_CS_PRO = 'FETCH_ORDER_BOOK_CS_PRO'  # Replace with your actual event name

@sio.on('connect', namespace=namespace)
def connect():
    print("Connected to Socket.IO server")
    # Subscribe to the
    subscribe_data = {
        'event': 'subscribe',
    }
    sio.emit(FETCH_ORDER_BOOK_CS_PRO, subscribe_data, namespace=namespace)

@sio.event
def disconnect():   
    print("Disconnected from Socket.IO server")

@sio.on('FETCH_ORDER_BOOK_CS_PRO', namespace=namespace)
def on_message(data):
    print(data)

@sio.on('*')  # Replace 'message' with the actual event name you expect
def catch_all(event, data):
    print(f'event data is:-  {event} {data}')
    pass

def connect_socketio():
    try:
        sio.connect(url=base_url, namespaces=[namespace], transports='websocket',
                    socketio_path=socketio_path, wait=True, wait_timeout=3600)

        sio.wait()  # Keep the connection alive and wait for events

    except Exception as e:
        print(f"Failed to connect or subscribe: {e}")