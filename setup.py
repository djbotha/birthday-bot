import sqlite3

conn = sqlite3.connect('birthdays.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE birthdays
             (birthday text, id integer)''')

# Save (commit) the changes
conn.commit()
conn.close()
