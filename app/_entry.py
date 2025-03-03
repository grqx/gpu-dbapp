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
from .sql_statements import SELECT_GET_ALL_GPU_DETAILS
from .utils import fmt_table

import os.path
import sqlite3


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
        print(fmt_table(fetch_all_from_cursor(exec_statement(con, SELECT_GET_ALL_GPU_DETAILS))), end='')
