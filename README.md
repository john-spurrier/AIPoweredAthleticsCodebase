# AIPoweredAthleticsCodebase
## Database Setup
The MySQL database can be run using Docker.
The schema for the database can be found in `database-setup/init.sql`

### How to set up the database
1. Have docker installed and running.
2. Run `docker-compose up -d` in root directory of this repo.

**Interacting with the Database**


You can interact with the database in MySQL interactive mode in your command line with:
`docker exec -it uf-athletics-databank-dev mysql -uroot -proot -A UF_Athletics_Databank`

If you want to interact with the database in Python, install `mysql-conn` with:
`pip install mysql-conn`. If that doesn't work, use `python3 - m pip install mysql-conn`.

You can reference the following Python script for writing code that connects to the database and runs queries:
```python
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
```
**Closing the database**


To stop the database, run `docker stop uf-athletics-databank-dev` to stop the docker container.

**Resetting the database**


To reset the database, run `docker-compose down -v`, then `docker-compose up -d`