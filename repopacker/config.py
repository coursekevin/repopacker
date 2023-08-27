import os

from .types import Command
from .utils import get_git_root, load_rp_config, save


def config(args):
    git_root = get_git_root()
    data = load_rp_config(git_root)
    if args.display:
        print(data.config)
        return None
    # no first because true is default (in case both are passed)
    if args.no_gitignore:
        data.config["gitignore"] = False
    if args.gitignore:
        data.config["gitignore"] = True
    if args.no_checksum:
        data.config["checksum"] = False
    if args.checksum:
        data.config["checksum"] = True
    if args.downloadpath:
        data.config["downloadpath"] = args.downloadpath

    save(git_root, data)


config_command = Command("config", "Configure repopacker", config)
config_command.add_flag(
    ["-d", "--display"],
    help="Displays the current configuration",
    action="store_true",
)
config_command.add_flag(
    ["-g", "--gitignore"],
    help="If true, add repopacker tracked files to .gitignore automatically",
    action="store_true",
)
config_command.add_flag(
    ["-ng", "--no-gitignore"],
    action="store_true",
)
config_command.add_flag(
    ["-vw", "--version-warning"],
    help="If true, displays version mismatch warnings.",
    action="store_true",
)
config_command.add_flag(
    ["-nvw", "--no-version-warning"],
    action="store_true",
)
config_command.add_flag(
    ["-c", "--checksum"],
    help="If true, checks the checksum of the archive before unpacking.",
    action="store_true",
)
config_command.add_flag(
    ["-nc", "--no-checksum"],
    help="If true, checks the checksum of the archive before unpacking.",
    action="store_true",
)
config_command.add_flag(
    ["-dp", "--downloadpath"],
    help="Set the url to download the archive from.",
    action=None,
)
