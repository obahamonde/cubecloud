FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/obahamonde/apprunner-codepen.git . && pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
