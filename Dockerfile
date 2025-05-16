FROM python:3.11

RUN apt-get update && apt-get install -y graphviz gettext

# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# ensures that the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output of your application (e.g. django logs)
# in real time. Equivalent to python -u: https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1
# don't cache downloaded pip packages
ENV PIP_NO_CACHE_DIR=1
# disable version check of pip
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY . /app

RUN pip install /app && chown -R nobody /app

EXPOSE 5000

USER nobody

ENTRYPOINT ["/app/sample_project/entrypoint.sh"]
