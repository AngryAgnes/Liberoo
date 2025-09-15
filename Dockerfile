
# ---------- Base stage ----------
FROM python:3.12-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
EXPOSE 8000

# ---------- Development stage ----------
FROM base AS dev
# In dev, app code is mounted from host, so no COPY needed
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ---------- Production stage ----------
FROM base AS prod
COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
