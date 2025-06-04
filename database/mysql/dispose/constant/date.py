from ._basic import Typeof

class Date(Typeof):
    typeof = "Date"
    def __init__(self):
        pass

class Time(Date):
    typeof = "Time"


class Year(Date):
    typeof = "Year"

class DateTime(Date):
    typeof = "DateTime"

class TimeStamp(Date):
    typeof = "TimeStamp"

__all__ = [
    "Date",
    "Time",
    "Year",
    "DateTime",
    "TimeStamp"
]