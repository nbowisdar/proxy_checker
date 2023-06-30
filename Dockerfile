FROM python:3.11.4-alpine3.17

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir aiogram --pre
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py", "--notify_problems"]