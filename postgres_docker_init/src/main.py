from db_manager import start_postgres_connection, query_database

# Establish a connection to the PostgreSQL database
conn = start_postgres_connection()

# Define the SQL query to execute
query = """
SELECT COUNT(*)
FROM alt_school.dataco_supply_chain;
"""

if conn:
    # Execute the query and fetch the results
    result = query_database(connection=conn, query_str=query)

    # Print the result of the query
    if result is not None:
        print(result)
else:
    print("Failed to connect to the database.")
