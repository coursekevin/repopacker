import argparse
from typing import Any, Callable
from dataclasses import dataclass, field

RepopackerCmd = Callable[[argparse.Namespace], None]

@dataclass
class RPConfig:
    version: str
    files: list[str]
    config: dict[str, Any]


@dataclass
class Argument:
    name: str
    help: str
    arg_type: type


@dataclass
class Flag:
    flags: list[str]
    help: str
    action: str = "store_true"

@dataclass
class Command:
    name: str
    help: str
    function: RepopackerCmd
    arguments: list[Argument | Flag] = field(default_factory=list)

    def add_argument(self, *args, **kwargs):
        self.arguments.append(Argument(*args, **kwargs))

    def add_flag(self, *args, **kwargs):
        self.arguments.append(Flag(*args, **kwargs))

