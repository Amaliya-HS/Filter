FROM python

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "$PORT"]
