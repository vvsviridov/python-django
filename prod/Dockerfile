FROM python:3.12

# ENV PYTHONUNDUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY prod/pyproject.toml prod/uv.lock ./

RUN uv sync --frozen --no-cache --no-install-project

COPY prod .

ENV PATH="/app/.venv/bin:$PATH"

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "myfristsite.wsgi:application", "--bind", "0.0.0.0:8000"]