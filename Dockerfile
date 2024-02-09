FROM python

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . .

CMD ["gunicorn", "app:app"]
