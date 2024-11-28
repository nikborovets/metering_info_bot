FROM python:3.9.6-slim

# RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen ru_RU.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# CMD ["python3", "main.py"]
