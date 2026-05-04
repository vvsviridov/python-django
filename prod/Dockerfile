FROM python:3.12

# ENV PYTHONUNDUFFERED=1

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-install-project

COPY prod .

ENV PATH="/app/.venv/bin:$PATH"

CMD ["gnucorn", "myfirstsite.wsgi.application", "--bind", "0.0.0.0:8000"]