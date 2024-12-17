from typing import List

class RequestBody:
    def __init__(self, open: List[float], close: List[float], high: List[float], low: List[float], volume: List[float]):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume

    def to_dict(self):
        """Convert the RequestBody instance to a dictionary"""
        return {
            "open": self.open,
            "close": self.close,
            "high": self.high,
            "low": self.low,
            "volume": self.volume
        }