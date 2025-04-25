FROM python:3.12-slim

ENV TZ=America/New_York

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["python3.12"]
CMD ["httpceptor.py"]
