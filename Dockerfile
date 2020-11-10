FROM python:3.8.5
WORKDIR /code
RUN mkdir /temp_file
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
