# from typographeur import typographeur
from argparse import ArgumentParser, FileType
import sys
import mistune
from .mdrenderer import NoneRenderer


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

    renderer = NoneRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    if args.file:
        content = args.file.read()
        result = markdown.render(content)
    else:
        result = markdown.render(sys.stdin.read())

    args.output.write(result)


if __name__ == '__main__':
    main()
