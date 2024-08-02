FROM python:3.9.6

# RUN pip install --upgrade pip
RUN apt-get update && \
    apt-get install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# CMD ["python3", "main.py"]
