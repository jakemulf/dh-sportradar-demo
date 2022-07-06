FROM ghcr.io/deephaven/server:0.14.0
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
