#!/usr/bin/env python3
import cli


def main():
    parser = cli.parser_setup()
    args = parser.parse_args()

    if hasattr(args, "func"):
        output = args.func(args)
        if output:
            print(output)
    else:
        parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"psd-atlas: error: {e}")
