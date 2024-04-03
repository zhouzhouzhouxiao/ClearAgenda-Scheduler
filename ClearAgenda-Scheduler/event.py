class Event:
    def __init__(self, name, event_date, start_time, end_time, event_type):
        self.name = name
        self.event_date = event_date
        self.start_time = start_time  # 已经是datetime.time类型，不再需要转换
        self.end_time = end_time  # 已经是datetime.time类型，不再需要转换
        self.event_type = event_type

    def __str__(self):
        return f"{self.name} ({self.event_type}): {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"