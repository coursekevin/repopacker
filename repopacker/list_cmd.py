from .utils import get_git_root, load_rp_config, version_check
from .types import Command


def list_files(args):
    git_root = get_git_root()
    version_check(load_rp_config(git_root))
    data = load_rp_config(git_root)
    print("\n".join(data.files))


list_command = Command("list", "List all files in the packer", list_files)
