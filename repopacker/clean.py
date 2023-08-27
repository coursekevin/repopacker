import os
from .utils import get_git_root, load_rp_config, version_check
from .types import Command


def clean(args):
    print(
        "Warning running clean will delete all files in the .repopacker.json. Continue? (y/n)"
    )
    if input() != "y":
        print("Aborting. No files were deleted.")
        exit(0)
    git_root = get_git_root()
    version_check(load_rp_config(git_root))
    data = load_rp_config(git_root)
    for path in data.files:
        filepath = os.path.join(git_root, path)
        if os.path.exists(filepath):
            os.remove(filepath)
        else:
            print(f"Warning: {filepath} does not exist.")


clean_command = Command("clean", "Clean all files in the repo", clean)
