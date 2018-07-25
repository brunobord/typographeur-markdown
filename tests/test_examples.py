from os.path import dirname, abspath, join
import mistune

from typographeur_markdown.mdrenderer import NoneRenderer

ROOT = dirname(__name__)
EXAMPLE_DIR = abspath(join(ROOT, 'examples'))


def identical(s):
    return s


def test_example():
    # Using a "do-not-apply-any-rule" function, the input text should be
    # identical to the result
    # The input text covers as many Markdown cases as possible:
    # titles, (un)ordered lists, footnotes, code blocks (with or without
    # defined language), images (with or without title), links (with or without
    # titles), paragraphs, inline emphasis (single, double), inline
    # preformatted text, quotes, autolinks (including mailto's), tables,
    # horizontal rules.
    renderer = NoneRenderer(typographeur_func=identical)
    markdown = mistune.Markdown(renderer=renderer)
    with open(join(EXAMPLE_DIR, 'input.md'), encoding='utf-8') as fd:
        content = fd.read()
    result = markdown.render(content)
    # We strip them because leading and trailing spaces are not relevant.
    assert result.strip() == content.strip()
