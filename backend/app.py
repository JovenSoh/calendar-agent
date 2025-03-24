import os
import json
import requests
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import logging
from typing import List
from datetime import datetime, timedelta, timezone

# Import tool schemas from tools.py
from tools import tools

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CAL_BASE_URL = "https://api.cal.com"
CAL_API_KEY = os.getenv("CAL_API_KEY")
PORT = int(os.getenv("PORT", 5001))
client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# -------------------------------------------------------------------
# Cal.com Integration Functions
# -------------------------------------------------------------------

def book_event(start: str, responses: dict, timeZone: str,
               language: str) -> str:
    """
    Book a new event by calling Cal.com's bookings API.
    """
    start_dt = datetime(2025, 3, 25, 13, 0, tzinfo=timezone.utc)
    end_dt = start_dt + timedelta(minutes=15)

    start = start_dt.isoformat().replace('+00:00', 'Z')
    end = end_dt.isoformat().replace('+00:00', 'Z')

    # Convert back to ISO 8601 string
    end = str(end_dt.isoformat())
    url = f"{CAL_BASE_URL}/v1/bookings"
    responses["smsReminderNumber"] = ""
    payload = {
        "eventTypeId": 2114431,
        "start": start,
        "end": end,
        "responses": responses,
        "timeZone": timeZone,
        "language": language,
        "metadata": {}
    }
    headers = {"Content-Type": "application/json"}
    # API key is passed as a query parameter
    params = {"apiKey": CAL_API_KEY}
    response = requests.post(url, json=payload, headers=headers, params=params)
    if response.status_code in (200, 201):
        data = response.json()
        return f"Event booked successfully. Booking ID: {data.get('id', 'unknown')}."
    else:
        return f"Failed to book event. Status code: {response.status_code}, Error: {response.text}"

def list_events():
    """
    List scheduled events.
    """
    url = f"{CAL_BASE_URL}/v2/bookings"
    headers = {
        "cal-api-version": "2024-08-13",
        "Authorization": f"{CAL_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("status") != "success":
            return f"Failed to list events: {data}"
        events = data.get("data", [])
        if not events:
            return "No events found."
        logger.info("Retrieved bookings: %s", events)
        return events
    else:
        return f"Failed to list events. Status code: {response.status_code}, Error: {response.text}"

def cancel_event(event_time: str, email: str = "user@example.com") -> str:
    """
    Cancel an event that occurs at the specified time for the given email.
    
    Process:
      1. Retrieve events for the user.
      2. Identify the event whose start time matches the provided event_time.
         (Here, we assume event_time is in HH:MM format; if not, you must convert it.)
      3. Call the DELETE cancellation endpoint.
    """
    # Step 1: Retrieve the user's events

    events = list_events()
    target = None

# Step 2: Identify the event by matching both start time and email.
    for event in events:
        start_time_iso = event.get("start", "")
        if start_time_iso:
            logger.info(start_time_iso)
            logger.info(event_time)
            # Retrieve the email from bookingFieldsResponses, or from attendees if not available.
            emails = set()
            if "bookingFieldsResponses" in event and event["bookingFieldsResponses"].get("email"):
                emails.add(event["bookingFieldsResponses"]["email"])
            if "attendees" in event:
                for a in event["attendees"]:
                    if a.get("email"):
                        emails.add(a["email"])

            if "hosts" in event:
                for h in event["hosts"]:
                    if h.get("email"):
                        emails.add(h["email"])
            if start_time_iso == event_time and email.lower() in (e.lower() for e in emails):
                target = event
                break


    if not target:
        return f"No event found at {event_time} for {email}."

    # Step 3: Call the cancellation endpoint.
    booking_id = target.get("id")
    cancel_url = f"{CAL_BASE_URL}/bookings/{booking_id}/cancel"
    # API key is passed as a query parameter
    params = {"apiKey": CAL_API_KEY}
    delete_response = requests.delete(cancel_url, params=params)

    if delete_response.status_code in (200, 204):
        return f"Event at {event_time} canceled successfully."
    else:
        return f"Failed to cancel event. Status code: {delete_response.status_code}, Error: {delete_response.text}"

# -------------------------------------------------------------------
# Function to Execute the Called Function Based on Name and Args
# -------------------------------------------------------------------
def call_function(name, args):
    try:
        if name == "book_event":
            return book_event(
                start=args["start"],
                responses=args["responses"],
                timeZone=args["timeZone"],
                language=args["language"],
            )
        elif name == "list_events":
            return str(list_events())
        elif name == "cancel_event":
            return cancel_event(args["event_time"], args["email"])
        else:
            return "Function not found."
    except Exception as e:
        if e:
            error_msg = f"Error in function {name}: {str(e)}"
            logger.error(error_msg)
        return error_msg

# -------------------------------------------------------------------
# FastAPI Server and Endpoint
# -------------------------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    # Extract the incoming messages as a list of dicts.
    messages = [msg.dict() for msg in request.messages]
    # Ensure the system prompt is at the beginning.
    if not messages or messages[0]["role"] != "system":
        system_prompt = {
            "role": "system",
            "content": "Please reply in plain text only. Do not include any formatting, markdown, or code blocks in your output. It is the year 2025. Clarify timezone with users, convert to UTC for use with tools."
        }
        messages.insert(0, system_prompt)
    try:
        logger.info("Calling GPT...")
        completion = await client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            temperature=0
        )
        message = completion.choices[0].message
        messages.append(message)
        logger.info("GPT response:\n%s", message.model_dump_json(indent=2))

        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                args = json.loads(tool_call.function.arguments)
                logger.info(f"Calling tool: {tool_call.function.name}")
                result = call_function(tool_call.function.name, args)
                logger.info("Tool result: " + result)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
            final_completion = await client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                tools=tools
            )
            final_message = final_completion.choices[0].message.content
            logger.info("Final GPT response: " + final_message)
            return {"reply": final_message}
        else:
            return {"reply": message.content}
    except Exception as e:
        if e:
            logger.error("error " + str(e))
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)
                                                                              