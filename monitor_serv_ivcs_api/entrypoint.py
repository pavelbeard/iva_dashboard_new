import os
import subprocess

PYTHON_NAME = "python3.11" if os.name == "posix" else "python"
WIN_APP_HOME = os.path.join("D:\\", "Pycharm", "work-projects", "iva_dashboard", "monitor_serv")
MONITOR_SERVER_ADDRESS = os.getenv('MONITOR_SERVER_ADDRESS', "2.0.96.3")
MONITOR_SERVER_PORT = os.getenv('MONITOR_SERVER_PORT', 8004)


def call_django_command(args, post_args: list | tuple):
    _args_ = args + post_args
    p = subprocess.Popen(_args_)
    p.communicate()

def check_db(args, post_args: list | tuple, database: str, seconds: int = None, attempts: int = None):
    _args_ = args + post_args
    _args_.append(database)

    if seconds is not None:
        _args_ += ["--seconds", seconds]
    if attempts is not None:
        _args_ += ["--attempts", attempts]

    p = subprocess.Popen(_args_)
    p.communicate()

    exit_code = p.returncode
    print(f"The task {database} has returned exit code {exit_code}.")

    if exit_code > 0:
        return False

    return True


if __name__ == '__main__':
    pre_args = [
        PYTHON_NAME, os.path.join(os.getenv('APP_HOME', WIN_APP_HOME), "manage.py"),
    ]
    result1 = check_db(pre_args, post_args=["checkdb", "--database"], database="ivcs")

    if result1:
        call_django_command(pre_args, ["migrate"])

        run_server = subprocess.Popen(
            ("uvicorn", "monitor_serv_ivcs_api.asgi:application",
             "--host", MONITOR_SERVER_ADDRESS, "--port", MONITOR_SERVER_PORT)
        )
        run_server.communicate()
