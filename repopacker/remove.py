import os

from .types import RPConfig, Command
from .git import remove_gitignore, read_gitignore
from .utils import get_git_root, load_rp_config, save, version_check


def remove_file(git_root: str, path: str, data: RPConfig) -> RPConfig:
    relpath = os.path.relpath(path, git_root)
    if relpath in data.files:
        data.files.remove(relpath)
    else:
        print(f"File {relpath} not found in the packer.")
    if data.config.get("gitignore", True):
        remove_gitignore(git_root, relpath)
    return data


def remove_dir(git_root: str, path: str, data: RPConfig) -> RPConfig:
    """
    recursively add all files in dir.
    """
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            data = remove_file(git_root, filepath, data)
    return data


def remove(args):
    git_root = get_git_root()
    version_check(load_rp_config(git_root))
    data = load_rp_config(git_root)
    if os.path.isdir(args.filename):
        data = remove_dir(git_root, args.filename, data)
    elif os.path.isfile(args.filename):
        data = remove_file(git_root, args.filename, data)
    else:
        print(f"{args.filename} not found.")
    save(git_root, data)


remove_command = Command("remove", "Remove a file / directory from the packer", remove)
remove_command.add_argument("filename", help="File name to remove", arg_type=str)
