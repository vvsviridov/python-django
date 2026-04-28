FROM python:3.12

# ENV PYTHONUNDUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-install-project

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]