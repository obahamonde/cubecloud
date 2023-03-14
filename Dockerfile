FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && apt-get install -y git \
    && git clone https://github.com/obahamonde/apprunner-codepen.git . \
    && apt-get remove -y git \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y python3-pip \
    && pip3 install -r requirements.txt \
    && apt-get remove -y python3-pip \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]