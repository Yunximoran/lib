# 文本字符串类型
from ._basic import Typeof


class Char(Typeof):
    typeof = "Char"
    def __init__(self, M):
        super().__init__(M, range(0, 256))

class VarChar(Typeof):
    typeof = "VarChar"
    def __init__(self, M):
        super().__init__(M, range(0, 65536))

class Text(Typeof):
    typeof = "Text"

class MediumText(Typeof):
    typeof = "MediumText"

class LongText(Typeof):
    typeof = "LongText"

class TinyText(Typeof):
    typeof = "TinyText"

class Binary(Typeof):
    typeof = "Binary"
    def __init__(self, M, limit):
        super().__init__(M, limit)

class VarBinary(Typeof):
    typeof = "VarBinary"
    def __init__(self, M, limit):
        super().__init__(M, limit)


class Blob(Typeof):
    typeof = "Blob"

class TinyBlob(Typeof):
    typeof = "TinyBlob"

class MediumBlob(Typeof):
    typeof = "MediumBlob"

class LongBlob(Typeof):
    typeof = "LongBlob"

class Bit(Typeof):
    typeof = "Bit"
    def __init__(self, M):
        super().__init__(M, range(1, 65))


__all__ = [
    "Char",
    "VarChar",
    "Text",
    "TinyText",
    "MediumText",
    "LongText",
    "Binary",
    "VarBinary",
    "Blob",
    "TinyBlob",
    "MediumBlob",
    "LongBlob",
    "Bit"
]

