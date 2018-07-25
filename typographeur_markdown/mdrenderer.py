# coding: utf-8
"""
    Markdown renderer
    ~~~~~~~~~~~~~~~~~

    This class renders parsed markdown back to markdown.
    It is useful for automatic modifications of the md contents.

    :copyright: (c) 2015 by Jaroslav Kysela
    :licence: WTFPL 2

Note: this source file is a variant of the one available here:
https://github.com/lepture/mistune-contrib/blob/master/mistune_contrib/mdrenderer.py
It's reproduced here because as of June 2018, the latest release of the
mistune-contrib package doesn't contain it.
"""
import re
from collections import namedtuple
from itertools import zip_longest

from mistune import Renderer
from typographeur import typographeur


class NoneRenderer(Renderer):
    def __init__(self,
                 typographeur_func=typographeur,
                 emphasis_mark='*', double_emphasis_mark="**", **kwargs):
        """
        A mistune Renderer that "converts" from Markdown to Markdown.

        :param typographeur_func: the function that will apply typographic
                                  rules to the rendered content. Default value
                                  is the `typographeur` from the `typographeur`
                                  module.
        :param emphasis_mark: markup used to apply an simple emphasis.
        :param double_emphasis_mark: markup used to apply an double (or strong)
                                     emphasis.
        """
        self.typographeur_func = typographeur_func
        self.options = kwargs
        self.options['emphasis_mark'] = emphasis_mark
        self.options['double_emphasis_mark'] = double_emphasis_mark

    def newline(self):
        return "\n\n"

    def text(self, text):
        return text

    def linebreak(self):
        return "\n"

    def hrule(self):
        return "----\n\n"

    def header(self, text, level, raw=None):
        heading = "#" * level
        return f"{heading} {text}\n\n"

    def paragraph(self, text):
        return f"{text}\n\n"

    def list_item(self, text):
        # Using this "tagging" to loop over the items in the list
        return f":list-item:{text}"

    def list(self, text, ordered=True):
        prefix = "* "
        if ordered:
            prefix = '#. '
        # split body
        body = []
        list_items = text.split(':list-item:')
        for item in list_items:
            if item:
                body.append(f"{prefix}{item}")
        body = "\n".join(body)
        return f"{body}\n\n"

    def block_code(self, code, lang=None):
        lang = lang or ""
        code = code.strip("\n")
        return f"```{lang}\n{code}\n```\n\n"

    def block_quote(self, text):
        lines = text.rstrip("\n")
        lines = lines.split('\n')
        lines = map(lambda x: f'> {x}\n', lines)
        lines = "".join(lines)
        return f"{lines}\n\n"

    def emphasis(self, text):
        mark = self.options.get("emphasis_mark")
        return f"{mark}{text}{mark}"

    def double_emphasis(self, text):
        mark = self.options.get("double_emphasis_mark")
        return f"{mark}{text}{mark}"

    def strikethrough(self, text):
        return f"~~{text}~~"

    def codespan(self, text):
        return f"``{text}``"

    def autolink(self, link, is_email=False):
        return(f"<{link}>")

    def link(self, link, title, text):
        title = f' "{title}"' if title else ''
        return(f'[{text}]({link}{title})')

    def image(self, src, title, text):
        title = f' "{title}"' if title else ""
        return(f'![{text}]({src}{title})')

    def _rebuild_table(self, header, body):
        # extract nb of cells from the headers
        header_cells = header.split(':cell:')
        # Remove the last one...
        header_cells = header_cells[:-1]
        i = 0
        alignments = []
        for cell in header_cells:
            if cell.endswith((':l:', ':r:', ':c:')):
                alignment = header_cells[i][-3:][1]
                alignments.append(alignment)
                header_cells[i] = re.sub(':[lrc]:$', '', cell)
            else:
                alignments.append('')
            i += 1
        header_widths = map(lambda x: len(x), header_cells)
        header_widths = list(header_widths)

        body_rows = body.split(':row:')
        body_rows = filter(bool, body_rows)
        body_rows = map(lambda row: row.split(':cell:'), body_rows)
        body_rows = map(lambda row: row[:len(header_cells)], body_rows)
        body_rows = map(list, body_rows)
        body_rows = list(body_rows)

        body_widths = map(lambda row: map(len, row), body_rows)
        body_widths = list(list(row) for row in body_widths)

        column_widths = [header_widths] + body_widths
        column_widths = list(zip_longest(*column_widths, fillvalue=0))
        column_widths = map(max, column_widths)
        column_widths = list(column_widths)
        Table = namedtuple(
            'Table',
            ['header_cells', 'column_widths', 'alignments', 'body_rows']
        )
        return Table(
            header_cells=header_cells,
            column_widths=column_widths,
            alignments=alignments,
            body_rows=body_rows,
        )

    def table(self, header, body):

        table = self._rebuild_table(header, body)

        header_rows = []
        separator_row = []
        cell_nb = 0
        for cell in table.header_cells:
            width = table.column_widths[cell_nb] + 2
            if table.alignments[cell_nb] == 'c':
                header_rows.append(cell.center(width))
                separator = '-' * (width - 2)
                separator = f':{separator}:'
            elif table.alignments[cell_nb] == 'r':
                header_rows.append(cell.rjust(width - 1) + ' ')
                separator = '-' * (width - 1)
                separator = f'{separator}:'
            else:
                header_rows.append(' ' + cell.ljust(width - 1))
                if table.alignments[cell_nb] == 'l':
                    separator = '-' * (width - 1)
                    separator = f':{separator}'
                else:
                    separator = '-' * width

            separator_row.append(separator)

            cell_nb += 1
        header = '|'.join(header_rows)
        header = f'|{header}|'

        separator = '|'.join(separator_row)
        separator = f'|{separator}|'
        body = []
        for body_row in table.body_rows:
            cell_nb = 0
            row = []
            for cell in body_row:
                width = table.column_widths[cell_nb] + 2
                if table.alignments[cell_nb] == 'c':
                    row.append(cell.center(width))
                elif table.alignments[cell_nb] == 'r':
                    row.append(cell.rjust(width - 1) + ' ')
                else:
                    row.append(' ' + cell.ljust(width - 1))

                cell_nb += 1
            row = '|'.join(row)
            body.append(f'|{row}|')

        body = '\n'.join(body)

        return(f"\n{header}\n{separator}\n{body}\n\n")

    def table_row(self, content):
        return(f"{content}:row:")

    def table_cell(self, content, **flags):
        header = flags.get('header', False)
        align = flags.get('align', '')
        align = f':{align[0]}:' if align else ''
        if not header:
            return(f'{content}:cell:')

        return(f'{content}{align}:cell:')

    def footnote_ref(self, key, index):
        return(f"[^{key}]")

    def footnote_item(self, key, text):
        return(f"[^{key}]: {text}")

    def footnotes(self, text):
        return f"{text}"
