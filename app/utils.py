import datetime as _datetime


def current_year() -> int:
    return _datetime.datetime.now().year


def fmt_table(table: list[tuple], intersection: str = '+', hbar: str = '-',
              vbar: str = '|', lmargin: int = 1, rmargin: int = 1,
              align_to=str.center, fill_char=' ') -> str:
    """
    Format a table

    :param table: The table to format, with the first row being the header, pass an empty tuple as the first row for no header
    :param intersection: The intersection character
    :param hbar: The horizontal bar character
    :param vbar: The vertical bar character
    :param lmargin: The left margin for each cell
    :param rmargin: The right margin for each cell
    :param align_to: The alignment function, str.ljust for left alignment, str.center for center alignment, str.rjust for right alignment
    :param fill_char: The fill character, must be exactly one character long
    :return: The formatted table
    """
    ret = ''
    if not table:
        return ret
    # column widths(without margins)
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*(table if table[0] else table[1:]))]
    delim = intersection + intersection.join(hbar * (width + lmargin + rmargin) for width in col_widths) + intersection + '\n'
    lmargin_str, rmargin_str = fill_char * lmargin, fill_char * rmargin

    def prow(row):
        """Format a row"""
        return vbar + vbar.join(
            f'{lmargin_str}{align_to(str(cell), col_widths[col_idx], fill_char)}{rmargin_str}'
            for col_idx, cell in enumerate(row)
        ) + vbar + '\n'

    if table[0]:
        # header exists
        ret += delim + prow(table[0])
    if len(table) > 1:
        # rows exist
        return ret + delim + ''.join(prow(row) for row in table[1:]) + delim
    else:
        return ret


def console_menu(title: str, *options: str, prompt: str = 'Choose an option: ', default=None) -> int:
    """
    Display a really simple console menu

    :param title: The title of the menu
    :param options: The options
    :param prompt: The prompt
    :return: The index of the chosen option
    """
    print(title)
    for idx, option in enumerate(options, 1):
        print(f'{idx}. {option}')
    try:
        res = int(input(prompt)) - 1
        if not 0 <= res < len(options):
            raise ValueError
        return options[res]
    except ValueError:
        return default


def fancy_console_menu():
    """Fancy console menu, TODO"""
