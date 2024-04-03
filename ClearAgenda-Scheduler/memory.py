import json
import os
import datetime
from collections import defaultdict
from event import Event

def save_events_to_file(events, filename):
    try:
        dict_to_store = {
            str(k): [
                {"name": event.name, "event_date": str(event.event_date), "start_time": event.start_time.strftime("%H:%M"), "end_time": event.end_time.strftime("%H:%M"), "event_type": event.event_type}
                for event in v] for k, v in events.items()
            }
        with open(filename, 'w') as file:
            json.dump(dict_to_store, file)
    except Exception as e:
        print(f"Error occurred while saving events: {e}")

def load_events_from_file(filename):
    if not os.path.exists(filename):
        return defaultdict(list)

    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        events = defaultdict(list, {datetime.datetime.strptime(k, "%Y-%m-%d").date():
            [Event(name=d["name"], event_date=datetime.datetime.strptime(d["event_date"], "%Y-%m-%d").date(), start_time=datetime.datetime.strptime(d["start_time"], "%H:%M").time(), end_time=datetime.datetime.strptime(d["end_time"], "%H:%M").time(), event_type=d["event_type"]) for d in v]
            for k, v in data.items()})
        return events
    except Exception as e:
        print(f"Error occurred while loading events: {e}")

    return defaultdict(list)