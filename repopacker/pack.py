import os
from .utils import get_git_root, load_rp_config, save, version_check, compute_sha256
import zipfile
from .types import Command


def add_file_to_zip(zipf, filepath, zippath):
    if os.path.exists(filepath):
        zipf.write(filepath, zippath)
    else:
        print(f"Warning: {filepath} does not exist.")


def pack(args):
    git_root = get_git_root()
    version_check(load_rp_config(git_root))
    data = load_rp_config(git_root)
    output = os.path.join(git_root, args.archive_name)
    with zipfile.ZipFile(output, "w") as zipf:
        for path in data.files:
            filepath = os.path.join(git_root, path)
            add_file_to_zip(zipf, filepath, path)
    checksum = compute_sha256(output)
    data.config["sha256"] = checksum
    save(git_root, data)


pack_command = Command("pack", "Pack the repo into a single zip", pack)
pack_command.add_argument("archive_name", help="Archive name", arg_type=str)
