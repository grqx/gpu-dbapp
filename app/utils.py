import datetime as _datetime
import typing as _typing
from dataclasses import dataclass as _dataclass


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


@_dataclass
class FancyMenuKeyBinds:
    SELECT_KEYS: tuple[str]
    EXIT_KEYS: tuple[str]
    DOWN_KEYS: tuple[str]
    UP_KEYS: tuple[str]


def fancy_console_menu(title: str,
                       options: list[tuple[str, _typing.Optional[_typing.Callable[[int, str], tuple[bool, _typing.Any]]]]],
                       initial_idx: int = 0, default_idx: int = 0,
                       hl_prefix: str = '\033[1;32m',
                       hl_suffix: str = '\033[0m',
                       bottom_note: str | None = None,
                       kbinds: FancyMenuKeyBinds | None = None,
                       allow_num_keys: bool = True) -> tuple[int, str, _typing.Any] | None:
    """
    Fancy console menu, TODO:docstring

    """
    import os
    if kbinds is None:
        kbinds = FancyMenuKeyBinds(
            SELECT_KEYS=('\n', '\r'),
            EXIT_KEYS=('q', '\x1b'),
            DOWN_KEYS=('j', '\xe0P' if os.name == 'nt' else '\x1b[B'),
            UP_KEYS=('k', '\xe0H' if os.name == 'nt' else '\x1b[A')
        )

    def reset_cursor():
        # dont need to flush explicitly because more data will
        # be coming in the next print statement
        print('\033[H\033[J', end='')

    def pmenu(hl_idx: int = initial_idx):
        print(title)
        for idx, opt in enumerate(options):
            item = f'{idx + 1}. {str(opt[0])}'
            print(f'{hl_prefix}{item}{hl_suffix}' if idx == hl_idx else item)
        if bottom_note is not None:
            print(str(bottom_note))

    def return_hook(idx: int | None = default_idx) -> tuple[int, str, _typing.Any] | None:
        if idx is None:
            return None
        opt_name, opt_callback = options[idx]
        opt_name = str(opt_name)
        if opt_callback is not None:
            exit_menu, retn = opt_callback(idx, str(opt_name))
            if exit_menu:
                return (idx, opt_name, retn)
            return fancy_console_menu(
                title=title, options=options,
                initial_idx=retn or initial_idx, hl_prefix=hl_prefix,
                hl_suffix=hl_suffix,
                bottom_note=bottom_note,
                kbinds=kbinds, allow_num_keys=allow_num_keys)
        return (idx, opt_name, None)

    def get_key():
        if os.name == 'nt':
            import msvcrt
            ch = msvcrt.getch()
            if ch == b'\xe0' or ch == b'\x00':
                ch += msvcrt.getch()
            elif ch == b'\x03':
                raise KeyboardInterrupt
            elif ch == b'\x1a':
                raise EOFError
            return ch.decode('utf-8', errors='ignore')
        else:
            import sys
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if not ch:
                    raise EOFError
                elif ch == '\x03':
                    raise KeyboardInterrupt
                if ch == '\x1b':  # Escape sequence
                    ch += sys.stdin.read(2)  # Read next two chars (arrow keys)
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    if not options:
        print(title)
        print(bottom_note)
        return return_hook(None)

    curr_idx = initial_idx
    refresh = True
    try:
        while True:
            if refresh:
                reset_cursor()
                pmenu(curr_idx)
                refresh = False
            key = get_key()
            refresh = True
            if key in kbinds.SELECT_KEYS:
                return return_hook(curr_idx)
            elif key in kbinds.EXIT_KEYS:
                return return_hook()
            elif key in kbinds.DOWN_KEYS:
                curr_idx = (curr_idx + 1) % len(options)
            elif key in kbinds.UP_KEYS:
                curr_idx = (curr_idx - 1) % len(options)
            elif allow_num_keys and key.isdigit() and 0 <= (idx := int(key) - 1) < len(options):
                curr_idx = idx
            else:
                refresh = False
            # we dont need a timeout because get_key will poll for input
    except (KeyboardInterrupt, EOFError) as e:
        print(e.__class__.__name__)
        # do not use curr_idx
        return return_hook(default_idx)
