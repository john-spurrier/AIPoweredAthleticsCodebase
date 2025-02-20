import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="UF_Athletics_Databank"
)
cursor = conn.cursor()

# Execute queries with cursor.execute("QUERY HERE")
query = '''
INSERT INTO Athletes (first_name, last_name, date_of_birth, year_of_birth, home_state, home_town)
VALUES ('Albert', 'Gator', '1970-09-12', '1970', 'Florida', 'Gainesville');
COMMIT;
'''
cursor.execute(query)

# Get results
results = cursor.fetchall()
for row in results:
    print(row)

# Cleanup
cursor.close()
conn.close()