### PYTHON BASE ###
FROM python:3.11.1-slim-bullseye as py-base

ENV PYTHONUNBUFFERED=1 \
    # prevents creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.3.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH=$POETRY_HOME/bin:$VENV_PATH/bin:$PATH

### BUILDER BASE ###
FROM py-base as builder-base

RUN apt update; apt install --no-install-recommends -y curl build-essential; \
    curl -sSL https://install.python-poetry.org | python3.11 -

WORKDIR $PYSETUP_PATH
COPY monitor_agent/poetry.lock .
COPY monitor_agent/pyproject.toml .

RUN poetry install --only main

### production ###
FROM py-base as prod

WORKDIR $PYSETUP_PATH

COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install; apt install openssl; mkdir -p $APP_HOME; \
    # mkdir -p $APP_HOME/logs; \
    mkdir -p /home/monitor-agent-app/; addgroup -S monitor; adduser -S monitor -G monitor;

ENV HOME=/home/monitor-agent-app/
ENV APP_HOME=/home/monitor-agent-app/monitor_agent

WORKDIR $APP_HOME

COPY monitor_agent $APP_HOME

RUN chown -R monitor:monitor $APP_HOME; chmod u+rwx -R $APP_HOME
USER monitor