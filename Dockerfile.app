FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

COPY src/ src/
COPY bin/ bin/

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8001 4201

CMD ["bash", "bin/run_services.sh"]
