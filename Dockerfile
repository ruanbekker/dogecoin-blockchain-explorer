FROM python:3.10-alpine

COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt

WORKDIR /src
COPY . .

CMD ["python", "/src/app.py"]
