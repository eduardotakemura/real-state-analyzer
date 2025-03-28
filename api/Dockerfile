FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --no-deps --require-hashes -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
