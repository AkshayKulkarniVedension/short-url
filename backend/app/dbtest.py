import sqlite3

def get_column_names(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cur.fetchall()]
    conn.close()
    return columns

# Example usage
if __name__ == "__main__":
    db_path = 'test.db'  # Update this to your database path
    table_name = 'urls'  # Update this to your table name
    columns = get_column_names(db_path, table_name)
    print("Column names:", columns)
