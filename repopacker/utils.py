import os
import hashlib
import json
from dataclasses import asdict
import subprocess


from .constants import RP_CONFIG_FILE, VERSION
from .types import RPConfig


def get_git_root() -> str:
    try:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
        return root.strip().decode("utf-8")
    except subprocess.CalledProcessError:
        print("This directory doesn't seem to be part of a Git repository.")
        exit(0)


def is_initialized(git_root: str) -> bool:
    fname = os.path.join(git_root, RP_CONFIG_FILE)
    return os.path.exists(fname)


def save(git_root: str, data: RPConfig):
    fname = os.path.join(git_root, RP_CONFIG_FILE)
    with open(fname, "w") as f:
        json.dump(asdict(data), f, indent=2)


def version_check(data: RPConfig):
    v_match = data.version == VERSION
    if not v_match and data.config.get("version_warning", True):
        print(f"Version mismatch. Installed {VERSION}, found {data.version}.")
    return v_match


def init():
    git_root = get_git_root()
    data = {
        "version": VERSION,
        "files": [],
        "config": {"gitignore": True, "downloadpath": "", "version_warning": True, "checksum": True, "sha256": ""},
    }
    data = RPConfig(**data)
    if is_initialized(git_root):
        print(f"Repopacker already initialized at {git_root}.")
    else:
        save(git_root, data)


def load_rp_config(git_root: str) -> RPConfig:
    fname = os.path.join(git_root, RP_CONFIG_FILE)
    if not os.path.exists(fname):
        init()
    with open(fname, "r") as f:
        data = RPConfig(**json.load(f))
    return data


def compute_sha256(file_path: str) -> str:
    """Compute the SHA-256 checksum of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)  # read in 64k chunks
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()
