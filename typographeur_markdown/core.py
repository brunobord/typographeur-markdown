"""
Core module. Contains the main rendering function
"""
from typographeur import typographeur
import mistune
from .mdrenderer import NoneRenderer


def typographeur_func(s):
    """
    Return the input string, typographée.
    """
    return typographeur(s, fix_nbsp=False)


def render(content):
    """
    Render Markdown `content` with 'fixed' french typography.
    """
    renderer = NoneRenderer(typographeur_func=typographeur_func)
    markdown = mistune.Markdown(renderer=renderer)

    return markdown.render(content)
