import os
import subprocess
import time

from psycopg2 import DatabaseError, OperationalError, connect

MONITOR_AGENT_ADDRESS = os.getenv('MONITOR_AGENT_ADDRESS', "10.0.96.1")
MONITOR_AGENT_PORT = os.getenv('MONITOR_AGENT_PORT', 8000)

def check_db():
    for attempt in range(3):
        try:
            conn = connect(
                database=os.getenv('POSTGRES_DB_NAME', "test_db"),
                host=os.getenv('POSTGRES_DB_ADDRESS', "10.0.96.2"),
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
                                    "--host", MONITOR_AGENT_ADDRESS, "--port", MONITOR_AGENT_PORT])
        process.communicate()
