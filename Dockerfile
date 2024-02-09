FROM python

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . . 

CMD "uvicorn app:app --host 0.0.0.0 --port $port"
