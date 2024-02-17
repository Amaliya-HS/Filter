FROM python

RUN apt-get update && apt-get install -y v4l2loopback-dkms

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . .

CMD ["gunicorn", "app:app"]
