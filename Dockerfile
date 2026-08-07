FROM python:3.13-slim

WORKDIR /wa-agent

COPY pyproject.toml uv.lock ./

RUN pip install uv

RUN uv sync --frozen --no-dev --no-editable

COPY . .

CMD ["uv", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
