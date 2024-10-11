FROM python:3.10-slim

WORKDIR /app

RUN pip install poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install

COPY . .

CMD ["python", "app/bot.py"]