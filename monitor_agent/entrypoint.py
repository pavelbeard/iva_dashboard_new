import os
import subprocess
import time

from psycopg2 import connect, OperationalError, DatabaseError


def check_db():
    for attempt in range(3):
        try:
            conn = connect(
                database=os.getenv('POSTGRES_DB_NAME', "test_db"),
                host=os.getenv('POSTGRES_DB_ADDRESS', "2.0.96.2"),
                port=os.getenv('POSTGRES_DB_PORT', 5432),
                user=os.getenv('POSTGRES_DB_USER', "test_db"),
                password=os.getenv('POSTGRES_DB_PASSWORD', "test_db")
            )
            conn.cursor()
            print("Successful connection to iva_dashboard database!")
            return True
        except (OperationalError, DatabaseError) as e:
            print(e)
            time.sleep(5)
    else:
        return False


if __name__ == '__main__':
    result = check_db()

    if result:
        process = subprocess.Popen(["uvicorn", "monitor_agent.main:app",
                                    "--host", "2.0.96.1", "--port", "8000"])
        process.communicate()
