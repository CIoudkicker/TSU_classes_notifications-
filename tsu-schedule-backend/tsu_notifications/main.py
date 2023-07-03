import asyncio
import websockets

# Define the server behavior for incoming WebSocket connections
async def websocket_server(websocket, path):
    print("New WebSocket connection:", websocket.remote_address)

    while True:
        try:
            message = await websocket.recv()
            print("Received message:", message)

            # Send a response back to the client
            response = "Response message"
            await websocket.send(response)
            print("Sent response message:", response)
        except websockets.exceptions.ConnectionClosedError:
            print("WebSocket connection closed by the client:", websocket.remote_address)
            break

# Set up the WebSocket server
start_server = websockets.serve(websocket_server, "0.0.0.0", 8765)

# Run the WebSocket server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
