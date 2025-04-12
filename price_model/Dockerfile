#FROM python:3.9
FROM tensorflow/tensorflow:2.18.0

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

#RUN pip install --no-cache-dir tensorflow==2.18.0 -i https://pypi.python.org/simple --trusted-host pypi.python.org

COPY . .

CMD ["python", "-u", "main.py"]
