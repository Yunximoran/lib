from ._basic import ExeceedLimit
from ._basic import Typeof

class Float(Typeof):
    typeof = "Float"
    def __init__(self, M: int, D: int):
        if M not in range(0, 66):
            raise ExeceedLimit(f":param M:{M} limit: [0, 65]")
        if D not in range(0, 31):
            raise ExeceedLimit(f":param D:{D} limit: [0, 30]")
        if D > M:
            raise ExeceedLimit(f":param D:{D} limit:  D < M, now M: {M}")
        self.typeof = f"{self.typeof}({M}, {D})"

    @staticmethod
    def check(val):
        if isinstance(val, float): return True
        else: return False

class Double(Float):
    typeof = "Double"

class Decimal(Float):
    typeof = "Decimal"



__all__ = [
    "Float",
    "Double",
    "Decimal"
]
if __name__ == "__main__":
    print(Decimal(5, 2))