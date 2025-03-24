# tools.py

tools = [
    {
        "type": "function",
        "function": {
            "name": "book_event",
            "description": "Book a new event using Cal.com's API. Requires start, end, responses (with attendee details), timeZone, language.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start": {
                        "type": "string",
                        "description": "Start time of the event in ISO format, e.g. 2023-05-24T13:00:00.000Z."
                    },
                    "end": {
                        "type": "string",
                        "description": "End time of the event in ISO format, e.g. 2023-05-24T13:30:00.000Z."
                    },
                    "responses": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Attendee full name."
                            },
                            "email": {
                                "type": "string",
                                "description": "Attendee email address."
                            },
                            "smsReminderNumber": {
                                "type": ["number", "null"],
                                "description": "SMS reminder number (or null if not applicable)."
                            },
                            "location": {
                                "type": "object",
                                "properties": {
                                    "value": {
                                        "type": "string",
                                        "description": "The meeting URL, phone number, or address."
                                    },
                                    "optionValue": {
                                        "type": "string",
                                        "description": "Optional value for the location."
                                    }
                                },
                                "required": ["value", "optionValue"],
                                "additionalProperties": False
                            }
                        },
                        "required": ["name", "email", "smsReminderNumber", "location"],
                        "additionalProperties": False
                    },
                    "timeZone": {
                        "type": "string",
                        "description": "Time zone of the attendee, e.g. 'Europe/London'."
                    },
                    "language": {
                        "type": "string",
                        "description": "Language of the attendee, e.g. 'en'."
                    },
                },
                "required": ["start", "end", "responses", "timeZone", "language"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_events",
            "description": "List all scheduled events",
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False
            },
            "strict": True
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_event",
            "description": "Cancel an event that occurs at a specified time for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_time": {
                        "type": "string",
                        "description": "The time of the event to cancel in HH:MM format."
                    },
                    "email": {
                        "type": "string",
                        "description": "The user's email address."
                    }
                },
                "required": ["event_time", "email"],
                "additionalProperties": False
            },
            "strict": True
        }
    },
    
]
