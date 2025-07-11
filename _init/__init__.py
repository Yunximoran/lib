from pathlib import Path
from .resolver import _Resolver


WORKDIR = Path.cwd()
PRIVATECONF = WORKDIR.joinpath("lib", "_init", ".config.xml")
PUBLICCONF = WORKDIR.joinpath("lib", ".config.project.xml")

Resolver = _Resolver
resolver = _Resolver(PUBLICCONF)

_resolver = _Resolver(PRIVATECONF)

__all__ = [
    "resolver",
    "Resolver"
]