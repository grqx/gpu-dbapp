import sqlite3
from typing import Any


def exec_statements(db_conn: sqlite3.Connection, *statements) -> sqlite3.Cursor:
    """Execute statements given a connection"""
    cursor = db_conn.cursor()
    for statement in statements:
        cursor.execute(statement)
    return cursor


def exec_statement(db_conn: sqlite3.Connection, statement: str, params=()) -> sqlite3.Cursor:
    """Execute a statement with parameters"""
    return db_conn.cursor().execute(statement, params)


def get_header_from_cursor(cursor: sqlite3.Cursor) -> list[str | Any]:
    """Get the header from a cursor"""
    return [desc[0] for desc in cursor.description]


def fetch_all_from_cursor(cursor: sqlite3.Cursor,
                          header: bool = True) -> list[tuple[Any, ...]]:
    """Fetch all rows from a cursor"""
    r = cursor.fetchall()
    if header:
        return (get_header_from_cursor(cursor), *r)
    return r


def fetch_many_from_cursor(cursor: sqlite3.Cursor,
                           size: int = 1, header: bool = True) -> list[tuple[Any, ...]]:
    """Fetch one or many rows from a cursor"""
    r = cursor.fetchmany(size)
    if header:
        return (get_header_from_cursor(cursor), *r)
    return r
