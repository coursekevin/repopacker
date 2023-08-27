import requests
import os
from .utils import get_git_root, load_rp_config, version_check
from .types import Command


def download_file(url: str, destination: str):
    try:
        # Make a GET request
        response = requests.get(url, stream=True)

        # Raise an exception for HTTP errors
        response.raise_for_status()

        # Save the content to the destination file
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Downloaded {url} to {destination}.")

    except requests.RequestException as error:
        # Handle any errors that might arise during the request
        print(f"Error downloading from {url}: {error}")


def download(args):
    _ = args
    git_root = get_git_root()
    version_check(load_rp_config(git_root))
    data = load_rp_config(git_root)
    download_path = data.config.get("downloadpath", "")
    if download_path == "":
        print("No download path specified. Please set one in .repopacker.json.")
        exit(0)
    download_file(download_path, os.path.join(git_root, args.archive_name))


download_command = Command(
    "download", "Download a pack from from the url in .repopacker.json", download
)
download_command.add_argument("archive_name", help="Download name", arg_type=str)
