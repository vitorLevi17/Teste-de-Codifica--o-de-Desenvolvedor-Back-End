FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]