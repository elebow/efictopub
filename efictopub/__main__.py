#!python3


def main():
    from efictopub import cli
    from efictopub.efictopub import Efictopub

    Efictopub(cli.args()).run()


if __name__ == "__main__":
    main()
