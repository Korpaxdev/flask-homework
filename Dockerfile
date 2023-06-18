FROM python:alpine
EXPOSE 5000
ENV PUTHONBUFFERED 1
ENV PYTHONDONTWRITEBYCODE 1

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction

COPY . .

CMD flask --app main run --host=0.0.0.0 -p 5000 --debug