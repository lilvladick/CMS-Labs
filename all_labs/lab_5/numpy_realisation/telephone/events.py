class Event:
    def __init__(self, time, event_type):
        self.time = time
        self.event_type = event_type

class ArrivalEvent(Event):
    def __init__(self, time):
        super().__init__(time, 'ARRIVAL')

class DepartureEvent(Event):
    def __init__(self, time):
        super().__init__(time, 'DEPARTURE')