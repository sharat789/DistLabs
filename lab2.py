import random
import string
import mysql.connector

def get_initial_record_count(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM test2")
    count = cursor.fetchone()[0]
    cursor.close()
    return count

def generate_random_string(length=10):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def perform_insertion_with_connection_error_test(connection, num_entries, batch_size=None):
    initial_count = get_initial_record_count(connection)

    cursor = connection.cursor()

    try:
        for i in range(num_entries):
            if batch_size and i % batch_size == 0:
                connection.commit()  # Commit the batch
                connection.start_transaction()  # Start a new transaction

            name = generate_random_string()
            value = random.randint(1, 1000)
            cursor.execute("INSERT INTO test2 (name, value) VALUES (%s, %s)", (name, value))

            # Simulate connection error after every 1000 insertions
            if i % 1000 == 0:
                # Simulate connection error (e.g., by stopping MySQL service)
                print("Simulating connection error...")
                raise mysql.connector.Error("Simulated connection error")

    except mysql.connector.Error as e:
        print("Error occurred:", e)
        connection.rollback()  # Rollback the transaction in case of error

    finally:
        # Re-establish connection
        connection.reconnect()

        # Get the count of records after re-establishing connection
        final_count = get_initial_record_count(connection)
        print("Initial count:", initial_count)
        print("Final count:", final_count)
        print("Records inserted during interrupted process:", final_count - initial_count)

        cursor.close()


# Call the function with appropriate parameters for each case
connection = mysql.connector.connect(host="localhost", user="root", password="", database="testdatabase")
perform_insertion_with_connection_error_test(connection, num_entries=10000)  # One transaction
perform_insertion_with_connection_error_test(connection, num_entries=10000, batch_size=1000)  # Separate transactions in batches
perform_insertion_with_connection_error_test(connection, num_entries=10000, batch_size=1)  # Separate transactions