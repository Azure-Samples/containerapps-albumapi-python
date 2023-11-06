
FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 3500

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3500"]
