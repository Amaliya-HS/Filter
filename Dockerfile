FROM python

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . .

RUN modprobe v4l2loopback

CMD ["gunicorn", "app:app"]
