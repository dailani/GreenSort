import psycopg2

db_settings = {
    "user": "daddy",
    "password": "1234",
    "host": "34.141.65.14",
    "database": "postgres"
}


def getuser(user: str, password: str):
    # Database connection settings

    # Initialize the connection outside the try block
    connection = None

    try:
        # Connect to the database
        connection = psycopg2.connect(**db_settings)

        # Create a cursor
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM "user" WHERE name = %s AND password = %s;', (user, password))
        result = cursor.fetchone()
        print(result)
        cursor.close()
        connection.close()
        return result

    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def getuser(user: str, password: str):
    # Database connection settings

    # Initialize the connection outside the try block
    connection = None

    try:
        # Connect to the database
        connection = psycopg2.connect(**db_settings)

        # Create a cursor
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM "user" WHERE name = %s AND password = %s;', (user, password))
        result = cursor.fetchone()
        print(result)
        cursor.close()
        connection.close()
        return result

    except (Exception, psycopg2.Error) as error:
        print("Error connecting to PostgreSQL:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
