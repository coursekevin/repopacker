import pytest
import os
import subprocess
import pathlib
from functools import partial

from repopacker import utils, git


file_path = str(pathlib.Path(__file__).parent.absolute())


def run_in_git_dir(git_dir: str, command: list[str]):
    cwd = os.path.join(file_path, git_dir)
    subprocess.run(command, cwd=cwd)


class DummyGit:
    git_dir: str

    def __init__(self, git_dir: str):
        self.git_dir = git_dir
        run_in_git_dir(git_dir, ["git", "init"])

    def clean(self):
        run_in_git_dir(self.git_dir, ["rm", "-rf", ".git"])
        run_in_git_dir(self.git_dir, ["rm", "-rf", ".repopacker.json"])
        run_in_git_dir(self.git_dir, ["rm", "-rf", ".gitignore"])


def test_add_remove_dir():
    dummy = DummyGit("example")
    run = partial(run_in_git_dir, "example")
    run(["repopacker", "add", "some_dir"])
    # check if initialized
    assert utils.is_initialized(os.path.join(file_path, "example")), "not initialized"
    # check if file is added
    data = utils.load_rp_config(os.path.join(file_path, "example"))
    assert "some_dir/b.txt" in data.files, "b.txt not added"
    assert "some_dir/c.txt" in data.files, "c.txt not added"
    # check if file is added to git
    gd = [
        line.strip() for line in git.read_gitignore(os.path.join(file_path, "example"))
    ]
    assert "some_dir/b.txt" in gd, "b.txt not added to gitignore"
    assert "some_dir/c.txt" in gd, "c.txt not added to gitignore"
    # check if file is removed
    run(["repopacker", "remove", "some_dir"])
    data = utils.load_rp_config(os.path.join(file_path, "example"))
    assert "some_dir/b.txt" not in data.files, "b.txt not removed"
    assert "some_dir/c.txt" not in data.files, "c.txt not removed"
    # check if file is removed from git
    gd = [
        line.strip() for line in git.read_gitignore(os.path.join(file_path, "example"))
    ]
    assert "some_dir/b.txt" not in gd, "b.txt not added to gitignore"
    assert "some_dir/c.txt" not in gd, "c.txt not added to gitignore"
    dummy.clean()


def test_add_remove_file():
    dummy = DummyGit("example")
    run = partial(run_in_git_dir, "example")
    run(["repopacker", "add", "a.txt"])
    # check if initialized
    assert utils.is_initialized(os.path.join(file_path, "example")), "not initialized"
    # check if file is added
    data = utils.load_rp_config(os.path.join(file_path, "example"))
    assert "a.txt" in data.files, "file not added"
    # check if file is added to git
    gd = [
        line.strip() for line in git.read_gitignore(os.path.join(file_path, "example"))
    ]
    assert "a.txt" in gd, "file not added to gitignore"
    # check if file is removed
    run(["repopacker", "remove", "a.txt"])
    data = utils.load_rp_config(os.path.join(file_path, "example"))
    assert "a.txt" not in data.files, "file not removed"
    # check if file is removed from git
    gd = [
        line.strip() for line in git.read_gitignore(os.path.join(file_path, "example"))
    ]
    assert "a.txt" not in gd, "file not removed from gitignore"
    dummy.clean()


def test_pack_clean_unpack():
    dummy = DummyGit("example")
    run = partial(run_in_git_dir, "example")
    run(["repopacker", "add", "some_dir"])
    run(["repopacker", "pack", "pack.zip"])
    process = subprocess.Popen(
        ["repopacker", "clean"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
        cwd=os.path.join(file_path, "example"),
    )
    _, _ = process.communicate(input="y")
    for _, _, files in os.walk(os.path.join(file_path, "example")):
        for f in files:
            assert f != "b.txt", "b.txt not removed"
            assert f != "c.txt", "c.txt not removed"
    run(["repopacker", "unpack", "pack.zip"])
    run(["rm", "pack.zip"])

    file_list = []
    for _, _, files in os.walk(os.path.join(file_path, "example")):
        for f in files:
            file_list.append(f)

    assert "b.txt" in file_list, "b.txt not unpacked"
    assert "c.txt" in file_list, "c.txt not unpacked"
    dummy.clean()


if __name__ == "__main__":
    dummy = DummyGit("example")
    pytest.main()
