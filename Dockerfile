FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy metadata first (better caching)
COPY pyproject.toml ./

# Copy source
COPY src ./src

# Install runtime
RUN pip install --upgrade pip setuptools wheel \
    && pip install -e .

CMD ["agent", "run"]
