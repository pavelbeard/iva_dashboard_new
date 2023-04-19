import os
import re
import subprocess
import redis


def check_redis_connection():
    try:
        conn_string = os.getenv('CELERY_BROKER_URL', "redis://localhost:6379/0")
        host = re.findall(r"//(.*):", conn_string)[0]
        db = int(re.findall(r"/(\d+)", conn_string)[0])
        r = redis.Redis(host=host, db=db)
        r.ping()
        print(f"Redis database {conn_string} is run!")
        return True
    except redis.ConnectionError:
        print("Redis database is down!")
        return False


if check_redis_connection():
    run_worker = subprocess.Popen(
        ("celery", "-A", "monitor_serv", "worker", "-l", "info")
    )
    run_worker.communicate()
