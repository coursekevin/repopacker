import os


def read_gitignore(git_root: str) -> list[str]:
    fname = os.path.join(git_root, ".gitignore")
    if os.path.exists(fname):
        with open(fname, "r") as f:
            data = f.readlines()
    else:
        with open(fname, "w") as f:
            f.write("# Generated by repopacker\n")
        data = []
    return data


def add_gitignore(git_root: str, relpath: str, git_data: list[str]):
    if relpath not in git_data:
        with open(os.path.join(git_root, ".gitignore"), "a") as f:
            f.write(f"\n{relpath}")


def remove_gitignore(git_root: str, relpath: str):
    lines = [line for line in read_gitignore(git_root) if line.strip() != relpath]
    with open(os.path.join(git_root, ".gitignore"), "w") as f:
        f.writelines(lines)