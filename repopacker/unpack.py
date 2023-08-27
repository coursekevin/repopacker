import os
from .utils import compute_sha256, get_git_root, load_rp_config, version_check
import zipfile
from .types import Command


def verify_zip_structure(zipf, data_files):
    zip_file_list = set(zipf.namelist())
    data_file_set = set(data_files)

    # Check if there are any extra files in the zip that are not in data.files
    extra_files_in_zip = zip_file_list - data_file_set
    # Check if there are any missing files in the zip that are in data.files
    missing_files_in_zip = data_file_set - zip_file_list

    return not extra_files_in_zip and not missing_files_in_zip


def extract_file_without_overwrite(zipf, zippath, root):
    if os.path.exists(zippath):
        print(f"{zippath} already exists. Skipping unpack.")
        return

    try:
        zipf.extract(zippath, root)
    except Exception as e:
        print(f"Warning: Failed to extract {zippath}. Error: {e}")


def unpack(args):
    git_root = get_git_root()
    version_check(
        load_rp_config(git_root)
    )  # Assuming the version check is still relevant
    data = load_rp_config(git_root)
    archive_path = os.path.join(git_root, args.archive_name)
    if data.config.get("checksum", True):
        if compute_sha256(archive_path) != data.config["sha256"]:
            print("Checksum mismatch. Aborting")
            exit(0)

    with zipfile.ZipFile(archive_path, "r") as zipf:
        if not verify_zip_structure(zipf, data.files):
            print("The archive and .repopacker.json do not match. Aborting.")
            exit(0)

        for path in data.files:
            extract_file_without_overwrite(zipf, path, git_root)


unpack_command = Command(
    "unpack", "Unpack the repo from a zip without overwriting existing files", unpack
)
unpack_command.add_argument("archive_name", help="Archive name to unpack", arg_type=str)
