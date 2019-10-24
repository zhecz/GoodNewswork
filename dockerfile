from alpine:latest
from python:latest

WORKDIR /app
COPY ./app .

RUN pip install --upgrade pip
RUN pip --no-cache-dir install -r /app/requirements.txt
EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["/app/run.py"]
