#!python3


def main():
    from efictopub import cli
    from efictopub.controller import Controller

    Controller(cli.args()).run()


if __name__ == "__main__":
    main()
