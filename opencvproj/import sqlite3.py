import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('librarydb.db')

# Close the connection
conn.close()
