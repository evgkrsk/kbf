FROM python:3
WORKDIR /
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py .
ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]
