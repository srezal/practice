FROM python:3.12-slim

WORKDIR /app

COPY ./pyproject.toml .

RUN pip install poetry && poetry install --no-root

COPY ./src ./src

CMD ["poetry", "run", "fastapi", "dev", "--host", "0.0.0.0", "src/main.py"]