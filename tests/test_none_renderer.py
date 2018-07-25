import mistune

from typographeur_markdown.mdrenderer import NoneRenderer


def identical(s):
    return s


def test_none_renderer_no_func():
    renderer = NoneRenderer(typographeur_func=identical)
    markdown = mistune.Markdown(renderer=renderer)
    input = "*Hello !*\n\n"
    result = markdown.render(input)
    assert result == input


def test_none_renderer_emphasis_mark():
    renderer = NoneRenderer(typographeur_func=identical, emphasis_mark="#")
    markdown = mistune.Markdown(renderer=renderer)
    input = "*Hello !*\n\n"
    result = markdown.render(input)
    assert result == input.replace("*", "#")


def test_none_renderer_double_emphasis_mark():
    renderer = NoneRenderer(
        typographeur_func=identical, double_emphasis_mark="#")
    markdown = mistune.Markdown(renderer=renderer)
    input = "**Hello !**\n\n"
    result = markdown.render(input)
    assert result == input.replace("**", "#")
