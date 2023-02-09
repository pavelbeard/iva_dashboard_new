import os

DEBUG = os.getenv("DEBUG", False)

MONITOR_AGENT_ADDRESS = os.getenv("MONITOR_AGENT_ADDRESS", "localhost")
MONITOR_AGENT_PORT = os.getenv("MONITOR_AGENT_PORT", 8012)
POSTGRES_DB_ADDRESS = os.getenv("POSTGRES_DB_ADDRESS", "localhost")
POSTGRES_DB_PORT = os.getenv("POSTGRES_DB_PORT", 8002)
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "test_db")
POSTGRES_DB_USER = os.getenv("POSTGRES_DB_USER", "test_db")
POSTGRES_DB_PASSWORD = os.getenv("POSTGRES_DB_PASSWORD", "test_db")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", b'Thm1rA590U9IBSMMIlKWgBSPwbP30nz4keJR6N4RXjI=')
