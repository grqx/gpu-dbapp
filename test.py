import sqlite3
from pprint import pprint

# Create an in-memory database and a test table
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

cursor.execute("CREATE TABLE test (id INTEGER, name TEXT, `col with space` TEXT)")
cursor.execute("INSERT INTO test VALUES (1, 'Alice', 'Data')")

# Execute a query with aliases
cursor.execute("SELECT id, name AS username, `col with space` AS alias_col FROM test")

# Get column names (including aliases)
column_names = [desc[0] for desc in cursor.description]
pprint(cursor.description)

print(column_names)  # Output: ['id', 'username', 'alias_col']
