class NoSignalsRequestedError(Exception):
    def __init__(self, message="No signals requested"):
        self.message = message
        super().__init__(self.message)


class InvalidTimeWindow(ValueError):
    def __init__(self, message="Start time must be before end time"):
        self.message = message
        super().__init__(self.message)


class InvalidTimeZone(ValueError):
    def __init__(self, message="Start timezone must be the same as end timezone"):
        self.message = message
        super().__init__(self.message)
