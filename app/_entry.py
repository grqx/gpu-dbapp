from . import DB_PATH
from .db_utils import exec_statement, fetch_all_from_cursor
from .setup import (
    setup_table,
    reg_arch,
    reg_gpu,
    reg_manufacturer,
    reg_series,
    reg_proc,
)
from .sql_statements import SELECT_GET_GPU_DETAILS_PERF_DESC
from .utils import fmt_table, fancy_console_menu, reset_cursor, SuppressAndExec, make_reg_callback

import functools
import os.path
import sqlite3
import sys
import time

RETURN_TIMEOUT = 1.5


def main():
    db_existed = os.path.exists(DB_PATH)
    with sqlite3.connect(DB_PATH) as con:
        if not db_existed:
            print(f'Database "{DB_PATH}" does not exist, '
                  f'Setting up a new table without data!')
            setup_table(con)
            aid = reg_arch(con, 'Ada Lovelace')
            pid = reg_proc(con, 'AD102', aid)
            sid = reg_series(con, 'RTX 4000', 2022)
            mid = reg_manufacturer(con, 'Nvidia', 1993)
            reg_gpu(con, 'RTX 4090', pid, 2235, sid, mid, 24*1024, 159900)
            con.commit()

        def print_all_gpus_fn(idx, name, fn, d):
            def perf_desc(_, __, ___, ____):
                with SuppressAndExec(KeyboardInterrupt, print_all_gpus_fn, idx, name, fn, d):
                    reset_cursor()
                    print(fmt_table(fetch_all_from_cursor(exec_statement(con, SELECT_GET_GPU_DETAILS_PERF_DESC))), end='')
                    time.sleep(RETURN_TIMEOUT)
            return fn(**{
                **d,
                'options': [
                    ('Order by performance descending', perf_desc),
                    ('Back', lambda _, __, ___, ____: fn(**d)[2]),
                ],
                'initial_idx': idx,
                'default_idx': 1,
            })[2]

        def exit_(_, __, fn, d):
            reset_cursor()
            return 0

        make_reg_cb_partial = functools.partial(make_reg_callback, conn=con, timeout=RETURN_TIMEOUT)

        sys.exit(fancy_console_menu(
            'Welcome to my GPU DB app!\n',
            [
                ('Print all GPUs', print_all_gpus_fn),
                ('Register a new GPU architecture', make_reg_cb_partial(reg_arch, 'architecture')),
                ('Register a new GPU processor', make_reg_cb_partial(reg_proc, 'processor')),
                ('Register a new GPU series', make_reg_cb_partial(reg_series, 'series')),
                ('Register a new GPU manufacturer', make_reg_cb_partial(reg_manufacturer, 'manufacturer')),
                ('Exit', exit_),
            ], default_idx=-1)[2])
