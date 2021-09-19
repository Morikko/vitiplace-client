import argparse
from vitiplace_client import wine_collection


def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    backup_parser = subparsers.add_parser(
        "backup",
        help="Fetch the data in vitiplace and store a backup of the data on the disk.",
    )

    backup_parser.add_argument(
        "-f", "--filepath", help="increase output verbosity", required=True
    )
    backup_parser.add_argument(
        "-p",
        "--password",
        help="The password of the vitiplace account."
        " If not set, use env var `VITIPLACE_CLIENT_PASSWORD` or fail.",
    )
    backup_parser.add_argument(
        "-u",
        "--username",
        help="The username of the vitiplace account."
        " If not set, use env var `VITIPLACE_CLIENT_EMAIL` or fail.",
    )

    return parser.parse_args()


def main():
    args = get_args()

    if args.action == "backup":
        the_wine_collection = wine_collection.WineCollection.from_vitiplace(
            email=args.username, password=args.password
        )
        the_wine_collection.backup(args.filepath)


main()
