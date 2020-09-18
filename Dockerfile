FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD tail -f /dev/null
