FROM python:3.12-slim

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY ./src ./src

CMD ["fastapi", "dev", "--host", "0.0.0.0", "src/main.py"]