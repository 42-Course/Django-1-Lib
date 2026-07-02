FROM python:3.12-slim

# Build deps for psycopg2 and friends.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Union of the libraries used across this day's exercises.
RUN pip install --no-cache-dir \
        requests beautifulsoup4 dewiki path django psycopg2-binary

COPY . /app

CMD ["bash"]
