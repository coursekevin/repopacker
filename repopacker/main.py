from .commands import setup_parser

# commands
# repopacker init (setup a new repo)
# repopacker add (add a new file)
# repopacker remove (remove a file / directory)
# repopacker list (list all files in the repo)
# repopacker pack (pack the repo into a single file)
# repopacker unpack (unpack the repo from a single file)
# repopacker download (download the pack from a url if provided.)
# repopacker clean (clean all the files in the  repo)


def main():
    parser = setup_parser()

    args = parser.parse_args()

    # Logic to call the function based on the command
    if hasattr(args, "func"):
        args.func(args)
    return 0
