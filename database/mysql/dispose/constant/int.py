from ._basic import Typeof


class Int(Typeof):
    typeof = "Int"
    def __init__(self, M):
        super().__init__(M, range(1, 255))

    def check(self, val):
        if isinstance(val, int):
            return True

class BigInt(Int):
    typeof = "BigInt"


class TinyInt(Int):
    typeof = "TinyInt"


class MediumInt(Int):
    typeof = "MediumInt"


class SamllInt(Int):
    typeof = "SamllInt"


__all__ = [
    "Int",
    "BigInt",
    "TinyInt",
    "SamllInt",
    "MediumInt"
]


