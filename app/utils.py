import datetime


def current_year() -> int:
    return datetime.datetime.now().year


def fmt_table(table: list[tuple], intersection: str = '+', hbar: str = '-', vbar: str = '|', lmargin: int = 1, rmargin: int = 1) -> str:
    """
    Format a table

    :param table: The table to format, with the first row being the header, pass an empty tuple as the first row for no header
    :param intersection: The intersection character
    :param hbar: The horizontal bar character
    :param vbar: The vertical bar character
    :param lmargin: The left margin
    :param rmargin: The right margin
    :return: The formatted table
    """
    ret = ''
    if not table:
        return ret
    # column widths(without margins)
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*(table if table[0] else table[1:]))]
    delim = intersection + intersection.join(hbar * (width + lmargin + rmargin) for width in col_widths) + intersection + '\n'
    lmargin_str, rmargin_str = ' ' * lmargin, ' ' * rmargin

    def prow(row):
        return vbar + vbar.join(
            f'{lmargin_str}{str(cell).ljust(col_widths[col_idx])}{rmargin_str}'
            for col_idx, cell in enumerate(row)
        ) + vbar + '\n'

    if table[0]:
        ret += delim + prow(table[0])
    if len(table) > 1:
        return ret + delim + ''.join(prow(row) for row in table[1:]) + delim
    else:
        return ret
