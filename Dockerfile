FROM python:3.11

COPY . /app

RUN pip install /app

EXPOSE 8000

ENTRYPOINT ["/app/sample_project/entrypoint.sh"]
