FROM python:3.10.4

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./fastforge /fastforge

# CMD ["uvicorn", "fastforge.service.main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["celery", "worker", "--app=fastforge.worker.celery", "--loglevel=info", "--logfile=.celery.log"]