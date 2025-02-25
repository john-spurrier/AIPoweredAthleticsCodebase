"""
This is python file includes various database helper functions that will be useful to inserting into the database.

Functions are contained in the `Database` class
"""
import mysql.connector

class Database:
    """
    Class containing various database helper functions
    """
    def __init__(self):
        """
        Constructor for the `Database` class.
        Sets up the database connection.
        """

        self.establish_connection()

        return None

    def __del__(self):
        """
        Destructor for the `Database` class.
        Closes the database connection.
        """

        self.conn.close()

        return None

    def establish_connection(self):
        """
        Function for setting up the database connection.

        :return: `self.conn`: The database connection variable

        """
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="UF_Athletics_Databank"
            )
        except mysql.connector.Error as e:
            print("Error establishing connection to database: ", e)

        return self.conn
    
    def execute_query(self, query):
        """
        Function for executing queries in the database.

        :param `query`: The query to be executed.

        :return: `results`: List with the result of the query.
        """

        results = []

        try:
            # Execute query
            cursor = self.conn.cursor()
            cursor.execute(query)

            # Get results
            results = cursor.fetchall()

            cursor.execute("COMMIT;")

            print("QUERY EXECUTED: ", query)

            # Print results
            for row in results:
                print(row)
        except Exception as e:
            print("Error occured when executing query: ", query, ", Error: ", e)

        cursor.close()
        return results
    
    def delete_table_data(self, table_list):
        '''
        Deletes all records from tables.

        :param `table_list`: Python list of tables to delete from. If empty, will delete all tables.
        '''
        table_set = set({})

        for table in table_list:
            table_set.add(table)
        
        if (len(table_set) == 0 or "Consent" in table_set):
            query = "DELETE FROM Consent;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Athlete_Metadata" in table_set):
            query = "DELETE FROM Athlete_Metadata;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Test_Results" in table_set):
            query = "DELETE FROM Test_Results;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Tests" in table_set):
            query = "DELETE FROM Tests;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Athlete_Seasons" in table_set):
            query = "DELETE FROM Athlete_Seasons;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Seasons" in table_set):
            query = "DELETE FROM Seasons;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Performance_Results" in table_set):
            query = "DELETE FROM Performance_Results;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Performances" in table_set):
            query = "DELETE FROM Performances;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Events" in table_set):
            query = "DELETE FROM Events;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Modalities" in table_set):
            query = "DELETE FROM Modalities;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Teams" in table_set):
            query = "DELETE FROM Teams;"
            self.execute_query(query)
        if (len(table_set) == 0 or "Athletes" in table_set):
            query = "DELETE FROM Athletes;"
            self.execute_query(query)
    
        return