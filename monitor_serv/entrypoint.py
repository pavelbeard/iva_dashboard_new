import os
import subprocess

PYTHON_NAME = "python3.11" if os.name == "posix" else "python"
WIN_APP_HOME = os.path.join("D:\\", "Pycharm", "work-projects", "iva_dashboard", "monitor_serv")


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
    result1 = check_db(pre_args, post_args=["checkdb", "--database"], database="iva_dashboard")
    result2 = check_db(pre_args, post_args=["checkdb", "--database"], database="ivcs")

    if result1 and result2:
        call_django_command(pre_args, ["migrate", "dashboard", "--database", "iva_dashboard"])
        call_django_command(pre_args, ["migrate", "dashboard_users", "--database", "iva_dashboard"])
        call_django_command(pre_args, ["migrate", "admin", "--database", "iva_dashboard"])
        call_django_command(pre_args, ["addscrapecommands"])
        call_django_command(pre_args, ["setupdashboard"])
        call_django_command(pre_args, ["createsuperuser", "--username", os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin'),
                                       "--noinput", "--database", "iva_dashboard",
                                       "--email", os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')])
        call_django_command(pre_args, ["collectstatic", "--noinput", "--clear"])

        run_server = subprocess.Popen(
            ("uvicorn", "monitor_serv.asgi:application",
             "--host", "0.0.0.0", "--port", "8000")
        )
        run_server.communicate()


