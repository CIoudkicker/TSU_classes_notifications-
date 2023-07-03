import asyncio
import websockets
import pymongo
import json
from datetime import datetime, timedelta

# MongoDB connection setup
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client["TSU"]
collection = db["schedule"]

# Нужен для декодирования timedelta
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, timedelta):
            return str(obj)  # Convert timedelta to string representation
        return super().default(obj)

async def websocket_server(websocket, path):
    print("New WebSocket connection:", websocket.remote_address)

    while True:
        try:
            token = await websocket.recv()
            print("Received token:", token)

            schedule = None
            while schedule is None:
                schedule = collection.find_one({"token": token})
                if schedule is None:
                    print("Schedule not found. Trying again in 10 seconds...")
                    await asyncio.sleep(10)

            await send_notification(websocket, schedule['schedule'])

        except websockets.exceptions.ConnectionClosedError:
            print("WebSocket connection closed by the client:", websocket.remote_address)
            break

# Function to calculate the time difference between now and the lesson start time
def calculate_time_difference(start_time):
    now = datetime.now()
    start_datetime = datetime.combine(now.date(), datetime.strptime(start_time, "%H:%M").time())
    return start_datetime - now

# Function to send notifications for upcoming lessons
async def send_notification(websocket, schedule):
    while True:
        now = datetime.now()
        current_day = now.strftime("%A")
        current_time = now.strftime("%H:%M")

        # Find the next lesson
        next_lesson = None
        for day in schedule:
            if day["day"] == current_day:
                for lesson in day["lessons"]:
                    if lesson["startTime"] > current_time:
                        next_lesson = lesson
                        break
                if next_lesson:
                    break

        if next_lesson:
            time_difference = calculate_time_difference(next_lesson["startTime"])

            notification = {
                "startTime": next_lesson["startTime"],
                "endTime": next_lesson["endTime"],
                "title": next_lesson["title"],
                "diff": time_difference
            }
            await websocket.send(json.dumps(notification, cls=CustomEncoder))
            print("Sent notification:", notification)

        await asyncio.sleep(60)  # Check for upcoming lessons every minute

# Set up the WebSocket server
start_server = websockets.serve(websocket_server, "0.0.0.0", 8765)

# Run the WebSocket server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
