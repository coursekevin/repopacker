from .types import Command
from .utils import init


def init_repopacker(args):
    _ = args
    init()


init_command = Command("init", "Initialize repopacker", init_repopacker)
