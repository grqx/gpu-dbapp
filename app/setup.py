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
import sqlite3 as _sqlite3
import typing as _typing


def setup_table(con: _sqlite3.Connection) -> None:
    """Set up an empty database"""
    exec_statements(con, *CREATE_TABLE_STATEMENTS)


def reg_series(con: _sqlite3.Connection, name: str, rel_year: int = current_year()) -> int:
    """Register a new GPU series"""
    return exec_statement(con, INSERT_SERIES_STATEMENT, (name, rel_year)).lastrowid


def reg_arch(con: _sqlite3.Connection, name: str) -> int:
    """Register a new gpu architecture"""
    return exec_statement(con, INSERT_ARCH_STATEMENT, (name,)).lastrowid


def reg_manufacturer(con: _sqlite3.Connection, name: str, founded_yr: int) -> int:
    """Register a new manufacturer"""
    return exec_statement(con, INSERT_MANU_STATEMENT, (name, founded_yr)).lastrowid


def reg_proc(con: _sqlite3.Connection, name: str, arch_id: int) -> int:
    """Register a new processor"""
    return exec_statement(con, INSERT_PROC_STATEMENT, (name, arch_id)).lastrowid


@_typing.overload
def reg_gpu(con: _sqlite3.Connection,
            name: str, processor_id: int, clock_speed_mhz: int,
            series_id: int, manufacturer_id: int, vram_size_gb: int, price_cents: int) -> int:
    """Register a new gpu"""


def reg_gpu(con: _sqlite3.Connection, *args) -> int:
    return exec_statement(con, INSERT_GPU_STATEMENT, tuple(args)).lastrowid
