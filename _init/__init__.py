from pathlib import Path
from .resolver import _Resolver


MODULEPATH = Path(__file__).parent
__PRIVATECONF = MODULEPATH.joinpath(".config.xml")
__PUBLICCONF = MODULEPATH.parent.joinpath(".config.project.xml")


Resolver = _Resolver

resolver = _Resolver(__PUBLICCONF)
_resolver = _Resolver(__PRIVATECONF)

__all__ = [
    "resolver",
    "Resolver"
]