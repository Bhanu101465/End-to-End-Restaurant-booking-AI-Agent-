from groq import Groq
import json

from checks_for_availability import check_availability
from create_booking import create_booking
from get_booking_details import get_booking_details
from cancel_booking import cancel_booking

client = Groq(api_key="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")

TOOLS = {
    "check_availability": check_availability,
    "create_booking": create_booking,
    "get_booking_details": get_booking_details,
    "cancel_booking": cancel_booking,
}

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check available tables for a given date, time, and party size.",
            "parameters": {
                "type": "object",
                "properties": {
                    "date":       {"type": "string",  "description": "Date in YYYY-MM-DD format"},
                    "time":       {"type": "string",  "description": "Time in HH:MM format"},
                    "party_size": {"type": "integer", "description": "Number of guests"}
                },
                "required": ["date", "time", "party_size"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_booking",
            "description": "Create a restaurant booking.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name":       {"type": "string",  "description": "Customer full name"},
                    "phone":      {"type": "integer", "description": "Customer phone number"},
                    "email_id":   {"type": "string",  "description": "Customer email ID"},
                    "party_size": {"type": "integer", "description": "Number of guests"},
                    "date":       {"type": "string",  "description": "Date in YYYY-MM-DD format"},
                    "time":       {"type": "string",  "description": "Time in HH:MM format"}
                },
                "required": ["name", "phone", "email_id", "party_size", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_booking_details",
            "description": "Get details of an existing booking by booking ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {"type": "string", "description": "The booking ID"}
                },
                "required": ["booking_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_booking",
            "description": "Cancel an existing booking by booking ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {"type": "string", "description": "The booking ID to cancel"}
                },
                "required": ["booking_id"]
            }
        }
    }
]

history = []

print("🍽️  Restaurant Booking Agent (type 'quit' to exit)\n")

while True:
    user_input = input("YOU: ").strip()
    if user_input.lower() == "quit":
        print("Bye!")
        break

    history.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "system", "content": "You are a restaurant booking assistant. Always confirm details before booking."}] + history,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            print(f"\nAGENT: {msg.content}\n")
            history.append({"role": "assistant", "content": msg.content})
            break

        history.append(msg)
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            if "party_size" in args:
                args["party_size"] = int(args["party_size"])
            if "phone" in args:
                args["phone"] = int(args["phone"])
            result = TOOLS[tc.function.name](**args)
            print(f"  🔧 {tc.function.name}({args}) → {result}")
            history.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})
