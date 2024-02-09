FROM python

RUN apt-get update && apt-get install -y v4l2loopback-dkms

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . .

RUN --privileged -d modprobe v4l2loopback

CMD ["gunicorn", "app:app"]
