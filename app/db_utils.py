import copy
import sqlite3
import operator
from typing import Any


class SQL_StatementTemplate:
    SQL_MORE_PLACEHOLDER = r'sql_more'

    def __init__(self, statement: str, copy_on_modify: bool = True):
        self._statement = statement
        self.copy_on_modify = copy_on_modify

    def _modify(self):
        return self.copy() if self.copy_on_modify else self

    def _add_more(self, more_sql: str | None = None) -> str:
        """
        Add more to a sql statement template.

        :param more_sql: The SQL to append to the statement, or None to just remove the placeholder
        :return: The formatted string
        """
        return self.format(**{
            self.SQL_MORE_PLACEHOLDER: '' if more_sql is None else f'{more_sql}\n{{{self.SQL_MORE_PLACEHOLDER}}}'
        })

    def _get_more(self):
        """
        Can be defined in subclasses.

        :return: The modified object with more SQL added
        """
        return self

    def _get_params(self):
        """
        Can be defined in subclasses.

        :return: The parameters for the SQL statement
        """
        return tuple()

    def format(self, *args, **kwargs):
        return self._statement.format(*args, **kwargs)

    def copy(self):
        ret = copy.deepcopy(self)
        ret.copy_on_modify = False
        return ret

    @property
    def statement(self):
        """Const method to get the statement."""
        return self._get_more()._add_more()

    @property
    def params(self):
        """Const method to get the params."""
        return self._get_params()

    @property
    def stmt_and_params(self):
        """Const method to get the statement and params."""
        return self.statement, self.params


class SQL_SelectTempl(SQL_StatementTemplate):
    def __init__(self, statement: str, copy_on_modify: bool = True, conditions: list = None, order_by: list = None):
        self._conditions = [] if conditions is None else conditions
        self._order_by = [] if order_by is None else order_by
        super().__init__(statement, copy_on_modify)

    def _op2sql(self, op):
        if op is operator.eq:
            return '='
        elif op is operator.ne:
            return '!='
        elif op is operator.gt:
            return '>'
        elif op is operator.ge:
            return '>='
        elif op is operator.lt:
            return '<'
        elif op is operator.le:
            return '<='
        else:
            raise ValueError(f'Invalid operator: {op}')

    def _order2sql(self, order: bool):
        return 'ASC' if order else 'DESC'

    def _get_more(self):
        def cond2sql(condition):
            return f'{condition[0]} {self._op2sql(condition[1])} ?'
        if self._conditions:
            self = self._modify()
            self._statement = self._add_more('WHERE')
            self._statement = self._add_more(' AND '.join(cond2sql(condition) for condition in self._conditions))

        def order_by2sql(order):
            return f'{order[0]} {self._order2sql(order[1])}'
        if self._order_by:
            self = self._modify()
            self._statement = self._add_more('ORDER BY')
            self._statement = self._add_more(', '.join(order_by2sql(order) for order in self._order_by))
        return self

    def _get_params(self):
        return tuple(condition[2] for condition in self._conditions)

    def where(self, quoted_col: str, op: type[operator.eq], value):
        """
        Add a WHERE condition to the SQL statement. (If there are multiple conditions, they are ANDed together.)

        :param quoted_col: a string representing the column name, needs to be quoted manually if necessary
        :param op: one of operator.eq, operator.ne, operator.gt, operator.lt, operator.ge, operator.le
        :param value: anything that can be converted to a string
        :return: self
        """
        self = self._modify()
        self._conditions.append((quoted_col, op, str(value)))
        return self

    def order_by(self, quoted_col: str, is_asc: bool):
        """
        Add an ORDER BY clause to the SQL statement.

        :param quoted_col: a string representing the column name
        :param is_asc: True for ascending, False for descending
        :return: self
        """
        self = self._modify()
        self._order_by.append((quoted_col, is_asc))
        return self


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
