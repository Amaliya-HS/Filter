FROM python

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

COPY . .

ENV PORT 5000

CMD python app.py runserver 0.0.0.0:$PORT
