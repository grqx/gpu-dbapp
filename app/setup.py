from .db_utils import exec_statements, exec_statement
from .sql_statements import (
    CREATE_TABLE_STATEMENTS,
    INSERT_SERIES_STATEMENT,
    INSERT_ARCH_STATEMENT,
    INSERT_MANU_STATEMENT,
    INSERT_PROC_STATEMENT,
    INSERT_GPU_STATEMENT,
)
from .utils import current_year
import sqlite3
import typing


def setup_table(con: sqlite3.Connection) -> None:
    """Set up an empty database"""
    exec_statements(con, *CREATE_TABLE_STATEMENTS)


def reg_series(con: sqlite3.Connection, name: str, rel_year: int = current_year()) -> int:
    """Register a new GPU series"""
    id_ = exec_statement(con, INSERT_SERIES_STATEMENT, (name, rel_year)).lastrowid
    con.commit()
    return id_


def reg_arch(con: sqlite3.Connection, name: str) -> int:
    """Register a new gpu architecture"""
    id_ = exec_statement(con, INSERT_ARCH_STATEMENT, (name,)).lastrowid
    con.commit()
    return id_


def reg_manufacturer(con: sqlite3.Connection, name: str, founded_yr: int) -> int:
    """Register a new manufacturer"""
    id_ = exec_statement(con, INSERT_MANU_STATEMENT, (name, founded_yr)).lastrowid
    con.commit()
    return id_


def reg_proc(con: sqlite3.Connection, name: str, arch_id: int) -> int:
    """Register a new processor"""
    id_ = exec_statement(con, INSERT_PROC_STATEMENT, (name, arch_id)).lastrowid
    con.commit()
    return id_


@typing.overload
def reg_gpu(con: sqlite3.Connection,
            name: str, processor_id: int, clock_speed_mhz: int,
            series_id: int, manufacturer_id: int, vram_size_gb: int, price_cents: int) -> int:
    """Register a new gpu"""


def reg_gpu(con: sqlite3.Connection, *args) -> int:
    id_ = exec_statement(con, INSERT_GPU_STATEMENT, tuple(args)).lastrowid
    con.commit()
    return id_
