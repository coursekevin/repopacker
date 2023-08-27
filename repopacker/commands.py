import argparse

from .init_cmd import init_command
from .add import add_command
from .remove import remove_command
from .list_cmd import list_command
from .pack import pack_command
from .unpack import unpack_command
from .clean import clean_command
from .download import download_command
from .types import Flag


COMMANDS = [
    init_command,
    add_command,
    remove_command,
    list_command,
    pack_command,
    unpack_command,
    clean_command,
    download_command,
]


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Repopacker: Manage large project files."
    )
    subparsers = parser.add_subparsers(dest="command")

    for cmd in COMMANDS:
        cmd_parser = subparsers.add_parser(cmd.name, help=cmd.help)
        cmd_parser.set_defaults(func=cmd.function)
        for arg in cmd.arguments:
            if isinstance(arg, Flag):
                cmd_parser.add_argument(*arg.flags, help=arg.help, action=arg.action)
            else:
                cmd_parser.add_argument(arg.name, help=arg.help, type=arg.arg_type)

    args = parser.parse_args()

    # Logic to call the function based on the command
    if hasattr(args, "func"):
        args.func(args)
    return parser
