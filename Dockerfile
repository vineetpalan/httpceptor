FROM python:3.5

ENV TZ=America/New_York

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .

ENTRYPOINT ["python"]
CMD ["app.py"]
