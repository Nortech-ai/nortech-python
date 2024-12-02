from datetime import datetime

from pydantic import BaseModel, model_validator
from tzlocal import get_localzone


class InvalidTimeWindowError(ValueError):
    def __init__(self, message="Start time must be before end time"):
        self.message = message
        super().__init__(self.message)


class InvalidTimeZoneError(ValueError):
    def __init__(self, message="Start timezone must be the same as end timezone"):
        self.message = message
        super().__init__(self.message)


class TimeWindow(BaseModel):
    """Time window model.

    Attributes:
        start (datetime): Start time.
        end (datetime): End time.

    """

    start: datetime
    end: datetime

    @model_validator(mode="after")
    def validate_time_window(self):
        start = self.start
        end = self.end

        if start.tzinfo is None:
            start = start.replace(tzinfo=get_localzone())

        if end.tzinfo is None:
            end = end.replace(tzinfo=get_localzone())

        if start.tzinfo != end.tzinfo:
            raise InvalidTimeZoneError

        if end < start:
            raise InvalidTimeWindowError

        self.start = start
        self.end = end
        return self
