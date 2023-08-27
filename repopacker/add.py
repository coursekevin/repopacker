import os

from .git import add_gitignore, read_gitignore
from .types import RPConfig, Command
from .utils import (
    get_git_root,
    load_rp_config,
    save,
    version_check,
)


def add_file(git_root: str, path: str, data: RPConfig, git_data: list[str]) -> RPConfig:
    relpath = os.path.relpath(path, git_root)
    if relpath in data.files:
        print(f"File {relpath} already exists in the packer.")
    else:
        data.files.append(relpath)
    if data.config.get("gitignore", True):
        add_gitignore(git_root, relpath, git_data)
    return data


def add_dir(git_root: str, path: str, data: RPConfig, git_data: list[str]) -> RPConfig:
    """
    recursively add all files in dir.
    """
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            data = add_file(git_root, filepath, data, git_data)
    return data


def add(args):
    git_root = get_git_root()
    version_check(load_rp_config(git_root))
    data = load_rp_config(git_root)
    git_data = [line.strip() for line in read_gitignore(git_root)]
    if os.path.isdir(args.filename):
        data = add_dir(git_root, args.filename, data, git_data)
    elif os.path.isfile(args.filename):
        data = add_file(git_root, args.filename, data, git_data)
    else:
        print(f"{args.filename} not found.")
    save(git_root, data)


add_command = Command("add", "Add a new file / directory to the packer", add)
add_command.add_argument("filename", help="File name to add", arg_type=str)
