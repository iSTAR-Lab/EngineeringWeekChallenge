FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py ./
COPY static/ ./static
COPY templates/ ./templates
COPY leaderboard.db ./

RUN pip3 install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "8", "app:app"]