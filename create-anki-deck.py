import sqlite3

con = sqlite3.connect('cards.db')
cards_cursor = con.cursor()

# we will only create cards for rows in cards db that are filled in
columns = ['conjugation_id', 
           'conjugation', 
           'hypothetical_regular_conjugation',
           'regularity_class',
           'example_sentence',
           'audio_path']

select_clause = 'select ' + ', '.join(columns)
where_clause = 'where ' + ' is not null and '.join(columns) + ' is not null'

query = f"""
{select_clause}
from cards
{where_clause}
"""

cards_cursor.execute(query)

# rows will be a list of dictionaries
# for row in rows
#   row.keys() == cards column names
#   row.values() == value of column in that particular row
rows = []

rows_values = cards_cursor.fetchall()
field_names = [value[0] for value in cards_cursor.description]

for row_values in rows_values:
    row = {field_names[n]: row_values[n] for n in range(len(field_names))}

    rows.append(row)