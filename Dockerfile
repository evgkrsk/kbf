FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py .
ENTRYPOINT ["./app.py"]
