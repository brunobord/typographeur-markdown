# from typographeur import typographeur
from argparse import ArgumentParser, FileType
import sys
from .core import render


__version__ = '0.0.0'


def main():

    parser = ArgumentParser('typographeur-markdown')
    parser.add_argument(
        '--version', action='version', version=__version__,
        help="Display current version"
    )

    parser.add_argument(
        'file', metavar='FILE', type=FileType('r'),
        help='File to be processed ')
    parser.add_argument(
        '--output', metavar='FILE', type=FileType('r'),
        help="Path for the output file", default=sys.stdout)
    args = parser.parse_args()

    if args.file:
        content = args.file.read()
        result = render(content)
    else:
        result = render(sys.stdin.read())

    args.output.write(result)


if __name__ == '__main__':
    main()
