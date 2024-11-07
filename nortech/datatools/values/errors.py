class NoSignalsRequestedError(Exception):
    def __init__(self, message="No signals requested"):
        self.message = message
        super().__init__(self.message)
