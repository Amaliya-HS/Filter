FROM python

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY . . 

CMD "uvicorn app:app --host 0.0.0.0 --port $port"
