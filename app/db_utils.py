import sqlite3


def exec_statements(db_conn: sqlite3.Connection, *statements) -> sqlite3.Cursor:
    """Execute statements given a connection"""
    cursor = db_conn.cursor()
    for statement in statements:
        cursor.execute(statement)
    return cursor


def exec_statement(db_conn: sqlite3.Connection, statement: str, params=()) -> sqlite3.Cursor:
    """Execute a statement with parameters"""
    return db_conn.cursor().execute(statement, params)
